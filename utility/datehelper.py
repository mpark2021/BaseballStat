from datetime import date, timedelta

def next(today):
    [yr, m, dt] = map(int, today.split("-"))
    d = date(yr, m, dt)
    d = d + timedelta(days=1)

    return str(d)