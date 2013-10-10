# UTILS/calcSun
"""
*********************
**Module**: utils.calcSun
*********************
This subpackage contains def to calculate sunrise/sunset

This includes the following defs:
    * :func:`utils.calcSun.getJD`:
        calculate the julian date from a python datetime object
    * :func:`utils.calcSun.calcTimeJulianCent`:
        convert Julian Day to centuries since J2000.0.
    * :func:`utils.calcSun.calcGeomMeanLongSun`:
        calculate the Geometric Mean Longitude of the Sun (in degrees)
    * :func:`utils.calcSun.calcGeomMeanAnomalySun`:
        calculate the Geometric Mean Anomaly of the Sun (in degrees)
    * :func:`utils.calcSun.calcEccentricityEarthOrbit`:
        calculate the eccentricity of earth's orbit (unitless)
    * :func:`utils.calcSun.calcSunEqOfCenter`:
        calculate the equation of center for the sun (in degrees)
    * :func:`utils.calcSun.calcSunTrueLong`:
        calculate the true longitude of the sun (in degrees)
    * :func:`utils.calcSun.calcSunTrueAnomaly`:
        calculate the true anamoly of the sun (in degrees)
    * :func:`utils.calcSun.calcSunRadVector`:
        calculate the distance to the sun in AU (in degrees)
    * :func:`utils.calcSun.calcSunApparentLong`:
        calculate the apparent longitude of the sun (in degrees)
    * :func:`utils.calcSun.calcMeanObliquityOfEcliptic`:
        calculate the mean obliquity of the ecliptic (in degrees)
    * :func:`utils.calcSun.calcObliquityCorrection`:
        calculate the corrected obliquity of the ecliptic (in degrees)
    * :func:`utils.calcSun.calcSunRtAscension`:
        calculate the right ascension of the sun (in degrees)
    * :func:`utils.calcSun.calcSunDeclination`:
        calculate the declination of the sun (in degrees)
    * :func:`utils.calcSun.calcEquationOfTime`:
        calculate the difference between true solar time and mean solar time (output: equation of time in minutes of time)
    * :func:`utils.calcSun.calcHourAngleSunrise`:
        calculate the hour angle of the sun at sunrise for the latitude (in radians)
    * :func:`utils.calcSun.calcAzEl`:
        calculate sun azimuth and zenith angle
    * :func:`utils.calcSun.calcSolNoonUTC`:
        calculate time of solar noon the given day at the given location on earth (in minutes since 0 UTC)
    * :func:`utils.calcSun.calcSolNoon`:
        calculate time of solar noon the given day at the given location on earth (in minutes)
    * :func:`utils.calcSun.calcSunRiseSetUTC`:
        calculate sunrise/sunset the given day at the given location on earth (in minutes since 0 UTC)
    * :func:`utils.calcSun.calcSunRiseSet`:
        calculate sunrise/sunset the given day at the given location on earth (in minutes)
    * :func:`utils.calcSun.calcTerminator`:
        calculate terminator position and solar zenith angle for a given julian date-time within latitude/longitude limits
        note that for plotting only, basemap has a built-in terminator

Source: http://www.esrl.noaa.gov/gmd/grad/solcalc/
Translated to Python by Sebastien de Larquier

*******************************
"""
import math
import numpy as np


def calcTimeJulianCent( jd ):
    """
Convert Julian Day to centuries since J2000.0.
    """
    T = (jd - 2451545.0)/36525.0
    return T


def calcGeomMeanLongSun( t ):
    """
Calculate the Geometric Mean Longitude of the Sun (in degrees)
    """
    L0 = 280.46646 + t * ( 36000.76983 + t*0.0003032 )
    while L0 > 360.0:
        L0 -= 360.0
    while L0 < 0.0:
        L0 += 360.0
    return L0 # in degrees


def calcGeomMeanAnomalySun( t ):
    """
Calculate the Geometric Mean Anomaly of the Sun (in degrees)
    """
    M = 357.52911 + t * ( 35999.05029 - 0.0001537 * t)
    return M # in degrees


