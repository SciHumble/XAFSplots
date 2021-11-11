"""System module."""
import matplotlib.pyplot as plt
import pandas as pd
# import numpy as np

plt.switch_backend("agg")  # Use the non-interactive backend in mpl to just save
# figures and not render them in the back


class Element:
    """This class is used to simplify the analysis of the XAFS-data from standard foils. For correct usage,
    please use the given Data from Hephaestus and import it in the same file of the plot.py file."""

    def __init__(self, name, edge, reference_points):
        self.name = name
        self.edge = edge
        self.reference_points = reference_points
        self.df = pd.read_table(
            '%s.dat' % self.name, comment='#', delim_whitespace=True,
            names=[
                'e', 'xmu', 'bkg', 'pre_edge', 'post_edge', 'der', 'sec', 'i0',
                'chie'
                ]
            )

    def plot_edge(self):
        """This will plot the Data in Range of +-50 eV around the theoretical K-edge and save it in a file called:
        Element.svg"""
        x_offset = self.edge - self.df.e[self.df.der.idxmax()]
        scale_range = self.df.der[self.df.der.idxmax()] - self.df.der[self.df.der.idxmin()]

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.df.e + x_offset, self.df.der)
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Absorption')
        ax.grid(axis='both')
        ax.axvline(x=self.edge, color='red', linewidth=1)
        ax.annotate(
            str(self.edge),
            xy=(self.edge, self.df.der[self.df.der.idxmax()]),
            xytext=(self.edge - 30, self.df.der[self.df.der.idxmax()] - 0.35 * scale_range),
            arrowprops=dict(
                facecolor='black',
                width=0.1,
                headwidth=3,
                shrink=0.05
            )
        )
        ax.text(
            x=self.edge - 1,
            y=self.df.der[self.df.der.idxmax()],
            s=str(self.edge),
            ha='right'
        )
        ax.set_xlim([self.edge - 50, self.edge + 50])

        for ind, i in enumerate(self.reference_points):
            ax.axvline(i, color='blue', linewidth=0.5)
            ax.text(
                i,
                self.df.der[self.df.der.idxmax()] + 0.095 * scale_range
                + 0.025 * ((-1) ** ind) * scale_range,
                str(i),
                ha='center'
            )

        return plt.savefig('%s.svg' % self.name)


cu = Element('Cu', 8979, [8984.5, 8989.6])
cu.plot_edge()
