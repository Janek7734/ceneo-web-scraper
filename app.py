from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Ceneo Web Scraper</h1><p>Projekt na Computer Programming 2</p>"

if __name__ == "__main__":
    app.run(debug=True)