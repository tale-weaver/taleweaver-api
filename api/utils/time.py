from datetime import datetime, timedelta


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_time_intervals(now_time, interval, num):
    list_time = []
    now_time = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    list_time.append(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    for _ in range(num - 1):
        now_time = now_time + timedelta(seconds=interval)
        list_time.append(now_time.strftime('%Y-%m-%d %H:%M:%S'))
    return list_time
