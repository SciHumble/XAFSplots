#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df=pd.read_table(
        'Cu.dat', skiprows=39,escapechar='#', delim_whitespace=True, 
#        names=[
#            'e', 'xmu', 'bkg', 'pre_edge', 'post_edge', 'der', 'sec', 'i0',
#            'chie'
#            ]
        )

df['derivative']= df.xmu.diff(periods=-1)/df.e.diff(periods=-1)
kedge = df.e[df.derivative.idxmax()]

fig=plt.figure()
ax=fig.add_subplot()
ax.plot(df['e'], df['der'])
ax.plot(df['e'], df['derivative'])
ax.set_xlabel('Energy in (eV)')
ax.set_ylabel('Absorption')
ax.grid(axis='both')
ax.axvline(x=kedge, color='red')
ax.set_xlim([kedge-50,kedge+50])
ax.text(kedge+1, 0.3, str(kedge))
plt.savefig("figure.png")
#plt.show()
