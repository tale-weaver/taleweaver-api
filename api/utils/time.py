from datetime import datetime, timedelta
from api.config.config import Config
import random

random.seed(int(datetime.now().timestamp()))


def now(seconds=0):
    return (datetime.now() + timedelta(seconds=seconds)).strftime('%Y-%m-%d %H:%M:%S')


def create_time_intervals(start_time, interval=Config.INTERVAL_TIME, num=8):
    list_time = []
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    for i in range(num*2):
        if i % 2 == 0:
            list_time.append({
                "time_stamp": start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "round": int(i / 2) + 1,
                "status": "submitting"
            })
        else:
            list_time.append({
                "time_stamp": start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "round": int(i / 2) + 1,
                "status": "voting"
            })
        start_time = start_time + timedelta(seconds=interval)

    list_time.append({
        "time_stamp": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "round": num,
        "status": "finished"
    })

    return list_time


def _find_surrounding_datetime_indices(datetimes, current_datetime):
    datetimes.sort()

    if current_datetime < datetimes[0]:
        raise ValueError(
            "Current time is before the first datetime in the list.")

    if current_datetime > datetimes[-1]:
        return len(datetimes) - 1, len(datetimes) - 1

    for i in range(len(datetimes) - 1):
        if datetimes[i] <= current_datetime <= datetimes[i + 1]:
            return i, i + 1


def find_surrounding_datetime_indices(datetime_strings, inspect_time):
    try:
        datetimes = [datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                     for dt_str in datetime_strings]
        current_datetime = datetime.strptime(inspect_time, '%Y-%m-%d %H:%M:%S')

        surrounding_indices = _find_surrounding_datetime_indices(
            datetimes, current_datetime)
        return surrounding_indices
    except ValueError as e:
        print(e)


def generate_random_time_between_two_times(start_time, end_time):
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

    random_time = start_time + timedelta(seconds=random.randint(
        0, int((end_time - start_time).total_seconds())))
    return random_time.strftime('%Y-%m-%d %H:%M:%S')
