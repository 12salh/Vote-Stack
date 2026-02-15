from flask import Flask, render_template_string, request
import redis
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

HTML = """
<h1>Vote!</h1>
<form method="POST">
  <button name="vote" value="cats">🐱 Cats</button>
  <button name="vote" value="dogs">🐶 Dogs</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        r.lpush("votes", request.form["vote"])
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
