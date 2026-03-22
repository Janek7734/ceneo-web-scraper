from app.scraper import extract_product

product_id = "167962745"

product_name, opinions = extract_product(product_id)

print("Nazwa produktu:", product_name)
print("Liczba opinii:", len(opinions))

if opinions:
    print(opinions[0].to_dict())
    print(opinions[-1].to_dict())