def calcEccentricityEarthOrbit( t ):
    """
Calculate the eccentricity of earth's orbit (unitless)
    """
    e = 0.016708634 - t * ( 0.000042037 + 0.0000001267 * t)
    return e # unitless


def calcSunEqOfCenter( t ):
    """
Calculate the equation of center for the sun (in degrees)
    """
    mrad = np.radians(calcGeomMeanAnomalySun(t))
    sinm = np.sin(mrad)
    sin2m = np.sin(mrad+mrad)
    sin3m = np.sin(mrad+mrad+mrad)
    C = sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) + sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289
    return C # in degrees


def calcSunTrueLong( t ):
    """
Calculate the true longitude of the sun (in degrees)
    """
    l0 = calcGeomMeanLongSun(t)
    c = calcSunEqOfCenter(t)
    O = l0 + c
    return O # in degrees


def calcSunTrueAnomaly( t ):
    """
Calculate the true anamoly of the sun (in degrees)
    """
    m = calcGeomMeanAnomalySun(t)
    c = calcSunEqOfCenter(t)
    v = m + c
    return v # in degrees


def calcSunRadVector( t ):
    """
Calculate the distance to the sun in AU (in degrees)
    """
    v = calcSunTrueAnomaly(t)
    e = calcEccentricityEarthOrbit(t)
    R = (1.000001018 * (1. - e * e)) / ( 1. + e * np.cos( np.radians(v) ) )
    return R # n AUs


def calcSunApparentLong( t ):
    """
Calculate the apparent longitude of the sun (in degrees)
    """
    o = calcSunTrueLong(t)
    omega = 125.04 - 1934.136 * t
    SunLong = o - 0.00569 - 0.00478 * np.sin(np.radians(omega))
    return SunLong # in degrees


def calcMeanObliquityOfEcliptic( t ):
    """
Calculate the mean obliquity of the ecliptic (in degrees)
    """
    seconds = 21.448 - t*(46.8150 + t*(0.00059 - t*(0.001813)))
    e0 = 23.0 + (26.0 + (seconds/60.0))/60.0
    return e0 # in degrees


def calcObliquityCorrection( t ):
    """
Calculate the corrected obliquity of the ecliptic (in degrees)
    """
    e0 = calcMeanObliquityOfEcliptic(t)
    omega = 125.04 - 1934.136 * t
    e = e0 + 0.00256 * np.cos(np.radians(omega))
    return e # in degrees


def calcSunRtAscension( t ):
    """
Calculate the right ascension of the sun (in degrees)
    """
    e = calcObliquityCorrection(t)
    SunLong = calcSunApparentLong(t)
    tananum = ( np.cos(np.radians(e)) * np.sin(np.radians(SunLong)) )
    tanadenom = np.cos(np.radians(SunLong))
    alpha = np.degrees(np.arctan2(tananum, tanadenom))
    return alpha # in degrees


def calcSunDeclination( t ):
    """
Calculate the declination of the sun (in degrees)
    """
    e = calcObliquityCorrection(t)
    SunLong = calcSunApparentLong(t)
    sint = np.sin(np.radians(e)) * np.sin(np.radians(SunLong))
    theta = np.degrees(np.arcsin(sint))
    return theta # in degrees


def calcEquationOfTime( t ):
    """
Calculate the difference between true solar time and mean solar time (output: equation of time in minutes of time)
    """
    epsilon = calcObliquityCorrection(t)
    l0 = calcGeomMeanLongSun(t)
    e = calcEccentricityEarthOrbit(t)
    m = calcGeomMeanAnomalySun(t)
    y = np.tan(np.radians(epsilon/2.0))
    y *= y

    sin2l0 = np.sin(np.radians(2.0 * l0))
    sinm   = np.sin(np.radians(m))
    cos2l0 = np.cos(np.radians(2.0 * l0))
    sin4l0 = np.sin(np.radians(4.0 * l0))
    sin2m  = np.sin(np.radians(2.0 * m))

    Etime = y * sin2l0 - 2.0 * e * sinm + 4.0 * e * y * sinm * cos2l0 - 0.5 * y * y * sin4l0 - 1.25 * e * e * sin2m
    return np.degrees(Etime*4.0) # in minutes of time


