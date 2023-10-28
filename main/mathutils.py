import math
from .models import SatelliteModel
from sgp4.api import jday, Satrec

R = 6370
g = 9.81
GM4pi2 = 1.009e13


class Satellite:
    def __init__(self, id, s, t, angle):
        self.id = id
        self.TLE = {
            's': s,
            't': t
        }
        self.angle = math.radians(angle)
        self.height = 1 / float(self.TLE['t'].split(" ")[-1]) * 24 * 60 * 60
        self.height = math.pow(self.height ** 2 * GM4pi2, 1 / 3) / 1000 - 6371
        self.maxDist = self.height / math.cos(self.angle / 2)


class Point:
    x = 0
    y = 0
    z = 0

    def __init__(self, lati, long):
        lati = math.radians(lati)
        long = math.radians(long)
        self.x = R * math.cos(lati) * math.cos(long)
        self.y = R * math.cos(lati) * math.sin(long)
        self.z = R * math.sin(lati)

    def set_coord(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class SatPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def distFromTo(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


def calculate_time(geoPoints):
    satArr = list(map(lambda x: Satellite(x.id, x.s, x.t, x.view_angle), SatelliteModel.objects.all()))

    points = []
    for geoPoint in geoPoints:
        points.append(Point(geoPoint[0], geoPoint[1]))

    # генерируем доп поинты, чтобы отсканить всю область.
    for i in range(4):
        for j in range(i + 1, 4):
            x = (points[i].x + points[j].x) / 2
            y = (points[i].y + points[j].y) / 2
            z = (points[i].z + points[j].z) / 2
            P = Point(0, 0)
            P.set_coord(x, y, z)
            points.append(P)

    dists = []
    for id, sat in enumerate(satArr):
        satellite = Satrec.twoline2rv(sat.TLE['s'], sat.TLE['t'])
        # 1 / v = T (суток на оборот), T * 24 * 60 + 1 (минут на оборот)
        time = int(1 / float(sat.TLE['t'].split(" ")[-1]) * 24 * 60) + 1
        # добавляем спутник
        dists.append([])
        # заранее добавляем нужное кол-во точек
        # формат [наименьшее расстояние, координаты на орбите, время]
        for ip, _ in enumerate(points):
            dists[id].append([1e20, 0, 0])
        for i in range(time):
            if (i % 2 == 0):
                jd, fr = jday(2023, 10, int(0 + i / 60 / 24 % 30), int(i / 60 % 24), int(i % 60), 0)
                e, r, v = satellite.sgp4(jd, fr)

                # перебираем точки
                for ip, point in enumerate(points):
                    distToPoint = distFromTo(r[0], r[1], r[2], point.x, point.y, point.z)
                    # если дист < минДист и дист < максДист
                    if (dists[id][ip][0] > distToPoint and sat.maxDist >= distToPoint):
                        dists[id][ip][0] = distToPoint
                        dists[id][ip][1] = SatPoint(r[0], r[1], r[2])
                        dists[id][ip][2] = i
    minTime = []
    for i in range(len(points)):
        minTime.append(1e20)
    for id, sat in enumerate(dists):
        for ip, satData in enumerate(sat):
            dist, point, time = satData
            if point != 0:
                minTime[ip] = min(minTime[ip], time)
    return -1 if max(minTime) == 1e20 else max(minTime)