import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df=pd.read_table(
        'Cu.dat', comment='#', delim_whitespace=True, 
        names=[
            'e', 'xmu', 'bkg', 'pre_edge', 'post_edge', 'der', 'sec', 'i0',
            'chie'
            ]
        )
axesy = 'derivative'

df['derivative']= df.xmu.diff(periods=-1)/df.e.diff(periods=-1)

kedge = df.e[df.derivative.idxmax()]

df.plot(x='e', y=['der', 'derivative'])
plt.xlabel('Energy in [\si(\electronvolt)]')
plt.ylabel('Absorption')
plt.grid(axis='both')
plt.axvline(x=kedge, color='red')
plt.xlim([kedge-50,kedge+50])

print(kedge)
plt.savefig("plot.png")
#plt.show()
