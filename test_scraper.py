from utils import get_page, parse_page, get_product_reviews_url, extract_opinion

product_id = "183662361"
url = get_product_reviews_url(product_id)

html = get_page(url)
soup = parse_page(html)

opinions = soup.select("div.js_product-review")

real_opinions = [
    op for op in opinions
    if not op.select_one(".user-post__aisummary-author-name")
]

print("Liczba wszystkich bloków:", len(opinions))
print("Liczba zwykłych opinii:", len(real_opinions))

if real_opinions:
    first_opinion = extract_opinion(real_opinions[0])
    print("\n=== PIERWSZA OPINIA ===\n")
    print(first_opinion)
else:
    print("Brak zwykłych opinii.")