#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

plt.switch_backend("agg") #Use the non-interactive backend in mpl to just save
#figures and not render them in the back

df = pd.read_table(
        'Cu.xmu', skiprows=40,
        #escapechar='#',
        delim_whitespace=True,
        names=[
            'e', 'xmu', 'bkg', 'pre_edge', 'post_edge', 'der', 'sec', 'i0',
            'chie'
            ]
        )

df['derivative'] = df.xmu.diff(periods=-1)/df.e.diff(periods=-1)
kedge = df.e[df.derivative.idxmax()]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(df['e']+(8979-kedge), df['der'])
#ax.plot(df['e'], df['derivative'])
ax.set_xlabel('Energy in (eV)')
ax.set_ylabel('Absorption')
ax.grid(axis='both')
ax.axvline(x=kedge, color='red')
ax.axvline(x=8979, color='blue')
ax.axvline(x=8984.5, color='blue')
ax.axvline(x=8989.6, color='blue')
ax.set_xlim([kedge-50,kedge+50])
ax.text(kedge+1, 0.3, str(kedge))
fig.savefig("figure.svg")
#fig.show()
