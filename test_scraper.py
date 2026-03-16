from utils import extract_all_opinions

product_id = "170164749"

opinions = extract_all_opinions(product_id)

print("Łączna liczba opinii:", len(opinions))

if opinions:
    print("\n=== PIERWSZA OPINIA ===\n")
    print(opinions[0])

    print("\n=== OSTATNIA OPINIA ===\n")
    print(opinions[-1])