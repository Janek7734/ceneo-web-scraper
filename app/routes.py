from flask import render_template


def register_routes(app):
    @app.route("/")
    def index():
        return "Ceneo Web Scraper"

    @app.route("/extract")
    def extract():
        return "Extract page"

    @app.route("/products")
    def products():
        return "Products page"

    @app.route("/product/<product_id>")
    def product(product_id):
        return f"Product page: {product_id}"

    @app.route("/charts/<product_id>")
    def charts(product_id):
        return f"Charts page: {product_id}"