def calcHourAngleSunrise( lat, solarDec ):
    """
Calculate the hour angle of the sun at sunrise for the latitude (in radians)
    """
    latRad = np.radians(lat)
    sdRad  = np.radians(solarDec)
    HAarg = np.cos(np.radians(90.833)) / ( np.cos(latRad)*np.cos(sdRad) ) - np.tan(latRad) * np.tan(sdRad)
    HA = np.arccos(HAarg);
    return HA # in radians (for sunset, use -HA)


def calcAzEl( t, localtime, latitude, longitude, zone ):
    """
Calculate sun azimuth and zenith angle
    """
    eqTime = calcEquationOfTime(t)
    theta  = calcSunDeclination(t)

    solarTimeFix = eqTime + 4.0 * longitude - 60.0 * zone
    earthRadVec = calcSunRadVector(t)

    trueSolarTime = localtime + solarTimeFix
    while trueSolarTime > 1440:
        trueSolarTime -= 1440.

    hourAngle = trueSolarTime / 4.0 - 180.0
    if hourAngle < -180.:
        hourAngle += 360.0

    haRad = np.radians(hourAngle)
    csz = np.sin(np.radians(latitude)) * np.sin(np.radians(theta)) + np.cos(np.radians(latitude)) * np.cos(np.radians(theta)) * np.cos(haRad)
    if csz > 1.0:
        csz = 1.0
    elif csz < -1.0:
        csz = -1.0
    zenith = np.degrees(np.arccos(csz))
    azDenom = np.cos(np.radians(latitude)) * np.sin(np.radians(zenith))
    if abs(azDenom) > 0.001:
        azRad = (( np.sin(np.radians(latitude)) * np.cos(np.radians(zenith)) ) - np.sin(np.radians(theta))) / azDenom
        if abs(azRad) > 1.0:
            if azRad < 0.:
                azRad = -1.0
            else:
                azRad = 1.0

        azimuth = 180.0 - np.degrees(np.arccos(azRad))
        if hourAngle > 0.0:
            azimuth = -azimuth
    else:
        if latitude > 0.0:
            azimuth = 180.0
        else:
            azimuth = 0.0
    if azimuth < 0.0:
        azimuth += 360.0
    exoatmElevation = 90.0 - zenith

    # Atmospheric Refraction correction
    if exoatmElevation > 85.0:
        refractionCorrection = 0.0
    else:
        te = np.tan(np.radians(exoatmElevation))
        if exoatmElevation > 5.0:
            refractionCorrection = 58.1 / te - 0.07 / (te*te*te) + 0.000086 / (te*te*te*te*te)
        elif exoatmElevation > -0.575:
            refractionCorrection = 1735.0 + exoatmElevation * (-518.2 + exoatmElevation * (103.4 + exoatmElevation * (-12.79 + exoatmElevation * 0.711) ) )
        else:
            refractionCorrection = -20.774 / te
        refractionCorrection = refractionCorrection / 3600.0

    solarZen = zenith - refractionCorrection

    return azimuth, solarZen


def calcSolNoonUTC( jd, longitude ):
    """
Calculate time of solar noon the given day at the given location on earth (in minute since 0 UTC)
    """
    tnoon = calcTimeJulianCent(jd)
    eqTime = calcEquationOfTime(tnoon)
    solNoonUTC = 720.0 - (longitude * 4.) - eqTime # in minutes
    return solNoonUTC


def calc_solar_stuff(julian_dates):
    """Compute various date specific solar quantities. """
    funcs = [calcSunRadVector]
    out = []
    fx_names = []
    for func in funcs:
        res = np.vectorize(func)(julian_dates)
        out.append(res)
        fx_names.append(func.__name__)
    out = np.hstack(out)
    return out, fx_names


