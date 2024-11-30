import calendar

def display_calendar():

    year = int(input("Entre year: "))
    month = int(input("Entre month (1-12): "))

    cal = calendar.TextCalendar(calendar.SUNDAY)

    month_calendar = cal.formatmonth(year, month)
    print(month_calendar)

display_calendar()
