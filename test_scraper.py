from app.scraper import fetch_page, parse_html, build_reviews_url

product_id = "183662361"
url = build_reviews_url(product_id, page=1)

html = fetch_page(url)
soup = parse_html(html)

print("URL:", url)
print("Długość HTML:", len(html))
print("\n=== LINKI Z PIERWSZEJ STRONY ===\n")

for link in soup.find_all("a", href=True):
    href = link["href"]
    text = link.get_text(" ", strip=True)

    if "opini" in href.lower() or "review" in href.lower() or "opini" in text.lower():
        print("TEXT:", text)
        print("HREF:", href)
        print("-" * 80)