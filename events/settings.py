# -*- coding: utf-8 -*-
import datetime
from datetime import time, timedelta
from django.conf import settings

MAX_SIZE_CHOICES = ( (x,str(x)) for x in range(1,16))
INITIAL_SIZE_CHOICES = ( (x,str(x)) for x in range(1,16))
BOOKING_TOMORROW = datetime.date.today() + datetime.timedelta(days=1)

# The below was copied from the guild.house Booking app:

# IMPORTANT SETTINGS! Actual booking range.
BOOKING_TIMES = (time(12), time(21))
BOOKING_INTERVAL = timedelta(minutes=30)

def generate_times():
    temp_date, time_list = datetime.date(2000, 1, 1), []
    this_time = BOOKING_TIMES[0]
    while this_time <= BOOKING_TIMES[1]:

        # Choice fields values need the seconds portion, but this
        # is omitted for the displayed time

        this_time_display_label = "{}:{:0>2}".format(
            this_time.hour, this_time.minute)
        this_time_actual_value = this_time_display_label + ":00"
        time_list.append((this_time_actual_value, this_time_display_label))

        # hack around timedelta not allowing time addition (on purpose)
        # http://bugs.python.org/issue1487389
        # http://bugs.python.org/issue1118748
        temp_time = datetime.datetime.combine(
            temp_date, this_time) + BOOKING_INTERVAL
        this_time = time(temp_time.hour, temp_time.minute)
    return time_list

BOOKING_TIMES_CHOICES = generate_times()
LOGIN_REDIRECT_URL = 'events'