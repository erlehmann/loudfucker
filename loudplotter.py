#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import *
from sys import stdin

rdata = genfromtxt(stdin, delimiter='\t', names = ('M', 'S', 'I'))
samples = range(len(rdata))
M = plot(samples, rdata['M'])
S = plot(samples, rdata['S'])
I = plot(samples, rdata['I'])
show()
