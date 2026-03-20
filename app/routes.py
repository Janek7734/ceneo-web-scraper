from flask import render_template, request, redirect, url_for, send_file


from app.scraper import extract_product
from app.models import Product
from app.helpers import (
    calculate_stats,
    save_product,
    load_product,
    load_all_products,
    save_opinions_to_csv,
    save_opinions_to_xlsx
)


def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/extract", methods=["GET", "POST"])
    def extract():
        if request.method == "POST":
            product_id = request.form.get("product_id", "").strip()

            if not product_id:
                return render_template("extract.html", error="Podaj product_id.")

            try:
                product_name, opinions = extract_product(product_id)

                if not product_name or not opinions:
                    return render_template(
                        "extract.html",
                        error="Nie udało się pobrać produktu lub opinii."
                    )

                product = Product(
                    product_id=product_id,
                    product_name=product_name,
                    opinions=opinions
                )

                product.stats = calculate_stats(product.opinions)
                save_product(product)
                save_opinions_to_csv(product)
                save_opinions_to_xlsx(product)

                return redirect(url_for("product", product_id=product_id))

            except Exception as e:
                return render_template("extract.html", error=f"Błąd: {e}")

        return render_template("extract.html", error=None)

    @app.route("/products")
    def products():
        products = load_all_products()

        sort_by = request.args.get("sort", "")

        if sort_by == "rating_desc":
            products = sorted(
                products,
                key=lambda product: product.stats.get("average_score", 0),
                reverse=True
            )
        elif sort_by == "rating_asc":
            products = sorted(
                products,
                key=lambda product: product.stats.get("average_score", 0)
            )

        return render_template("products.html", products=products, sort_by=sort_by)

    @app.route("/product/<product_id>")
    def product(product_id):
        try:
            product = load_product(product_id)

            author_filter = request.args.get("author", "").strip().lower()
            sort_by = request.args.get("sort", "")

            filtered_opinions = product.opinions

            if author_filter:
                filtered_opinions = [
                    opinion for opinion in filtered_opinions
                    if author_filter in opinion.author.lower()
                ]

            if sort_by == "score_asc":
                filtered_opinions = sorted(
                    filtered_opinions,
                    key=lambda opinion: float(opinion.score.split("/")[0].replace(",", ".")) if opinion.score else 0
                )
            elif sort_by == "score_desc":
                filtered_opinions = sorted(
                    filtered_opinions,
                    key=lambda opinion: float(opinion.score.split("/")[0].replace(",", ".")) if opinion.score else 0,
                    reverse=True
                )

            return render_template(
                "product.html",
                product=product,
                opinions=filtered_opinions,
                author_filter=author_filter,
                sort_by=sort_by
            )
        except Exception as e:
            return f"Błąd ładowania produktu: {e}"

    @app.route("/charts/<product_id>")
    def charts(product_id):
        try:
            product = load_product(product_id)
            return render_template("charts.html", product=product)
        except Exception as e:
            return f"Błąd ładowania wykresów: {e}"

    @app.route("/download/json/<product_id>")
    def download_json(product_id):
        return send_file(f"data/opinions/{product_id}.json", as_attachment=True)

    @app.route("/download/csv/<product_id>")
    def download_csv(product_id):
        return send_file(f"data/opinions/{product_id}.csv", as_attachment=True)

    @app.route("/download/xlsx/<product_id>")
    def download_xlsx(product_id):
        return send_file(f"data/opinions/{product_id}.xlsx", as_attachment=True)

    @app.route("/about")
    def about():
        return render_template("about.html")