import os

import numpy as np
from matplotlib import pyplot as plt
from app.model.movie_rec import load_dataset_from_csv

os.chdir("../")
CURR = os.getcwd()

DATA_PATH = os.path.join(CURR, 'app', 'data')
FILE_NAME_USERS = 'user_data.csv'
FILE_NAME_RATINGS = 'cleaned_rating.csv'
FILE_NAME_MOVIES = 'filtered_responses.csv'
RESULT_PATH = os.path.join(CURR, 'app', 'fairness_feedbackloop_analysis', 'results')


# In the users dataset

def users_value_counts(label, by_labels_value):
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    for lab, value in by_labels_value:
        data = data[data[lab] == value]
    value_count = data[label].value_counts()
    return value_count


def users_gender_balance():
    return users_value_counts('gender', [])


def users_age_balance():
    return users_value_counts('age', [])


def users_age_balance_by_gender(gender):
    return users_value_counts('age', [('gender', gender)])


def users_occupation_balance():
    return users_value_counts('occupation', [])


def users_occupation_balance_by_gender(gender):
    return users_value_counts('occupation', [('gender', gender)])


def users_occupation_balance_by_age(age):
    return users_value_counts('occupation', [('age', age)])


def users_occupation_balance_by_gender_age(gender, age):
    return users_value_counts('occupation', [('gender', gender), ('age', age)])


# In the ratings dataset

def ratings_value_counts(label, by_labels_value):
    users = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    ratings = load_dataset_from_csv(DATA_PATH, FILE_NAME_RATINGS, ['user_id', 'movie_id', 'rate'])
    data = ratings.merge(users, on='user_id')
    data = data.drop(columns=['movie_id'])
    for lab, value in by_labels_value:
        data = data[data[lab] == value]
    value_count = data[label].value_counts()
    return value_count


def ratings_gender_balance():
    return ratings_value_counts('gender', [])


def ratings_age_balance():
    return ratings_value_counts('age', [])


def ratings_age_balance_by_gender(gender):
    return ratings_value_counts('age', [('gender', gender)])


def ratings_occupation_balance():
    return ratings_value_counts('occupation', [])


def ratings_occupation_balance_by_gender(gender):
    return ratings_value_counts('occupation', [('gender', gender)])


def ratings_occupation_balance_by_age(age):
    return ratings_value_counts('occupation', [('age', age)])


def ratings_occupation_balance_by_gender_age(gender, age):
    return ratings_value_counts('occupation', [('gender', gender), ('age', age)])


def ratings():
    return ratings_value_counts('rate', [])


def ratings_by_gender(gender):
    return ratings_value_counts('rate', [('gender', gender)])


def ratings_by_age(age):
    return ratings_value_counts('rate', [('age', age)])


def ratings_by_gender_age(gender, age):
    return ratings_value_counts('rate', [('gender', gender), ('age', age)])


# Write the result in a csv file

def write_csv(data, file_name):
    # data is a value_count
    data.to_csv(os.path.join(RESULT_PATH, file_name))


def write_age_balance():
    labels = get_labels('gender')
    value_count = users_age_balance().reset_index()
    for label in labels:
        value_count_c = users_age_balance_by_gender(label).reset_index()
        value_count = value_count.merge(value_count_c, on='index')
    write_csv(value_count, 'users_age_balance.csv')


def write_age_balance_ratings():
    labels = get_labels('gender')
    value_count = ratings_age_balance().reset_index()
    for label in labels:
        value_count_c = ratings_age_balance_by_gender(label).reset_index()
        value_count = value_count.merge(value_count_c, on='index')
    write_csv(value_count, 'ratings_age_balance.csv')



def write_occupation_balance():
    list_labels = []
    labels_gender = get_labels('gender')
    value_count = users_occupation_balance().reset_index()
    for label in labels_gender:
        list_labels.append(label)
        value_count_c = users_occupation_balance_by_gender(label).reset_index()
        value_count = value_count.merge(value_count_c, on='index', how='outer')
    labels_age = get_labels('age')
    for label in labels_age:
        list_labels.append(label)
        value_count_c = users_occupation_balance_by_age(label).reset_index()
        if len(value_count_c) > 0:
            value_count = value_count.merge(value_count_c, on='index', how='outer')
    for label1 in labels_age:
        for label2 in labels_gender:
            list_labels.append(f'{label1}_{label2}')
            value_count_c = users_occupation_balance_by_gender_age(label2, label1).reset_index()
            if len(value_count_c) > 0:
                value_count = value_count.merge(value_count_c, on='index', how='outer')
    write_csv(value_count.fillna(0), 'users_occupation_balance.csv')
    print(list_labels)


# Other functions

def percentage(x):
    return x / float(x.sum()) * 100


def gender_difference_users_ratings():
    gender = ("M", "F")
    dataset_type = {
        'Users data': percentage(users_age_balance().values),
        'Ratings data': percentage(ratings_gender_balance().values),
    }

    x = np.arange(len(gender))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in dataset_type.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title('Gender balance in the datasets')
    ax.set_xticks(x + width / 2, gender)
    ax.set_ylabel('percentage of each gender')
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 100)

    plt.show()


def age_gender_difference_users():
    value_count = users_age_balance()
    value_count = value_count.sort_index()
    value_count_women = users_age_balance_by_gender('F')
    value_count_women = value_count_women.sort_index()
    value_count_men = users_age_balance_by_gender('M')
    value_count_men = value_count_men.sort_index()

    age = (value_count.index.tolist())
    age = age
    gender = {
        'Both': percentage(value_count.values),
        'Men': percentage(value_count_men.values),
        'Women': percentage(value_count_women.values),
    }

    x = np.arange(len(age))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in gender.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title('Age balance')
    ax.set_xticks(x + width, age)
    ax.set_ylabel('percentage of users')
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, 10)

    # resize the figure
    fig.set_size_inches(14.5, 5.5)

    plt.show()


def age_gender():
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    data_women = data[data['gender'] == 'F']
    mean_f = data_women['age'].mean()
    print(mean_f)
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    data_women = data[data['gender'] == 'M']
    mean_f = data_women['age'].mean()
    print(mean_f)


def get_labels(column_name):
    data = load_dataset_from_csv(DATA_PATH, FILE_NAME_USERS, ['user_id', 'age', 'occupation', 'gender'])
    return data[column_name].unique().tolist()


if __name__ == '__main__':
    write_age_balance_ratings()

