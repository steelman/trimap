#!/usr/bin/pytho
# -*- coding: utf-8 -*-
#
# trimap.py - Calculate positions of vertices of triangle mesh
# Copyright (C) 2016 Łukasz Stelmach
#

import csv
import math
import sys 

class Point:
    def __str__(self):
        return "x: %.4f y: %.4f r: %d" % (self.x, self.y, self.order)

    def __init__(self, x=None, y=None):
        self.x = float(x) if x is not None else None
        self.y = float(y) if y is not None else None

        self.order = None
        if x is not None and y is not None:
            self.order = 0;

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx+dy*dy)

    def set_position(self, A, B, a, b):
        c = A.distance(B)
        a2 = a * a
        b2 = b * b
        c2 = c * c

        # https://pl.wikipedia.org/wiki/Wci%C4%99cie_liniowe_w_prz%C3%B3d#Opis_metody_2
        Ca = -a2 + b2 + c2
        Cb =  a2 - b2 + c2
        Cc =  a2 + b2 - c2

        FP = math.sqrt(Ca*Cb+Ca*Cc+Cb*Cc)
        self.x = (A.x * Cb + A.y * FP + B.x * Ca - B.y * FP)/(Ca + Cb)
        self.y = (-A.x * FP + A.y * Cb + B.x * FP + B.y * Ca)/(Ca + Cb)
        self.order = 1 + (A.order if A.order > B.order else B.order)

class Triangle:
    def __str__(self):
        return "\tA:  %s\n\tB:  %s\n\tC:  %s\n" % (self._A, self._B, self._C)
    
    def __init__(self, A, B, C, a, b):
        self._A = A
        self._B = B
        self._C = C
        self._a = float(a)
        self._b = float(b)

    def set_c(self):
        self._C.set_position(self._A, self._B, self._a, self._b)

Points = {}
try:
    infile = sys.argv[1]
except IndexError:
    infile = sys.stdin

csvreader = csv.reader(infile)
for row in csvreader:
    if row[0] == "P":
        Points[row[1]]=Point(row[2], row[3])
    elif row[0] == "T":
        c = Points[row[3]] = Point()
        t = Triangle(Points[row[1]],
                     Points[row[2]],
                     c, row[4], row[5])
        t.set_c()

csvwriter = csv.writer(sys.stdout)
for p in sorted(Points.keys()):
    csvwriter.writerow([p, Points[p].x, Points[p].y, Points[p].order])
