import requests
from bs4 import BeautifulSoup
import json
import os
import re


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_page(html):
    return BeautifulSoup(html, "html.parser")


def get_product_reviews_url(product_id):
    return f"https://www.ceneo.pl/{product_id}#tab=reviews"


def get_reviews_page_url(product_id, page_number):
    if page_number == 1:
        return f"https://www.ceneo.pl/{product_id}#tab=reviews"
    return f"https://www.ceneo.pl/{product_id}/opinie-{page_number}"


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


def extract_opinions_from_page(soup):
    opinions = soup.select("div.js_product-review")

    if opinions:
        real_opinions = [
            op for op in opinions
            if not op.select_one(".user-post__aisummary-author-name")
        ]
        return [extract_opinion(op) for op in real_opinions]

    # fallback dla starszego układu stron /opinie-2, /opinie-3 itd.
    text = soup.get_text("\n", strip=True)

    blocks = re.split(
        r'(?=(?:Użytkownik Ceneo|[A-ZĄĆĘŁŃÓŚŹŻa-ząćęłńóśźż0-9._-]{2,})\s+Ocena:\s*\d+(?:,\d+)?/5)',
        text
    )

    results = []
    for block in blocks:
        if "Ocena:" not in block:
            continue

        author_match = re.search(r'^([^\n]+?)\s+Ocena:', block)
        score_match = re.search(r'Ocena:\s*([0-9]+(?:,[0-9]+)?/5)', block)
        recommendation_match = re.search(r'\b(Polecam|Nie polecam)\b', block)

        author = author_match.group(1).strip() if author_match else ""
        score = score_match.group(1).strip() if score_match else ""
        recommendation = recommendation_match.group(1).strip() if recommendation_match else ""

        lines = [line.strip() for line in block.splitlines() if line.strip()]

        content_lines = []
        start_collecting = False
        stop_words = {
            "Zalety", "Wady", "Kupiono w", "Rekomendowane oferty",
            "Skomentuj opinię", "Twój komentarz", "Odpowiedz", "Zgłoś"
        }

        for line in lines:
            if "Ocena:" in line:
                start_collecting = True
                continue
            if start_collecting:
                if line in stop_words:
                    break
                if not line.startswith("Wystawiono") and "Zaufana Opinia" not in line:
                    content_lines.append(line)

        content = "\n".join(content_lines).strip()

        results.append({
            "opinion_id": "",
            "author": author,
            "recommendation": recommendation,
            "score": score,
            "content": content,
            "pros": [],
            "cons": [],
            "helpful": "0",
            "unhelpful": "0",
            "publish_date": "",
            "purchase_date": "",
        })

    return results


def extract_all_opinions(product_id):
    all_opinions = []
    page_number = 1

    while True:
        url = get_reviews_page_url(product_id, page_number)
        print("Pobieram:", url)

        html = get_page(url)
        soup = parse_page(html)

        opinions = extract_opinions_from_page(soup)
        print("Znaleziono opinii na tej stronie:", len(opinions))

        if not opinions:
            break

        all_opinions.extend(opinions)
        page_number += 1

    return all_opinions


def save_to_json(product_id, opinions):
    os.makedirs("data/opinions", exist_ok=True)

    file_path = f"data/opinions/{product_id}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(opinions, f, ensure_ascii=False, indent=4)