def IMAGE_PROMPT(name: str) -> str:
    prompt = f"""
    Crea una imagen para una aplicación móvil de tienda que muestre {name}: 
    un producto moderno y atractivo, con diseño detallado y realista. 
    Debe tener un fondo blanco limpio, iluminación de estudio, alta resolución y detalle, 
    sin logotipos ni marcas visibles. El producto debe destacar sus características principales, 
    en un estilo visual adecuado para mostrar en una app de compras.
    """
    return prompt


def DESCRIBE_PROMPT(name: str) -> str:
    prompt = f"""
    Imagina que eres un redactor creativo de una tienda online. 
    El producto se llama: {name}. 
    Describe brevemente qué es, qué beneficios tiene y usa un tono amable y atractivo, 
    como para mostrarlo a un cliente en un ecommerce. 
    Mantén la descripción corta, máximo 3 líneas y 200 caracteres.
    """
    return prompt


def INITIAL_PROMPT() -> str:
    prompt = """
    Eres un asistente experto en inventarios. 
    Puedes buscar, guardar y actualizar productos, generar imágenes y descripciones.
    Usa las herramientas disponibles para ayudarte.
    Importante: se requiere que el usuario ingrese el stock, la lista de precio, el costo y el nombre
    """
    return prompt