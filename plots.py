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

KedgeInDataFrame = df.e[df.der.idxmax()]
x_offset = kedge_theory - KedgeInDataFrame

fig = plt.figure()
ax = fig.add_subplot()
ax.plot(df.e + x_offset, df.der)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Absorption')
ax.grid(axis='both')
ax.axvline(x=kedge_theory, color='red', linewidth=1)
# Der Text wird nicht angezeigt
ax.text(x=kedge_theory + 5, y=df.der.idxmax(), s=str(kedge_theory))
ax.set_xlim([kedge_theory - 50, kedge_theory + 50])

for i in range(0, len(Reference_Points)):
    ax.axvline(x=Reference_Points[i], color='blue', linewidth=0.5)
# Der Text wird nicht angezeigt
    ax.text(x=Reference_Points[i] + 5, y=df.der.idxmax() + 10, s=str(Reference_Points[i]))

filename = '%s.svg' % Element
plt.savefig(filename)       
