#from flask import Flask, jsonify, render_template_string
#import redis, os

#app = Flask(__name__)
#r = redis.Redis(host='redis', port=6379, decode_responses=True)

#HTML = """
#<h1>Voting Result</h1>
#<p>🐱 Cats: {{cats}}</p>
#<p>🐶 Dogs: {{dogs}}</p>
#"""

#@app.route("/")
#def index():
#    cats = int(r.get("cats") or 0)
#    dogs = int(r.get("dogs") or 0)
#    return render_template_string(HTML, cats=cats, dogs=dogs)

#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=80)
from flask import Flask, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)

db = client.voting
collection = db.votes

HTML = """
<h1>Voting Result</h1>
<p>🐱 Cats: {{cats}}</p>
<p>🐶 Dogs: {{dogs}}</p>
"""

@app.route("/")
def index():
    cats = collection.count_documents({"vote": "cats"})
    dogs = collection.count_documents({"vote": "dogs"})
    return render_template_string(HTML, cats=cats, dogs=dogs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
