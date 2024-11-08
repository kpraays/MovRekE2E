import os

import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame

from app.model.movie_rec import test_collaborative_filtering_subset, train, load_dataset_from_csv

os.chdir("../")
CURR = os.getcwd()

MODEL_PATH = os.path.join(CURR, 'app', 'model', 'model.pkl')
DATA_PATH = os.path.join(CURR, 'app', 'data')
FILE_NAME_USERS = 'user_data.csv'
FILE_NAME_RATINGS = 'cleaned_rating.csv'
FILE_NAME_NEW_RATINGS = 'new_ratings.csv'
FILE_NAME_MOVIES = 'filtered_responses.csv'
RESULT_PATH = os.path.join(CURR, 'app', 'fairness_feedbackloop_analysis', 'results')


def mean_rating_by_movie():
    ratings = load_dataset_from_csv(DATA_PATH, FILE_NAME_RATINGS, ['user_id', 'movie_id', 'rate'])
    ratings = ratings.drop(columns=['user_id'])
    ratings = ratings.groupby('movie_id').mean()
    new_ratings = load_dataset_from_csv(DATA_PATH, FILE_NAME_NEW_RATINGS, ['time', 'user_id', 'movie_id', 'rate'])
    new_ratings = new_ratings.drop(columns=['user_id', 'time'])
    new_ratings = new_ratings.groupby('movie_id').mean()
    ratings = ratings.merge(new_ratings, on='movie_id')
    movies = load_dataset_from_csv(DATA_PATH, FILE_NAME_MOVIES, ['movie_id', 'adult', 'type', 'max_min',
                                                                 'global_rate', 'languages'])
    movies = movies.drop(columns=['adult', 'type', 'max_min', 'languages'])
    ratings = ratings.merge(movies, on='movie_id')
    return ratings


if __name__ == '__main__':
    mean_rating_by_movie().to_csv(os.path.join(RESULT_PATH, 'mean_rating_by_movie.csv'))
