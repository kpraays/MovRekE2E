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

def history_evaluation(userid, movie, watchtime):
    try:
        score = -1
        recommendation = requests.get(f"http://fall2023-comp585-4.cs.mcgill.ca:8082/recommend/{userid}")
        movies_list = str(recommendation.text).split(",")
        watchtime = float(watchtime)

        movie_attributes = requests.get(f"http://fall2023-comp585.cs.mcgill.ca:8080/movie/{movie}")
        runtime = int(movie_attributes.json()["runtime"])
        proportion = watchtime/runtime
        proportion_score = -1

        if 0 <= proportion < 0.2:
            proportion_score = 0.2
        elif 0.2 <= proportion < 0.5:
            proportion_score = 0.6
        elif 0.5<= proportion < 0.7:
            proportion_score = 0.8
        elif 0.7<=proportion <=1:
            proportion_score = 1.0

        if movie in movies_list:
            movie_index = movies_list.index(movie)
            if 0 <= movie_index <= 5:
                score = 1 * proportion_score

            elif 6 <= movie_index <= 10:
                score = 0.8 * proportion_score

            elif 11 <= movie_index <= 15:
                score = 0.5 * proportion_score

            elif 16 <= movie_index < 20:
                score = 0.3 * proportion_score
        
        else:
            # item not in the recommendation
            score = 0.1 * proportion_score

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
        while not pick_watchtime:
            # pick the data from history view

            movie_details = get_history_logs()
            index = random.randint(0, len(movie_details))

            # ['2023-10-29T18:53:27', '278549', 'forrest+gump+1994', '75']
            # print(movie_details[index])

            if is_alnum_plus(movie_details[index][2]) and valid_movie(movie_details[index][2]):
                userid_watchtime = movie_details[index][1]
                movie_watchtime = movie_details[index][2]
                watchtime = movie_details[index][3]
                pick_watchtime = True
                # print(f"userid_watchtime is:{userid_watchtime}, movie is:{movie_watchtime}, watchtime is:{watchtime}")

        # print(history_evaluation(userid_watchtime, movie_watchtime, watchtime))
        csv_file_path = "history_eval.csv"
        with open(csv_file_path, 'a', newline='') as csvfile:
            
            csv_writer = csv.writer(csvfile)
            score, response_time = history_evaluation(userid_watchtime, movie_watchtime, watchtime)
            csv_writer.writerow([score, response_time])
            
        pick_watchtime = False        

    




        