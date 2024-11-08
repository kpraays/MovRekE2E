import requests
import urllib.parse
import time
import datetime
import csv
import os

BASE_URL = "http://fall2023-comp585-4.cs.mcgill.ca:3100/loki/api/v1"
CSV_HEADER = {
    'history': ['timestamp', 'userid', 'movieid', 'minute_watched'],
    'rating': ['timestamp', 'userid', 'movieid', 'rating'],
    'error': ['timestamp', 'userid', 'error', 'message', 'response_time(ms)']
}


def date_to_unix_timestamp(date_str):
    """
    Converts a date string in the format yyyy-mm-dd to Unix timestamp.

    :param date_str (str): The date string to convert.
    :return (int): The Unix timestamp corresponding to the input date string.
    """
    return int(time.mktime(time.strptime(date_str, '%Y-%m-%d')))


def fetch_logs_latest(type, limit=5000):
    """
    Fetches the latest logs of a given type from a remote server.

    :param type (str): The type of logs to fetch. Value can be history, rating or error
    :param limit (int): The number of logs to fetch. Defaults to maximum limit 5000.
    :return (str): a list of the n latest logs from the Kafka stream at the time of calling the API. each array item is in the following format based on type
                   history: (timestamp, userid, movieid, minute of movie watched)
                   rating: (timestamp, userid, movieid, rating)
                   error: (timestamp, userid, error, message, response time)
    """
    try:
        if limit > 5000:
            raise Exception(
                f"Given limit exceeds maximum limit ({limit} > 5000)")
        data = {'query': '{type="' + type + '"}', 'limit': limit}
        encoded_data = urllib.parse.urlencode(data)
        res = requests.get(BASE_URL + "/query?" + encoded_data)
        logs = filter(
            lambda x: 'no value' not in x[1], res.json()['data']['result'][0]['values'])
        return logs
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"{err}\nPlease try again with a smaller limit")
    except Exception as err:
        raise SystemExit(err)


def fetch_logs_range(type, start_date, end_date=str(datetime.date.today())):
    """
    Fetches the latest logs of a given type from a remote server.

    :param type (str): The type of logs to fetch. Value can be history, rating or error
    :param start_date (string): The start date of the logs to fetch in the format yyyy-mm-dd.
    :param end_date (string): The end date of the logs to fetch in the format yyyy-mm-dd. Defaults to today.
    :return (str): a list of the n latest logs from the Kafka stream at the time of calling the API. each array item is in the following format based on type
                   history: (timestamp, userid, movieid, minute of movie watched)
                   rating: (timestamp, userid, movieid, rating)
                   error: (timestamp, userid, error, message, response time)
    """
    try:
        print(date_to_unix_timestamp(start_date),
              date_to_unix_timestamp(end_date))
        data = {'query': '{type="' + type + '"}', 'limit': 5000,
                'start': date_to_unix_timestamp(start_date), 'end': date_to_unix_timestamp(end_date)}
        encoded_data = urllib.parse.urlencode(data)
        res = requests.get(BASE_URL + "/query_range?" + encoded_data)
        print(res.json()['data']['result'])
        logs = filter(
            lambda x: '<no value>' in x, res.json()['data']['result'][0]['values'])
        return logs
    except requests.exceptions.RequestException as err:
        raise SystemExit(f"{err}\nPlease try again with a smaller limit")


def save_logs_latest_to_csv(type, limit=5000):
    """
    Fetches the latest logs of a given type from a remote server and saves them to a CSV file.

    :param type (str): The type of logs to fetch. Value can be history, rating or error
    :param limit (int): The number of logs to fetch. Defaults to maximum limit 5000.
    :param filename (str): The name of the CSV file to save the logs to. Defaults to 'logs_latest.csv'.
    """
    try:
        logs = fetch_logs_latest(type, limit)
        if logs:
            with open(os.path.join('app', 'data', f'logs-{type}-{int(time.time())}.csv'), mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(CSV_HEADER[type])
                for log in logs:
                    writer.writerow(log[:1] + log[1].split(','))
    except Exception as err:
        print(f"Unable to create CSV file\n{err}")


def save_logs_range_to_csv(type, start_date, end_date=str(datetime.date.today())):
    """
    Fetches the logs of a given type within a date range from a remote server and saves them to a CSV file.

    :param type (str): The type of logs to fetch. Value can be history, rating or error
    :param start_date (string): The start date of the logs to fetch in the format yyyy-mm-dd.
    :param end_date (string): The end date of the logs to fetch in the format yyyy-mm-dd. Defaults to today.
    :param filename (str): The name of the CSV file to save the logs to. Defaults to 'logs_range.csv'.
    """
    logs = fetch_logs_range(type, start_date, end_date)
    if logs:
        with open(os.path.join('app', 'data', f'logs-{type}-{int(time.time())}.csv'), mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER[type])
            for log in logs:
                writer.writerow(log[:1] + log[1].split(','))


save_logs_latest_to_csv('history')
