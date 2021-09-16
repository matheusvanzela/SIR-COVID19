# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 12:31:06 2020

@author: mathe
"""

import numpy as np
import matplotlib.pyplot as plt

# simulation start date March 16th (rough German data snapshot)

S = 85000000                    # susceptible population Germany
I = 8000                        # infected at start date
R = 60                          # recovered at start date
D = 20                          # deaths at start date
a = 0.0000000027                # transmission factor (eyeballed at start date to fit the curve)
b = 1/3                        # average recovery period (from media hearsay)

reduction_factor = 1            # daily social distancing / scare effects
letality = 0.01                 # letality under conditions of proper medical care from optimistic media hearsay
letality_no_care = 0.04         # letality under conditions of overwhelmed medical system from media hearsay
h = 1/10                        # hospitalization factor (from media hearsay)
healthcare_capacity = 60000     # health care capacity (picked up from the internet)

days = 100                       # simulation horizon

Is = np.zeros(days-1)            # initialize all the things
Rs = np.zeros(days-1)
ds = np.zeros(days-1)
Hs = np.zeros(days-1)
Ds = np.zeros(days-1)
c = np.ones(days-1) * healthcare_capacity

for i in range(1, days):

    a = a * reduction_factor    # assume people get scared a little more every day
    l = letality if I*h <= healthcare_capacity else letality_no_care

    dS = -a * S * I             # SIR model per-step deltas
    dI = a * S * I - b * I
    dR = b * I * (1-l)          # split recovered into deaths and recovered
    dD = b * I * l

    S += dS                     # apply deltas
    I += dI
    R += dR
    D += dD

    Is[i-1] = I                 # fill plots
    Hs[i-1] = I * h
    Rs[i-1] = R
    Ds[i-1] = D
    ds[i-1] = i

    print("Day %i - Infected: %i Dead: %i" % (i, I, D))

plt.plot(ds, Is)
plt.plot(ds, Hs)
plt.plot(ds, Rs)
plt.plot(ds, Ds)
plt.plot(ds, c)
plt.legend(("Infected", "Hospitalized", "Recovered", "Deaths", "Capacity"))

plt.show()