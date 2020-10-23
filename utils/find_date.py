import datetime


def find_date(date):
    """ Функция для преврощения даты в день"""
    day, month, year = (int(i) for i in date.split('/'))
    date = datetime.datetime(year, month, day)
    print(date)
    wd = date.weekday()
    return wd+1
