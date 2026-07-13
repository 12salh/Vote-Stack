from flask import Flask, render_template_string, request
import redis
import os
from datetime import datetime


app = Flask(__name__)


# Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)



HTML = """

<!DOCTYPE html>
<html>

<head>

<title>DevOps Voting System</title>


<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial,sans-serif;
}


body{

    height:100vh;

    display:flex;

    justify-content:center;

    align-items:center;

    background:
    linear-gradient(135deg,#020617,#1d4ed8);

    color:white;

}


.container{

    width:600px;

    padding:40px;

    text-align:center;

    background:rgba(255,255,255,0.12);

    backdrop-filter:blur(15px);

    border-radius:25px;

    box-shadow:0 20px 50px black;

}



h1{

    font-size:42px;

    margin-bottom:20px;

}



p{

    color:#cbd5e1;

    margin-bottom:35px;

}



.buttons{

    display:flex;

    justify-content:center;

    gap:25px;

}



button{

    width:200px;

    height:90px;

    border:none;

    border-radius:20px;

    font-size:28px;

    cursor:pointer;

    color:white;

    transition:.3s;

}



button:hover{

    transform:scale(1.1);

}



.cat{

    background:#f97316;

}



.dog{

    background:#22c55e;

}



.success{

    background:#16a34a;

    padding:20px;

    border-radius:15px;

    font-size:20px;

}



.error{

    background:#dc2626;

    padding:20px;

    border-radius:15px;

    font-size:20px;

}



.footer{

    margin-top:30px;

    color:#94a3b8;

    font-size:14px;

}


</style>


</head>



<body>


<div class="container">


<h1>
🐾 Voting System
</h1>


<p>
Choose your favorite animal
</p>



{% if message %}

<div class="{{status}}">
{{message}}
</div>


{% else %}


<form method="POST">


<div class="buttons">


<button class="cat"
name="vote"
value="cats">

🐱 Cats

</button>


<button class="dog"
name="vote"
value="dogs">

🐶 Dogs

</button>


</div>


</form>


{% endif %}



<div class="footer">

Flask + Redis + Kubernetes

</div>


</div>


</body>

</html>

"""



def get_user_ip():

    """
    Get real client IP behind Load Balancer
    """

    if request.headers.get("X-Forwarded-For"):

        return request.headers.get(
            "X-Forwarded-For"
        ).split(",")[0]


    return request.remote_addr





@app.route("/", methods=["GET","POST"])
def vote():


    user_ip = get_user_ip()


    voter_key = f"voter:{user_ip}"



    # Check previous vote

    old_vote = redis_client.get(
        voter_key
    )


    if old_vote:


        return render_template_string(
            HTML,
            message=f"❌ You already voted ({old_vote})",
            status="error"
        )



    if request.method == "POST":


        selected_vote = request.form.get(
            "vote"
        )



        if selected_vote not in [
            "cats",
            "dogs"
        ]:


            return "Invalid vote"



        # Save vote

        redis_client.lpush(
            "votes",
            selected_vote
        )



        # Save user

        redis_client.set(
            voter_key,
            selected_vote
        )


        # Store voting time

        redis_client.hset(

            f"vote_info:{user_ip}",

            mapping={

                "vote": selected_vote,

                "time": str(datetime.now())

            }

        )



        return render_template_string(

            HTML,

            message="✅ Your vote has been recorded!",

            status="success"

        )



    return render_template_string(

        HTML,

        message=None,

        status=None

    )




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=80
    )
