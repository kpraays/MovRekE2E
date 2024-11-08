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
FILE_NAME_MOVIES = 'filtered_responses.csv'
RESULT_PATH = os.path.join(CURR, 'app', 'fairness_feedbackloop_analysis', 'results')


def get_labels(column_name):
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    return data[column_name].unique().tolist()


def gender_rmse():
    return test_collaborative_filtering_subset('gender', get_labels('gender'))


def age_rmse():
    return test_collaborative_filtering_subset('age', get_labels('age'))


def occupation_rmse():
    return test_collaborative_filtering_subset('occupation', get_labels('occupation'))


def write_csv(data, file_name):
    # dict to array of arrays
    data = np.array([[k, v] for k, v in data.items()])
    # switch axis
    #data = np.swapaxes(data, 0, 1)
    # create dataframe
    data = DataFrame(data, columns=['label', 'rmse'])
    data.to_csv(os.path.join(RESULT_PATH, file_name))


if __name__ == '__main__':
    train(data_path=DATA_PATH, file_name_users=FILE_NAME_USERS, file_name_movies=FILE_NAME_MOVIES,
          file_name_ratings=FILE_NAME_RATINGS, model_path=MODEL_PATH)
    write_csv(occupation_rmse(), 'occupation_rmse.csv')
