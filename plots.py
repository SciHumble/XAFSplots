"""System module."""
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np

plt.switch_backend("agg")  # Use the non-interactive backend in mpl to just save
# figures and not render them in the back

# Vorbereitung um das alles in eine Funktion plot(element, kedge_theory, reference_points) zu integrieren.
element = 'Cu'
reference_points = [8984.5, 8989.6]  # eV
kedge_theory = 8979  # eV

datafile = '%s.dat' % element

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
scale_range = df.der[df.der.idxmax()] - df.der[df.der.idxmin()]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(df.e + x_offset, df.der)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Absorption')
ax.grid(axis='both')
ax.axvline(x=kedge_theory, color='red', linewidth=1)
ax.annotate(
    str(kedge_theory),
    xy=(kedge_theory, df.der[df.der.idxmax()]),
    xytext=(kedge_theory-30, df.der[df.der.idxmax()]-0.35*scale_range),
    arrowprops=dict(
        facecolor='black',
        width=0.1,
        headwidth=3,
        shrink=0.05
    )
)
ax.text(
    x=kedge_theory - 1,
    y=df.der[df.der.idxmax()],
    s=str(kedge_theory),
    ha='right'
)
ax.set_xlim([kedge_theory - 50, kedge_theory + 50])

for ind, i in enumerate(reference_points):
    ax.axvline(i, color='blue', linewidth=0.5)
    ax.text(
        i,
        df.der[df.der.idxmax()] + 0.095*scale_range
        + 0.025*((-1)**ind)*scale_range,
        str(i),
        ha='center'
    )

filename = '%s.svg' % element
plt.savefig(filename)       
