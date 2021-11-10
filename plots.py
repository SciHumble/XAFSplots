"""System module."""
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np

# Vorbereitung um das alles in eine Funktion plot(Element, kedge_theory, *Reference_Points) zu integrieren.
Element = 'Cu'
Reference_Points = (8984.5, 8989.6)
kedge_theory = 8979

datafile = '%s.dat' % Element

df = pd.read_table(
        datafile, comment='#', delim_whitespace=True, 
        names=[
            'e', 'xmu', 'bkg', 'pre_edge', 'post_edge', 'der', 'sec', 'i0',
            'chie'
            ]
        )

kedge_df = df.e[df.der.idxmax()]
line_number_kedge = df.der.idxmax()
x_offset = kedge_theory - kedge_df
minimum = df.der.idxmin()
maximum = df.der.idxmax()
scale_range = maximum - minimum

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(df.e + x_offset, df.der)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Absorption')
ax.grid(axis='both')
ax.axvline(x=kedge_theory, color='red', linewidth=1)
# Der Text wird nicht angezeigt
ax.annotate(''+str(kedge_theory), xy=(kedge_theory, df.der[df.der.idxmax()]),
           xytext=(kedge_theory-10, df.der[df.der.idxmax()]-0.05*scale_range),
           arrowprops=dict(facecolor='black', shrink=0.05))
print(df.der[df.der.idxmax()])
ax.text(x=kedge_theory, y=maximum, s=str(kedge_theory))
ax.set_xlim([kedge_theory - 50, kedge_theory + 50])

for i in range(0, len(Reference_Points)):
    ax.axvline(x=Reference_Points[i], color='blue', linewidth=0.5)
# Der Text wird nicht angezeigt
    ax.text(Reference_Points[i], maximum + 0.00005*scale_range, str(Reference_Points[i]))

filename = '%s.svg' % Element
plt.savefig(filename)       
