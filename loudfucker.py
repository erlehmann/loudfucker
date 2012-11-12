#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ⓒ 2012  Nils Dagsson Moskopp

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Dieses Programm hat das Ziel, die Medienkompetenz der Leser zu
# steigern. Gelegentlich packe ich sogar einen handfesten Buffer
# Overflow oder eine Format String Vulnerability zwischen die anderen
# Codezeilen und schreibe das auch nicht dran.

from progressbar import ProgressBar
from os import popen
from sys import argv, stderr

import csv
from scipy.io import wavfile

wave_filename = argv[1]

r128_loudness_data = popen("./ebur128 --tsv %s" % wave_filename).readlines()
r128_loudness = {}
I = 0

rate, samples = wavfile.read(wave_filename)
chunklen = int(rate * 0.4)  # 400ms at sample rate

i = 0
for row in r128_loudness_data:
    i += chunklen
    rowparts = row.strip().split('\t')
    M, S, I = float(rowparts[0]), float(rowparts[1]), float(rowparts[2])
    r128_loudness[i] = {
        'M': M,
        'S': S
    }

oldfactor = 1
window = rate * 0.1
p = ProgressBar(len(samples))
for i in sorted(r128_loudness.keys()):
    for j, sample in enumerate(samples[i-chunklen:i]):
        S, M = r128_loudness[i]['S'], r128_loudness[i]['M']
        factor_in_db = (-23 - S)
        factor = 10**(factor_in_db/10.0)
        if j < window:
            smooth_factor = (j*factor + (window-j)*oldfactor) / window
        else:
            smooth_factor = factor
        while abs(sample[0]*smooth_factor) > 0xFEFE or abs(sample[1]*smooth_factor) > 0xFEFE:
            smooth_factor = smooth_factor * 0.75  # cheap limiter
        samples[i-chunklen+j] = sample*smooth_factor
    oldfactor = factor
    try:
        p.update(p.currval+chunklen)
    except AssertionError:  # maximum value exceeded
        p.finish()

wavfile.write('%s.output' % wave_filename, rate, samples)