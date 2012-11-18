#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import *
from sys import stdin

rdata = genfromtxt(stdin, delimiter='\t', names = ('M', 'S', 'I'))
times = [0.4*i for i in range(len(rdata))]
M = plot(times, rdata['M'])
S = plot(times, rdata['S'])
I = plot(times, rdata['I'])
xlabel('Time (s)')
ylabel('Loudness (LUFS)')
ylim(-80,0)
show()
