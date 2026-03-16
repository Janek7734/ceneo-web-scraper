from utils import extract_all_opinions, save_to_json

product_id = "183662361"

opinions = extract_all_opinions(product_id)
save_to_json(product_id, opinions)

print("Zapisano opinie do pliku JSON.")
print("Liczba opinii:", len(opinions))