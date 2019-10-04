#import libraries

from flask import Flask, render_template
import pymongo
import scrape

#Creates the Flask app to pass the information when called
#create flask instance
app = Flask(__name__)

# creates connection to mongo bd running and creates connection to the data blob collections
#create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries

#using the Flask app do this when the route is requested.
# do this is route titled home pulls data from Mongo db blob and sets it into a template a file called index.html
@app.route("/")
def home():
    mars_data = list(db.collecion.find())[0]
    return render_template('index.html', mars_data=mars_data)

using the Flask app do this when the route is requested.
# do this is route titled scrape pulls data from Mongo db blob and sets it into a template a file called index.html
#First step empties the db blob
@app.route("/scrape")
def scrape():
    db.collection.remove({})

    db.collection.insert_one(mars_data)
    return render_template('scrape.html')


if __name__ == "__main__":
    app.run(debug=True)
