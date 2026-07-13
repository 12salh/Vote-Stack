from flask import Flask, render_template_string
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client.voting
collection = db.votes


HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Voting Dashboard</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial, sans-serif;
}


body{

    min-height:100vh;

    background:linear-gradient(135deg,#0f172a,#2563eb);

    display:flex;

    justify-content:center;

    align-items:center;

    color:white;

}


.container{

    width:800px;

    max-width:90%;

    padding:40px;

    background:rgba(255,255,255,0.1);

    backdrop-filter:blur(15px);

    border-radius:25px;

    text-align:center;

    box-shadow:0 20px 50px rgba(0,0,0,.5);

}


h1{

    font-size:45px;

    margin-bottom:15px;

}


.subtitle{

    color:#cbd5e1;

    margin-bottom:40px;

}



.cards{

    display:flex;

    justify-content:center;

    gap:30px;

    flex-wrap:wrap;

}



.card{

    width:250px;

    padding:30px;

    border-radius:20px;

    background:rgba(255,255,255,.15);

    transition:.3s;

}


.card:hover{

    transform:translateY(-10px);

}



.icon{

    font-size:60px;

}


.name{

    font-size:28px;

    margin:15px;

}



.count{

    font-size:55px;

    font-weight:bold;

}



.cat{

    border:2px solid #f97316;

}


.dog{

    border:2px solid #22c55e;

}



.status{

    margin-top:40px;

    padding:15px;

    background:#16a34a;

    border-radius:30px;

}


.footer{

    margin-top:30px;

    color:#cbd5e1;

}


</style>

</head>


<body>


<div class="container">


<h1>
🐾 Voting Results
</h1>


<p class="subtitle">
Cats vs Dogs Voting System
</p>



<div class="cards">


<div class="card cat">

<div class="icon">
🐱
</div>

<div class="name">
Cats
</div>

<div class="count">
{{cats}}
</div>

<p>
Total Votes
</p>

</div>




<div class="card dog">

<div class="icon">
🐶
</div>

<div class="name">
Dogs
</div>


<div class="count">
{{dogs}}
</div>


<p>
Total Votes
</p>


</div>


</div>



<div class="status">

🟢 Database Connected | Voting System Running

</div>


<div class="footer">

Powered by Flask + MongoDB

</div>


</div>


</body>

</html>
"""


@app.route("/")
def index():

    cats = collection.count_documents({"vote": "cats"})

    dogs = collection.count_documents({"vote": "dogs"})

    return render_template_string(
        HTML,
        cats=cats,
        dogs=dogs
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=80
    )
