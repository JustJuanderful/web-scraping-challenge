
# MongoDB and Flask Application
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import sys
import os

# Flask Setup
app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Flask Route
@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route
@app.route("/scrape")
def scrape():
    mars_df = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_df, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)