from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import accuracy
import pandas as pd
import numpy as np
import pickle
import os

os.chdir("../")
CURR = os.getcwd()

MODEL_PATH = os.path.join(CURR, '..', 'model', 'model.pkl')
DATA_PATH = os.path.join(CURR, '..', 'data')

FILE_NAME_USERS = 'user_data.csv'
FILE_NAME_RATINGS = 'cleaned_rating.csv'
FILE_NAME_MOVIES = 'filtered_responses.csv'

global_model = None
global_users = None
global_dataset = None
global_users_ratings = None
global_movies = None
global_test_set = None


def column_switch(column):
    if column['max_min'] != 0:
        return (column['min'] * 100) // column['max_min']
    return 0


def load_dataset_from_csv(folder_path, file_name, columns):
    """
    Load a specific dataset from a CSV file

    :param folder_path: the path of the folder where the dataset is
    :param file_name: the name of the file where the dataset is
    :param columns: the list of the names of all the columns in the dataset
    :return: the panda dataset
    """
    dataset = pd.read_csv(os.path.join(folder_path, file_name),
                          sep=',', encoding="latin-1")
    dataset.columns = columns
    return dataset


def load_data(folder_path, file_name_ratings=FILE_NAME_RATINGS, file_name_movies=FILE_NAME_MOVIES,
              file_name_users=FILE_NAME_USERS):
    """
    Load the data and prepare them for the training.

    :param folder_path: The path of the folder containing all the csv files with the data.
    :param file_name_ratings: The name of the file containing the ratings of the users.
    :param file_name_movies: The name of the file containing the movies.
    :param file_name_users: The name of the file containing the users.
    :return: the dataset for the collaborative filtering, the database of the users, the database with the user and the
    ratings, and the database with the movies.
    """

    global global_users
    global global_dataset
    global global_users_ratings
    global global_movies

    # Load the users database
    global_users = load_dataset_from_csv(folder_path, file_name_users, ['user_id', 'age', 'occupation', 'gender'])

    # Load the ratings database
    ratings = load_dataset_from_csv(folder_path, file_name_ratings, ['user_id', 'movie_id', 'rate'])

    # Create a database with users and ratings
    global_users_ratings = pd.merge(ratings, global_users, on='user_id')

    # Load the movies database and sort it
    global_movies = load_dataset_from_csv(folder_path, file_name_movies, ['movie_id', 'adult', 'type', 'max_min',
                                                                          'global_rate', 'languages'])
    global_movies.sort_values(by=['global_rate'], ascending=False)

    # Create the Dataset for the collaborative filtering
    reader = Reader(line_format='user item rating',
                    sep=',', rating_scale=(1, 5))
    global_dataset = Dataset.load_from_df(ratings, reader=reader)

    return global_dataset, global_users, global_users_ratings, global_movies


def train_collaborative_filtering(train_set, model_path=MODEL_PATH):
    """
    Train the model with the train dataset

    :param train_set: The train dataset
    :param model_path: The path where the model will be saved
    :return: the model
    """

    # Create the model
    model = SVD()

    # Train the model on the training data
    model.fit(train_set)

    # save
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    return model


def test_collaborative_filtering():
    """
    Test of the collaborative filtering
    """

    assert global_model is not None
    assert global_test_set is not None

    # Make predictions on the test set
    predictions = global_model.test(global_test_set)

    # Evaluate the model's performance using RMSE (Root Mean Squared Error)
    return accuracy.rmse(predictions)


def test_collaborative_filtering_subset(subset_label, subset_values):
    """
    Test of the collaborative filtering for a subset of the user set
    """

    assert global_model is not None
    assert global_test_set is not None

    test_set = global_test_set
    users_df = global_users

    # transform the test set to a dataframe
    test_set_df = pd.DataFrame(test_set, columns=['user_id', 'movie_id', 'rate'])

    # merge the test set with the users dataframe
    test_set_df = pd.merge(test_set_df, users_df, on='user_id')

    dict_rmse = {}

    for value in subset_values:
        new_test_set = test_set_df[test_set_df[subset_label] == value]
        new_test_set = new_test_set[['user_id', 'movie_id', 'rate']]
        new_test_set = new_test_set.values.tolist()
        predictions = global_model.test(new_test_set)
        if len(predictions) != 0:
            dict_rmse[value] = accuracy.rmse(predictions)

    return dict_rmse


