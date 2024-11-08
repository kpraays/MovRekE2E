from flask import Flask, g
import requests
import os
from model.movie_rec import get_recommendation, train, load_model
from prometheus_flask_exporter import PrometheusMetrics
from container_db_connect import connect_db, db_insert

app = Flask(__name__)
metrics = PrometheusMetrics(app)
global_version = "default"

def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.teardown_appcontext
def teardown_db(e=None):
    close_db(e)


with app.app_context():
    # Train the model the first time the container is started and load it locally
    try:
        train()
        # create connection with db
        conn = get_db()

        with open("auto_deployment/version.txt", "r") as f:
            global_version = int(str(f.read()))
            
        
    except Exception as exc:
        print(f"Error occurred while training model: {exc}")
    
    finally:
        close_db()

    try:
        load_model()
    except Exception as exc:
        print(f"Error occurred while loading model: {exc}")


def get_user_details(userid):
    """
    Retrieve user details from the user API.

        :param userid: user id for prediction
    """
    try:
        response = requests.get(
            "http://fall2023-comp585.cs.mcgill.ca:8080/user/"+str(userid))

        if response.status_code != 200:
            return "Response not successful"

        return response.json()
    except Exception as exc:
        print(f"Unexpected exception raised while getting user details: {exc}")
        return "Error: " + str(exc)


def predict_movies(userid):
    """
    Return the list of movies from model's prediction

        :param userid: user id for prediction    
    """
    # we might have to send request to server to retrieve attributes for the user
    # these may be needed to send to the model.
    try:
        prediction = get_recommendation(userid)
        db_insert(get_db(), "reccom", {"version_number": global_version, "user_id": userid})
        return ",".join(prediction)
    except Exception as exc:
        print(
            f"Unexpected exception raised while getting movie predictions: {exc}")
        return "Error: " + str(exc)


@app.route("/")
def welcome_return():
    return {"Welcome": "This is the {name} API".format(name="stable" if str(os.environ['PORT']) == "5000" else "canary")}


# define predict endpoint
@app.route('/recommend/<userid>')
def recommend_route(userid):
    if not userid.isdigit():
        return "Error: Invalid user id"
    return predict_movies(int(userid))


if __name__ == '__main__':
    app.run(port=os.environ['PORT'])

# run the file using python3 app.py
