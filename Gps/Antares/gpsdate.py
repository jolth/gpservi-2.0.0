#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 http://www.leapsecond.com/tools/gpsdate.c
 Simple tool to convert GPS time and calendar dates.

 Return Modified Julian Day given calendar year,
 month (1-12), and day (1-31).
  - Valid for Gregorian dates from 17-Nov-1858.
  - Adapted from sci.astro FAQ.

Usage:
      >>> import gpsdate
      >>> mjd = gpsdate.GpsToMjd(1735, 81769)
      >>> gpsdate.MjdToDate(mjd, 1980, 1, 6)
      (2013, 4, 7)
      >>> 

"""

def DateToMjd(year, month, day):
    """
        >>> import gpsdate
        >>> gpsdate.DateToMjd(1980, 1, 6)
        44244
        >>> 
    """
    return 367 * year \
        - 7 * (year + (month + 9) / 12) / 4 \
        - 3 * ((year + (month - 9) / 7) / 100 + 1) / 4 \
        + 275 * month / 9 \
        + day \
        + 1721028 \
        - 2400000


# Convert Modified Julian Day to calendar date.
# - Assumes Gregorian calendar.
# - Adapted from Fliegel/van Flandern ACM 11/#10 p 657 Oct 1968.
def MjdToDate(mjd, year, month, day):
    """
        mar abr  9 21:41:49 COT 2013

        >>> import gpsdate
        >>> mjd = gpsdate.GpsToMjd(1735, 81769)
        >>> gpsdate.MjdToDate(mjd, 1980, 1, 6)
        (2013, 4, 7)
        >>> 
    """
    J = mjd + 2400001 + 68569;
    C = 4 * J / 146097;
    J = J - (146097 * C + 3) / 4;
    Y = 4000 * (J + 1) / 1461001;
    J = J - 1461 * Y / 4 + 31;
    M = 80 * J / 2447;
    day = J - 2447 * M / 80;
    J = M / 11;
    month = M + 2 - (12 * J);
    year = 100 * (C - 49) + Y + J;
    return (year, month, day)



# Convert GPS Week and Seconds to Modified Julian Day.
# Ignores UTC leap seconds.
#def GpsToMjd(GpsCycle, GpsWeek, GpsSeconds) 
def GpsToMjd(gpsWeek, gpsSeconds):
    """
        >>> import gpsdate
        >>> gpsdate.GpsToMjd(1735, 81769)
        56389
        >>> 
    """
    #gpsDays = ((gpsCycle * 1024) + gpsWeek) * 7 + (gpsSeconds / 86400);
    gpsCycle = 0 # Jan 6 1980
    gpsDays = ((gpsCycle * 1024) + gpsWeek) * 7 + (gpsSeconds / 86400);
    return DateToMjd(1980, 1, 6) + gpsDays;
    #return DateToMjd(1980, 1, 8) + gpsDays; # Trampa




