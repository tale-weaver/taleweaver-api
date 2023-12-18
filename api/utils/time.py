from datetime import datetime, timedelta
from api.config.config import Config


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


def _find_surrounding_datetime_indices(datetimes):
    datetimes.sort()

    current_datetime = datetime.now()

    if current_datetime < datetimes[0]:
        raise ValueError(
            "Current time is before the first datetime in the list.")

    if current_datetime > datetimes[-1]:
        return len(datetimes) - 1, len(datetimes) - 1

    for i in range(len(datetimes) - 1):
        if datetimes[i] <= current_datetime <= datetimes[i + 1]:
            return i, i + 1


def find_surrounding_datetime_indices(datetime_strings):
    try:
        datetimes = [datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                     for dt_str in datetime_strings]
        surrounding_indices = _find_surrounding_datetime_indices(datetimes)
        return surrounding_indices
    except ValueError as e:
        print(e)