def vec_solnoon(julian_dates, longitudes):
    """Computes time of solar zenith given dates and longitudes.

    Parameters
    ----------
    julian_dates : array
        The dates in julian format
    longitudes : array, shape=(n_locations,)
        The longitudes of each station

    Returns
       noon : array, shape=(n_dates * locations)
           the time of the solar zenith for each date location pair.
           Ordered first by location then date.
    """
    n_dates = julian_dates.shape[0]
    n_stations = longitudes.shape[0]

    # tile dates and repeat lat
    julian_dates = np.repeat(julian_dates, n_stations)
    longitudes = np.tile(longitudes, n_dates)
    out = np.vectorize(calcSolNoonUTC)(julian_dates, longitudes)
    out = out.reshape((n_dates, n_stations))
    return out


def calcSolNoon( jd, longitude, timezone, dst ):
    """
Calculate time of solar noon the given day at the given location on earth (in minute)
    """
    timeUTC    = calcSolNoonUTC(jd, longitude)
    newTimeUTC = calcSolNoonUTC(jd + timeUTC/1440.0, longitude)
    solNoonLocal = newTimeUTC + (timezone*60.0) # in minutes
    if dst:
        solNoonLocal += 60.0
    return solNoonLocal


def calcSunRiseSetUTC( jd, latitude, longitude ):
    """
Calculate sunrise/sunset the given day at the given location on earth (in minute since 0 UTC)
    """
    t = calcTimeJulianCent(jd)
    eqTime = calcEquationOfTime(t)
    solarDec = calcSunDeclination(t)
    hourAngle = calcHourAngleSunrise(latitude, solarDec)
    # Rise time
    delta = longitude + np.degrees(hourAngle)
    riseTimeUTC = 720. - (4.0 * delta) - eqTime # in minutes
    # Set time
    hourAngle = -hourAngle
    delta = longitude + np.degrees(hourAngle)
    setTimeUTC = 720. - (4.0 * delta) - eqTime # in minutes
    return riseTimeUTC, setTimeUTC

def vec_sunriseset(julian_dates, locations):
    """Computes sun rise and set for given dates and locations.

    Parameters
    ----------
    julian_dates : array
        The dates in julian format
    location : array, shape=(n_locations, 2)
        The locations, first col is lat, second is lon.

    Returns
       rise : array, shape=(n_dates * locations)
           the sun rise dates in UTC; ordered by location first and then
           date (ie val_0_0, val_1_0, val_2_0, ...) where the first index
           is location and the second date.
       set : array, shape=(n_dates * locations)
           the sun set dates (see above).
    """
    n_dates = julian_dates.shape[0]
    n_stations = locations.shape[0]

    julian_cents = np.vectorize(calcTimeJulianCent)(julian_dates)
    eq_time = np.vectorize(calcEquationOfTime)(julian_cents)
    solar_dec = np.vectorize(calcSunDeclination)(julian_cents)

    # tile dates and repeat lat
    solar_dec = np.repeat(solar_dec, n_stations)
    latitude = np.tile(locations[:, 0], n_dates)
    longitude = np.tile(locations[:, 1], n_dates)
    hour_angle = np.vectorize(calcHourAngleSunrise)(latitude, solar_dec)

    eq_time = np.repeat(eq_time, n_stations)

    # rise time
    delta = longitude + np.degrees(hour_angle)
    rise_time = 720. - (4.0 * delta) - eq_time # in minutes

    hour_angle = -hour_angle
    delta = longitude + np.degrees(hour_angle)
    set_time = 720. - (4.0 * delta) - eq_time # in minutes

    out = np.c_[rise_time, set_time]

    out = out.reshape((n_dates, n_stations, 2))
    return out


