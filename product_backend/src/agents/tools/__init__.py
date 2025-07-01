from .image import generate_product_image
from .description import describe_product
from .api import search_product, create_product, update_product

tools = [
    search_product,
    create_product,
    update_product,
    describe_product,
    generate_product_image
]
