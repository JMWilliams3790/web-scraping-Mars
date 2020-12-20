from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/about_mars"
mongo = PyMongo(app)



# clear all existing data out of the collection.
# For demo purposes only, 
# you may not want to do this for an app you're building!
mongo.db.mars.drop()

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    if mars == None:
            mars = {
        "news" : None,
        "image" : None,
        "table" : None,
        "hemisphere" : [None,None,None,None]
    }
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
