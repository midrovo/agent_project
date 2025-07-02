import io, base64, uuid
from src.core.config import settings
import cloudinary
import cloudinary.uploader
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from src.agents.llm.prompts import IMAGE_PROMPT



def generate_product_image(name: str) -> dict:
    """
    Genera una imagen para una app móvil basada en el nombre del producto,
    sube la imagen a Cloudinary y devuelve la URL.
    """

    # LLM para generar la imagen
    llm_img = ChatOpenAI(model="gpt-4.1-mini", output_version="responses/v1")
    tool_img = {"type": "image_generation", "quality": "low"}
    llm_with_tools_img = llm_img.bind_tools([tool_img])

    # system_message = SystemMessage(content=IMAGE_PROMPT(name))

    ai_message = llm_with_tools_img.invoke(IMAGE_PROMPT(name))

    image = next(item for item in ai_message.content if item["type"] == "image_generation_call")
    binary = base64.b64decode(image["result"])

    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )

    image_file = io.BytesIO(binary)
    image_file.name = "product_image.png"

    public_id = f"product_{uuid.uuid4()}"

    try:
        upload_result = cloudinary.uploader.upload(
            image_file,
            public_id=public_id
        )
        return {
            "name": name,
            "image_url": upload_result["secure_url"],
            "success": True
        }
    except Exception as e:
        return {
            "name": name,
            "error": str(e),
            "success": False
        }
