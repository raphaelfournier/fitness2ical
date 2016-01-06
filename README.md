# Fitness2iCal

Fitness2ical is a small script which helps obtain a ical-friendly version of a
human-readable fitness plan. 

## Usage

A sample call would be

    $ python fitness2ical.py > myplan.ics

This generates an icalendar file myplan.ics containing "all day" events for the
appropriate days. It can be easily imported into your favorite calendaring
program (Google Agenda, Apple iCal, etc.). There is a "default plan", called
"halfmarathonIn100min.cfg" which is a plan to prepare for a half-marathon (goal:
under 100 min). Another plan can be used with the --filename parameter, as
follows:

    $ python fitness2ical.py --filename myfile.cfg > myplan.ics

The fitness plan is described in a cfg file. There is a first section, giving
the number of weeks of the plan. Then, for each week, there is an option for
each day, as follows:

[week n]
Monday = "Leg Day"
Friday = "Arm Day"

Days in each week can be omitted. The number of "active" days in a week may vary
between the different weeks in the plan.

To start from a different date, use the --startdate parameter:

    $ python fitness2ical.py --startdate 20160112 > myplan.ics

The format for the start date is YYYYMMDD (four digits for the year, then two
digits each for month and day).

## Acknowledgements

The script was adapted from [shiftical](https://github.com/reinhardt/shiftcal).
The running plan was taken from the book "Semi et marathon, baisser ses
chronos", by Charles Brion (Amphora Editions, Paris, 2014).

