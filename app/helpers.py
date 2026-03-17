import os
import json


def score_to_float(score_text):
    if not score_text:
        return 0.0

    try:
        return float(score_text.split("/")[0].replace(",", "."))
    except (ValueError, AttributeError, IndexError):
        return 0.0


def calculate_stats(opinions):
    opinions_count = len(opinions)
    pros_count = sum(1 for opinion in opinions if opinion.pros)
    cons_count = sum(1 for opinion in opinions if opinion.cons)

    scores = [score_to_float(opinion.score) for opinion in opinions if opinion.score]
    average_score = round(sum(scores) / len(scores), 2) if scores else 0.0

    recommendations = {
        "Polecam": 0,
        "Nie polecam": 0,
        "Brak": 0
    }

    for opinion in opinions:
        if opinion.recommendation == "Polecam":
            recommendations["Polecam"] += 1
        elif opinion.recommendation == "Nie polecam":
            recommendations["Nie polecam"] += 1
        else:
            recommendations["Brak"] += 1

    stars_distribution = {
        "0.5": 0,
        "1.0": 0,
        "1.5": 0,
        "2.0": 0,
        "2.5": 0,
        "3.0": 0,
        "3.5": 0,
        "4.0": 0,
        "4.5": 0,
        "5.0": 0
    }

    for opinion in opinions:
        value = score_to_float(opinion.score)
        if value > 0:
            key = f"{value:.1f}"
            if key in stars_distribution:
                stars_distribution[key] += 1

    return {
        "opinions_count": opinions_count,
        "pros_count": pros_count,
        "cons_count": cons_count,
        "average_score": average_score,
        "recommendations": recommendations,
        "stars_distribution": stars_distribution
    }


def ensure_data_folders():
    os.makedirs("data/opinions", exist_ok=True)
    os.makedirs("data/products", exist_ok=True)


def save_product(product):
    ensure_data_folders()

    opinions_path = f"data/opinions/{product.product_id}.json"
    product_path = f"data/products/{product.product_id}.json"

    with open(opinions_path, "w", encoding="utf-8") as f:
        json.dump(
            [opinion.to_dict() for opinion in product.opinions],
            f,
            ensure_ascii=False,
            indent=4
        )

    with open(product_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "product_id": product.product_id,
                "product_name": product.product_name,
                "stats": product.stats
            },
            f,
            ensure_ascii=False,
            indent=4
        )


def load_product(product_id):
    from app.models import Product, Opinion

    product_path = f"data/products/{product_id}.json"
    opinions_path = f"data/opinions/{product_id}.json"

    with open(product_path, "r", encoding="utf-8") as f:
        product_data = json.load(f)

    with open(opinions_path, "r", encoding="utf-8") as f:
        opinions_data = json.load(f)

    opinions = []
    for opinion_data in opinions_data:
        opinion = Opinion(
            opinion_id=opinion_data.get("opinion_id", ""),
            author=opinion_data.get("author", ""),
            recommendation=opinion_data.get("recommendation", ""),
            score=opinion_data.get("score", ""),
            content=opinion_data.get("content", ""),
            pros=opinion_data.get("pros", []),
            cons=opinion_data.get("cons", []),
            helpful=opinion_data.get("helpful", "0"),
            unhelpful=opinion_data.get("unhelpful", "0"),
            publish_date=opinion_data.get("publish_date", ""),
            purchase_date=opinion_data.get("purchase_date", "")
        )
        opinions.append(opinion)

    return Product(
        product_id=product_data["product_id"],
        product_name=product_data.get("product_name", ""),
        opinions=opinions,
        stats=product_data.get("stats", {})
    )