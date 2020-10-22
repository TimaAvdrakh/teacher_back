import datetime


def next_weekday(d, weekday):
    """Function to find next given day after given day"""
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + dtm.timedelta(days_ahead)