import random
import re
import requests
import time
import json
import math
import csv
from loki_scraper import date_to_unix_timestamp, fetch_logs_latest

def is_alnum_plus(input_string):
    pattern = r"^[a-zA-Z0-9+]+$"
    if re.match(pattern, input_string):
        return True
    else:
        return False

def valid_movie(movie_name):
    res = requests.get(f"http://fall2023-comp585.cs.mcgill.ca:8080/movie/{movie_name}")
    if res.status_code == 200:
        return True
    else:
        False

def get_history_logs():
    # pick the data from history view
    history_logs = fetch_logs_latest("history")
    # this is how the history logs look like
    # ['1698617051405637915', '2023-10-29T18:04:11,481542,ptu+2003,88']

    movie_details = []
    for _ in history_logs:
        sample = []
        sample.extend(_[1].split(","))
        movie_details.append(sample)

    return movie_details

def get_userid_movies():
    rating_logs = fetch_logs_latest("rating")
    userid_movies = []
    for _ in rating_logs:
        ['1698613915052791561', '2023-10-29T17:11:55,261281,the+lord+of+the+rings+the+two+towers+2002,5']
        sample = []
        sample.append(_[1].split(",")[1])
        sample.append(_[1].split(",")[2])
        sample.append(_[1].split(",")[3])
        userid_movies.append(sample)
    return userid_movies

def rating_evaluation(userid, movie, rating):
    try:
        score = -1
        recommendation = requests.get(f"http://fall2023-comp585-4.cs.mcgill.ca:8082/recommend/{userid}")
        movies_list = str(recommendation.text).split(",")
        rating = float(rating)
        
        if movie in movies_list:
            movie_index = movies_list.index(movie)
            if 0 <= movie_index <= 5:
                score = 1 * (rating/5.0)

            elif 6 <= movie_index <= 10:
                score = 0.8 * (rating/5.0)

            elif 11 <= movie_index <= 15:
                score = 0.5 * (rating/5.0)

            elif 16 <= movie_index < 20:
                score = 0.3 * (rating/5.0)

        else:
            # item not in the recommendation
            score = 0.1 * (rating/5.0)

        return round(score,2), math.floor(recommendation.elapsed.total_seconds()*1000)

    except Exception as exc:
        print(f"Exception occurred: {exc}")



if __name__ == "__main__":

    rating_score = 0
    runtime_score = 0
    recommendation_score = 0

    pick_rating = False
    pick_watchtime = False

    movie_ratings = "default"
    userid_ratings = "default"
    rating = "default"

    movie_watchtime = "default"
    userid_watchtime = "default"
    watchtime = "default"

    while True:
        # run it forever as daemon.

        while not pick_rating:
            # pick the data from rating view

            userid_movies = get_userid_movies()
            index = random.randint(0, len(userid_movies))

            # [userid, movie_name, rating]
            # print(userid_movies[index])
            # len(userid_movies[index]) == 3

            if is_alnum_plus(userid_movies[index][1]) and valid_movie(userid_movies[index][1]):
                userid_ratings = userid_movies[index][0]
                movie_ratings = userid_movies[index][1]
                rating = userid_movies[index][2]
                pick_rating = True
                # print(f"userid_ratings:{userid_ratings}, movie_ratings:{movie_ratings}, rating:{rating}")

        # score, response_time = rating_evaluation(userid_ratings, movie_ratings, rating)
        # print(score, response_time)
        csv_file_path = "ratings_eval.csv"
        with open(csv_file_path, 'a', newline='') as csvfile:
            
            csv_writer = csv.writer(csvfile)
            score, response_time = rating_evaluation(userid_ratings, movie_ratings, rating)
            csv_writer.writerow([score, response_time])
            
        pick_rating = False        
        time.sleep(1)

    




        