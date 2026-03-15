import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_page(html):
    return BeautifulSoup(html, "lxml")

def get_product_reviews_url(product_id):
    return f"https://www.ceneo.pl/{product_id}#tab=reviews"

def extract_opinion(opinion_element):
    opinion = {
        "opinion_id": opinion_element.get("data-entry-id", ""),
        "author": "",
        "recommendation": "",
        "score": "",
        "content": "",
        "pros": [],
        "cons": [],
        "helpful": "0",
        "unhelpful": "0",
        "publish_date": "",
        "purchase_date": ""
    }

    author = opinion_element.select_one(".user-post__author-name")
    if author:
        opinion["author"] = author.get_text(strip=True)

    recommendation = opinion_element.select_one(".user-post__author-recomendation em")
    if recommendation:
        opinion["recommendation"] = recommendation.get_text(strip=True)

    score = opinion_element.select_one(".user-post__score-count")
    if score:
        opinion["score"] = score.get_text(strip=True)

    content = opinion_element.select_one(".user-post__text")
    if content:
        opinion["content"] = content.get_text("\n", strip=True)

    helpful = opinion_element.select_one("button.vote-yes span")
    if helpful:
        opinion["helpful"] = helpful.get_text(strip=True)

    unhelpful = opinion_element.select_one("button.vote-no span")
    if unhelpful:
        opinion["unhelpful"] = unhelpful.get_text(strip=True)

    times = opinion_element.select(".user-post__published time")
    if len(times) > 0:
        opinion["publish_date"] = times[0].get("datetime", "")
    if len(times) > 1:
        opinion["purchase_date"] = times[1].get("datetime", "")

    feature_sections = opinion_element.select(".review-feature__section")

    for section in feature_sections:
        title = section.get_text(" ", strip=True).lower()

        items = [
            item.get_text(strip=True)
            for item in section.select(".review-feature__item")
        ]

        if "zalety" in title:
            opinion["pros"] = items
        elif "wady" in title:
            opinion["cons"] = items

    return opinion