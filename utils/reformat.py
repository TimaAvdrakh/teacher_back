def reformat_date(str):
    "from 20-10-25 to 25/10/20"
    year , month, day = [i for i in str.split('-')]
    return f"{day}/{month}/{year}"