def recommendation(user_id, nb_recommendation):
    """
    Recommend a list of movies for a user based on collaborative filtering or demographic filtering when there are
    not enough data.

    :param user_id: The user id to make the prediction
    :param nb_recommendation: The number of recommendation asked
    :exception: The user have to exist in the database
    """

    assert global_model is not None
    assert global_movies is not None
    assert global_users is not None
    assert global_dataset is not None
    assert global_users_ratings is not None

    # Get the array of the movies already rates by the user
    user_ratings_arr = np.array(list(map(lambda x: x[1], filter(
        lambda x: x[0] == user_id, global_dataset.raw_ratings))))

    max_nb_movies = 100

    # Get the array of all the movies
    movies_arr = np.array(global_movies)[:max_nb_movies, 0]

    # Create an array with all the movies not seen yet by the user
    movies_not_seen = np.setdiff1d(movies_arr, user_ratings_arr)

    # Get the user entry in the database of all users
    user_row = global_users.loc[global_users['user_id'] == int(user_id)]
    assert len(user_row) > 0, 'The user does not exist in the users database'

    # Get the user gender ('F' or 'M')
    user_gender = user_row['gender'].values[0]

    # Get the user age
    user_age = user_row['age'].values[0]

    movie_recommendations = []
    for movie_id in movies_not_seen:

        # Get the movie entry in the database of all movies
        movie_entry = global_movies.loc[global_movies['movie_id'] == movie_id]

        # Filter to do not recommend adult movie to a kid
        if (True in movie_entry['adult'].values) and user_age < 18:
            movie_recommendations.append((movie_id, 0))
        else:
            # prediction of the collaborative filtering model
            prediction = global_model.predict(user_id, movie_id)

            # Test if the collaborative filtering prediction is not possible.
            # The prediction can be impossible if the user or the movie is new or have too few ratings (cold start)
            # If the prediction is not possible, do a demographic-based filtering.
            if prediction.details['was_impossible']:

                # Rate of the movie
                global_rate = movie_entry['global_rate'].values

                # If there are no global rate, give the default prediction
                if len(global_rate) == 0:
                    global_rate = global_model.default_prediction()
                else:
                    global_rate = global_rate[0]

                # Take all the ratings done by a user of the same gender
                users_same_movie = global_users_ratings.loc[global_users_ratings['movie_id'] == movie_id]
                users_same_gender = users_same_movie.loc[users_same_movie['gender'] == user_gender]

                # If at least one person of the same gender have rate the movie, consider it in the prediction
                if len(users_same_gender) == 0:
                    movie_recommendations.append(
                        (movie_id, (global_rate / 10) * 5))
                else:
                    predicted_rating = ((global_rate / 10) * 5 + users_same_gender.mean(axis=0, numeric_only=True)[
                        'rate']) / 2
                    movie_recommendations.append((movie_id, predicted_rating))
            else:
                # If the prediction is possible, use the collaborative filtering model
                predicted_rating = prediction.est
                movie_recommendations.append((movie_id, predicted_rating))

    # Sort the recommendations by predicted rating in descending order
    movie_recommendations.sort(key=lambda x: x[1], reverse=True)

    # Get the top N movie recommendations
    top_movie_recommendations = movie_recommendations[:nb_recommendation]

    return top_movie_recommendations


def print_recommendations(top_movie_recommendations, user_id):
    """
    Utility function to print the recommendation for a user.

    :param top_movie_recommendations: recommendations made by the recommender system
    :param user_id: The id of the user
    :return the string output
    """

    output = f'Top {len(top_movie_recommendations)} Movie Recommendations for User {user_id}:'
    for movie_id, predicted_rating in top_movie_recommendations:
        output += '\n'
        output += f'Movie ID: {movie_id}, Predicted Rating: {predicted_rating:.2f}'
    print(output)
    return output


def train(data_path=DATA_PATH, file_name_ratings=FILE_NAME_RATINGS, file_name_movies=FILE_NAME_MOVIES,
          file_name_users=FILE_NAME_USERS, model_path=MODEL_PATH):
    """
    Train the model and save it in a file.

    :param data_path: The path where the data are
    :param file_name_ratings: The name of the file containing the ratings of the users.
    :param file_name_movies: The name of the file containing the movies.
    :param file_name_users: The name of the file containing the users.
    :param model_path: The path where the model will be saved
    """

    global global_model
    global global_test_set

    # Load the dataset using Surprise
    dataset, users, users_ratings, movies = load_data(data_path, file_name_users=file_name_users,
                                                      file_name_movies=file_name_movies,
                                                      file_name_ratings=file_name_ratings)

    # Split the dataset into a train set and a test set (20% test, 80% train)
    train_set, global_test_set = train_test_split(
        dataset, test_size=0.2, random_state=42)

    # Training
    global_model = train_collaborative_filtering(train_set, model_path=model_path)


def get_recommendation(user_id):
    """
    Get the recommendation for a user

    :param user_id: the id of the user
    """

    # Get movie recommendations for a user
    nb_recommendation = 20
    try:
        recommendations = recommendation(
            user_id, nb_recommendation)
    except Exception as exc:
        print(f"Error occurred while getting recommendations: {exc}")

    try:
        print_recommendations(recommendations, user_id)
    except Exception as exc:
        print(f"Error occurred while printing recommendations: {exc}")

    return [x[0] for x in recommendations]


def load_model(model_path=MODEL_PATH, data_path=DATA_PATH, file_name_ratings=FILE_NAME_RATINGS,
               file_name_movies=FILE_NAME_MOVIES, file_name_users=FILE_NAME_USERS):
    global global_model
    file_path = model_path

    # load the model
    with open(file_path, 'rb') as f:
        global_model = pickle.load(f)

    # load the data
    load_data(data_path, file_name_users=file_name_users, file_name_movies=file_name_movies,
              file_name_ratings=file_name_ratings)
