import requests
from bs4 import BeautifulSoup

from app.models import Opinion


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pl,en-US;q=0.9,en;q=0.8",
    "Referer": "https://www.ceneo.pl/",
    "Upgrade-Insecure-Requests": "1",
}


def fetch_page(url, referer=None):
    headers = HEADERS.copy()
    if referer:
        headers["Referer"] = referer

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def parse_html(html):
    return BeautifulSoup(html, "html.parser")


def build_reviews_url(product_id):
    return f"https://www.ceneo.pl/{product_id}#tab=reviews"


def extract_product_name(soup):
    title = soup.select_one("h1")
    if title:
        return title.get_text(strip=True)
    return ""


def extract_single_opinion(opinion_element):
    opinion = Opinion(
        opinion_id=opinion_element.get("data-entry-id", "")
    )

    author = opinion_element.select_one(".user-post__author-name")
    if author:
        opinion.author = author.get_text(strip=True)

    recommendation = opinion_element.select_one(".user-post__author-recomendation em")
    if recommendation:
        opinion.recommendation = recommendation.get_text(strip=True)

    score = opinion_element.select_one(".user-post__score-count")
    if score:
        opinion.score = score.get_text(strip=True)

    content = opinion_element.select_one(".user-post__text")
    if content:
        opinion.content = content.get_text("\n", strip=True)

    helpful = opinion_element.select_one("button.vote-yes")
    if helpful:
        opinion.helpful = helpful.get("data-total-vote", "0")

    unhelpful = opinion_element.select_one("button.vote-no")
    if unhelpful:
        opinion.unhelpful = unhelpful.get("data-total-vote", "0")

    pros = opinion_element.select(".review-feature__item--positive")
    opinion.pros = [item.get_text(strip=True) for item in pros]

    cons = opinion_element.select(".review-feature__item--negative")
    opinion.cons = [item.get_text(strip=True) for item in cons]

    times = opinion_element.select(".user-post__published time")
    if len(times) > 0:
        opinion.publish_date = times[0].get("datetime", "")
    if len(times) > 1:
        opinion.purchase_date = times[1].get("datetime", "")

    return opinion


def extract_opinions_from_structured_html(soup):
    opinion_elements = soup.select("div.js_product-review:not(.user-post--highlight)")
    return [extract_single_opinion(opinion) for opinion in opinion_elements]


def get_next_page_url(soup):
    next_page = soup.select_one("a.pagination__next")

    if next_page and next_page.get("href"):
        href = next_page.get("href")

        if href.startswith("http"):
            return href
        return "https://www.ceneo.pl" + href

    return None


def extract_product(product_id, max_pages=50):
    opinions = []
    product_name = ""
    visited_urls = set()

    url = build_reviews_url(product_id)
    referer = None
    page = 1

    while url and page <= max_pages and url not in visited_urls:
        visited_urls.add(url)

        print("Pobieram:", url)

        html = fetch_page(url, referer=referer)
        soup = parse_html(html)

        if not product_name:
            product_name = extract_product_name(soup)

        page_opinions = extract_opinions_from_structured_html(soup)
        print("Znaleziono opinii:", len(page_opinions))

        if not page_opinions:
            break

        opinions.extend(page_opinions)

        referer = url
        url = get_next_page_url(soup)
        page += 1

    return product_name, opinions