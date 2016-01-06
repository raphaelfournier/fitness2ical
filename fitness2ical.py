import argparse
import os
import re
from ConfigParser import SafeConfigParser
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from icalendar import Calendar, Event
from collections import OrderedDict

weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday",
                "Sunday"]

def findFirstDay(dateInit,firstDayOfPlan):
    date = dateInit
    wd = date.weekday()
    target = weekdays.index(firstDayOfPlan)
    if wd == target:
        return date
    else:
        date += timedelta((target-wd)%7)
        return date

def ajustDate(prev,today):
    a = (weekdays.index(today)-weekdays.index(prev))%7
    return a

def get_runningweeks(config):
    nbweeks = int(config.get('plan', 'weeks'))
    weeks = ["week "+str(x+1) for x in range(nbweeks)]
    plandata = OrderedDict()
    for week in weeks:
        days = [x[0] for x in config.items(week)]
        plandata[week] = OrderedDict()
        for day in days:
            plandata[week][day.capitalize()]=config.get(week,day)
    firstDiW = next(iter(plandata[week]))
    return plandata,firstDiW


class RunningCal(object):
    def __init__(self, start_date, startDay, weeks=[]):
        self.start_date = start_date
        self.startDay = startDay
        self.weeks = weeks

    def get_ical(self):
        cal = Calendar()
        adate = self.start_date
        prevday = self.startDay

        for week in self.weeks:
            for day in self.weeks[week]:
                adate += timedelta(ajustDate(prevday,day))
                prevday=day
                event = Event()
                event.add('dtstart', adate)
                enddate = adate
                event.add('dtend', enddate)
                # remove quotes
                event['summary'] = self.weeks[week][day][1:-1]
                cal.add_component(event)
                #adate += timedelta(1)

        return cal.to_ical()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate ical running calendars')
    parser.add_argument(
        '--startdate',
        type=str,
        help='the start date for the shift plan, in format YYYYMMDD'
        ' or as an offset in days from today, e.g. -1 for yesterday')
    parser.add_argument(
        '--filename',
        type=str,
        help='the name of the fitness plan to use')
    args = parser.parse_args()

    if not args.filename: # default
        filename = 'halfmarathonIn100min.cfg'
    if os.path.exists(filename):
        config = SafeConfigParser()
        config.read(filename)
        runningweeks,firstDiW = get_runningweeks(config)

    today = date.today()
    start_date = today # default
    if args.startdate:
        if args.startdate == 'today':
            start_date = today
        elif re.match(r'[+-][0-9]*$', args.startdate):
            start_date = today + timedelta(int(args.startdate))
        elif re.match(r'[0-9]{8}$', args.startdate):
            start_date = datetime.strptime(args.startdate, '%Y%m%d')
        else:
            print('error: unrecognized startdate format: {0}'.format(
                args.startdate))
            exit(1)

    # we are start_date, we want to start next XXXXsday
    firstDay = findFirstDay(start_date,firstDiW)

    getcal = RunningCal(firstDay, firstDiW, weeks=runningweeks)
    print(getcal.get_ical())