def calcSunRiseSet( jd, latitude, longitude, timezone, dst ):
    """
Calculate sunrise/sunset the given day at the given location on earth (in minutes)
    """
    rtimeUTC, stimeUTC = calcSunRiseSetUTC(jd, latitude, longitude)
    # calculate local sunrise time (in minutes)
    rnewTimeUTC, snewTimeUTC = calcSunRiseSetUTC(jd + rtimeUTC/1440.0, latitude, longitude)
    rtimeLocal = rnewTimeUTC + (timezone * 60.0)
    rtimeLocal += 60.0 if dst else 0.0
    if rtimeLocal < 0.0 or rtimeLocal >= 1440.0:
        jday = jd
        increment = 1. if rtimeLocal < 0. else -1.
        while rtimeLocal < 0.0 or rtimeLocal >= 1440.0:
            rtimeLocal += increment * 1440.0
            jday -= increment
    # calculate local sunset time (in minutes)
    rnewTimeUTC, snewTimeUTC = calcSunRiseSetUTC(jd + stimeUTC/1440.0, latitude, longitude)
    stimeLocal = snewTimeUTC + (timezone * 60.0)
    stimeLocal += 60.0 if dst else 0.0
    if stimeLocal < 0.0 or stimeLocal >= 1440.0:
        jday = jd
        increment = 1. if stimeLocal < 0. else -1.
        while stimeLocal < 0.0 or stimeLocal >= 1440.0:
            stimeLocal += increment * 1440.0
            jday -= increment
    # return
    return rtimeLocal, stimeLocal


def calcTerminator( date, latitudes, longitudes ):
    """
Calculate terminator position and solar zenith angle for a given julian date-time within latitude/longitude limits
Note that for plotting only, basemap has a built-in terminator
    """
    jd = getJD(date)
    t = calcTimeJulianCent(jd)
    ut = ( jd - (int(jd - 0.5) + 0.5) )*1440.
    npoints = 50
    zen = np.zeros((npoints,npoints))
    lats = np.linspace(latitudes[0], latitudes[1], num=npoints)
    lons = np.linspace(longitudes[0], longitudes[1], num=npoints)
    term = []
    for ilat in range(1,npoints+1):
        for ilon in range(npoints):
            az,el = calcAzEl(t, ut, lats[-ilat], lons[ilon], 0.)
            zen[-ilat,ilon] = el
        a = (90 - zen[-ilat,:])
        mins = np.r_[False, a[1:]*a[:-1] <= 0] | \
            np.r_[a[1:]*a[:-1] <= 0, False]
        zmin = mins & np.r_[False, a[1:] < a[:-1]]
        if True in zmin:
            ll = np.interp(0, a[zmin][-1::-1], lons[zmin][-1::-1])
            term.append([lats[-ilat], ll])
        zmin = mins & np.r_[a[:-1] < a[1:], False]
        if True in zmin:
            ll = np.interp(0, a[zmin], lons[zmin])
            term.insert(0, [lats[-ilat], ll])
    return lats, lons, zen, np.array(term)


def getJD( date ):
    """
Calculate julian date for given day, month and year
    """
    from dateutil.relativedelta import relativedelta

    if date.month < 2:
        date.replace(year=date.year-1)
        date += relativedelta(month=12)

    A = np.floor(date.year/100.)
    B = 2. - A + np.floor(A/4.)
    jd = np.floor(365.25*(date.year + 4716.)) + np.floor(30.6001*(date.month+1)) + date.day + B - 1524.5
    jd = jd + date.hour/24.0 + date.minute/1440.0 + date.second/86400.0
    return jd


def get_jd2(utc_datetime):
    """This function is based on NREL/TP-560-34302 by Andreas and Reda

    This function does not accept years before 0 because of the bounds check
    on Python's datetime.year field.

    """
    year = utc_datetime.year
    month = utc_datetime.month
    if(month <= 2.0):        # shift to accomodate leap years?
        year = year - 1.0
        month = month + 12.0
    day = utc_datetime.day + (((utc_datetime.hour * 3600.0) + (utc_datetime.minute * 60.0) + utc_datetime.second + (utc_datetime.microsecond / 1000000.0)) / 86400.0)
    gregorian_offset = 2.0 - (year // 100.0) + ((year // 100.0) // 4.0)
    julian_day = math.floor(365.25 * (year + 4716.0)) + math.floor(30.6001 * (month + 1.0)) + day - 1524.5
    if (julian_day <= 2299160.0):
        return julian_day # before October 5, 1852
    else:
        return julian_day + gregorian_offset # after October 5, 1852
