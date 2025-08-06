from flask import Blueprint, render_template
import json
import os

routes = Blueprint("routes", __name__)

# Construct absolute path to data folder
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def load_json(file_name):
    full_path = os.path.join(DATA_PATH, file_name)
    print(f"Loading data from: {full_path}")  # Debug path
    with open(full_path, "r", encoding="utf-8") as file:
        return json.load(file)

@routes.route("/")
def index():
    jobs = load_json("jobs.json")
    news = load_json("news.json")
    products = load_json("products.json")

    metrics = {
        "jobs_count": len(jobs),
        "news_count": len(news),
        "products_count": len(products)
    }

    return render_template("index.html", jobs=jobs, news=news, products=products, metrics=metrics)
