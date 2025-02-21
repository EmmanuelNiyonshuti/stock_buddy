from app.models.product import Product

def get_inventory(product_id):
    product = Product.get(product_id)
    return product.inventory