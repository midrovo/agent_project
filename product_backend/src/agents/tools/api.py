import requests
from src.core.config import settings

def search_product(name: str) -> dict:
    """
        Busca un producto por su nombre en la API de productos

        Argumentos:
            name (str): Nombre del producto a buscar

        Respuesta: Diccionario con la información del producto encontrado
    """

    response = requests.get(f"{ settings.API_BASE_URL }/name/{ name }")

    print(response)

    return response.json()


def create_product(
        name: str,
        description: str,
        stock: float,
        list_price: float,
        standard_price: float,
        discount: float,
        image: str = None
) -> dict:
    """
        Crea un nuevo producto (Unico) en la API de productos.

        Nota:
            - El campo `description` puede ser generado automáticamente
            usando el tool `describe_product` si no lo proporciona el usuario.
            - El campo `image` puede ser generado automáticamente
            usando el tool `generate_product_image`
            - Antes de crear el producto debes asegurar que el nombre
            no se repita usando el tool `search_product`

        Args:
            name (str): Nombre del producto (obligatorio)
            description (str): Descripción comercial del producto (obligatorio)
            stock (float): Cantidad disponible en inventario (obligatorio)
            list_price (float): Precio de venta (obligatorio)
            standard_price (float): Precio de costo (obligatorio)
            discount (float): Porcentaje de descuento (obligatorio)
            image (str, optional): URL de la imagen del producto

        Returns:
            dict: Información del producto creado.
    """

    payload = {
        "name": name,
        "description": description,
        "stock": stock,
        "list_price": list_price,
        "standard_price": standard_price,
        "discount": discount,
    }
    if image is not None:
        payload["image"] = image

    response = requests.post(
        f"{ settings.API_BASE_URL }/{ name }",
        json=payload
    )

    return response.json()


def update_product(
        name: str,
        description: str,
        stock: float,
        list_price: float,
        standard_price: float,
        discount: float,
        image: str = None
) -> dict:
    """
        Actualiza un producto existente en la API de productos.

        Nota:
            - El campo `image` puede ser generado automáticamente
              usando el tool `generate_product_image`
            - Antes de actualizar la imagen del producto se verifica
              si no la tiene usando el tool `search_product`
            - El nombre del producto si se puede actualizar  

        Args:
            name (str): Nombre del producto que se va a actualizar.
            description (str): Descripción del producto.
            stock (float): Cantidad en inventario.
            list_price (float): Precio de venta.
            standard_price (float): Precio de costo.
            discount (float): Porcentaje de descuento.
            image (str, optional): URL de la imagen del producto.

        Returns:
            dict: Información actualizada del producto.
    """

    payload = {
        "name": name,
        "description": description,
        "stock": stock,
        "list_price": list_price,
        "standard_price": standard_price,
        "discount": discount,
    }
    if image is not None:
        payload["image"] = image

    response = requests.put(
        f"{ settings.API_BASE_URL }/{ name }",
        json=payload
    )

    return response.json()