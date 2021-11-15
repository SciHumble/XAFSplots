"""System module."""
import matplotlib.pyplot as plt
import pandas as pd
import ast  # to convert a string to a list and the string has already the format of a list.

# import numpy as np
import os.path

plt.switch_backend("agg")  # Use the non-interactive backend in mpl to just save
# figures and not render them in the back


class Element:
    """This class is used to simplify the analysis of the XAFS-data from standard foils. For correct usage,
    please use the given Data from Hephaestus and import it in the same file of the plot.py file."""

    def __init__(self, name, edge, reference_points: list):
        self.name = name
        self.edge = edge
        self.reference_points = reference_points
        if os.path.isfile("Data/%s.xmu" % self.name) is True:
            self.df = pd.read_table(
                "Data/%s.xmu" % self.name,
                comment="#",
                delim_whitespace=True,
                names=[
                    "e",
                    "xmu",
                    "bkg",
                    "pre_edge",
                    "post_edge",
                    "der",
                    "sec",
                    "i0",
                    "chie",
                ],
            )
        elif os.path.isfile("Data/%s.csv" % self.name) is True:
            self.df = pd.read_csv(
                "Data/%s.csv" % self.name, sep=";", names=["e0", "der"]
            )
            self.df["e"] = self.df.e0 + self.edge

    def plot_edge(self):
        """This will plot the Data in Range of +-50 eV around the theoretical K-edge and save it in a file called:
        Element.svg"""
        x_offset = self.edge - self.df.e[self.df.der.idxmax()]
        scale_range = (
            self.df.der[self.df.der.idxmax()]
            - self.df.der[self.df.der.idxmin()]
        )

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.df.e + x_offset, self.df.der)
        ax.set_xlabel("Energy (eV)")
        ax.set_ylabel("Absorption")
        ax.grid(axis="both")
        ax.axvline(x=self.edge, color="red", linewidth=1)
        ax.annotate(
            str(self.edge),
            xy=(self.edge, self.df.der[self.df.der.idxmax()]),
            xytext=(
                self.edge - 30,
                self.df.der[self.df.der.idxmax()] - 0.35 * scale_range,
            ),
            arrowprops=dict(
                facecolor="black", width=0.1, headwidth=3, shrink=0.05
            ),
        )
        ax.text(
            x=self.edge - 1,
            y=self.df.der[self.df.der.idxmax()],
            s=str(self.edge),
            ha="right",
        )
        ax.set_xlim([self.edge - 50, self.edge + 50])

        for ind, ref in enumerate(self.reference_points):
            ax.axvline(str(ref), color="blue", linewidth=0.5)
            ax.text(
                str(ref),
                self.df.der[self.df.der.idxmax()]
                + 0.095 * scale_range
                + 0.025 * ((-1) ** ind) * scale_range,
                str(ref),
                ha="center",
            )

        return plt.savefig("%s.svg" % self.name)

    def print_information(self):
        print(self.name)
        print(self.edge)
        print(self.reference_points)
        return


df_ref = pd.read_csv("FoilsData.csv", names=["name", "edge", "ref"], sep=";")

object_list = []
for i in range(len(df_ref)):
    obj = (
        df_ref.name[i],
        df_ref.edge[i],
        ast.literal_eval(df_ref.ref[i]),
    )  # ast.literal_eval is a function to
    # convert a string which has the format of a list to list.
    object_list.append(obj)
