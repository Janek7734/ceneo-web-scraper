from app.scraper import extract_product
from app.models import Product
from app.helpers import calculate_stats, save_product

product_id = "183662361"

product_name, opinions = extract_product(product_id)

product = Product(
    product_id=product_id,
    product_name=product_name,
    opinions=opinions
)

product.stats = calculate_stats(product.opinions)
save_product(product)

print("Nazwa produktu:", product.product_name)
print("Liczba opinii:", len(product.opinions))
print("Statystyki:", product.stats)