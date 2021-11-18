"""System module."""
import matplotlib.pyplot as plt
import pandas as pd
import os.path


plt.switch_backend("agg")  # Use the non-interactive backend in mpl to just
# save figures and not render them in the back
plt.rcParams.update({'figure.max_open_warning': 0})  # This has the purpose to
# prevent the warning, that more than 20 Figures has been created.


class Element:
    """This class is used to simplify the analysis of the XAFS-data from
     standard foils. For correct usage, please use the given Data from
     Hephaestus and import it in the same file of the plot.py file."""

    def __init__(self, name: str, edge_energy: float, reference_points: list):
        self.name = name
        self.edge_energy = edge_energy
        self.reference_points = reference_points
        if os.path.isfile('Data/{}.xmu'.format(self.name)) is True:
            self.df = pd.read_table(
                'Data/{}.xmu'.format(self.name),
                comment='#',
                delim_whitespace=True,
                names=[
                    'e',
                    'xmu',
                    'bkg',
                    'pre_edge',
                    'post_edge',
                    'der',
                    'sec',
                    'i0',
                    'chie'
                    ]
                )
            self.data_origin = 'Hephaestus'
        elif os.path.isfile('Data/{}.csv'.format(self.name)) is True:
            self.df = pd.read_csv(
                'Data/{}.csv'.format(self.name),
                sep=';',
                names=['e0', 'der']
                )
            self.df['e'] = self.df.e0 + self.edge_energy
            self.data_origin = 'XAFS Materials'

    def plot_edge(self):
        """This will plot the Data in Range of +-50 eV around the theoretical
         K-edge and save it in a file called: Element.svg"""
        id_max = self.df.der[(self.df['e'] < self.edge_energy + 7.5) &
                             (self.df['e'] > self.edge_energy - 7.5)].idxmax()
        # I assume that the from my data is around the region of +-7.5 eV
        x_offset = self.edge_energy - self.df.e[id_max]
        scale_range = self.df.der[self.df.der.idxmax()] \
            - self.df.der[self.df.der.idxmin()]

        xticks_list = []
        for count in range(-5, 6):
            xticks_list.append(count * 10)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.df.e + x_offset, self.df.der)
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Absorption')
        ax.grid(axis='both')
        ax.axvline(x=self.edge_energy, color='red', linewidth=1)
        """
        ax.annotate(
            str(self.edge_energy),
            xy=(self.edge_energy, self.df.der[id_max]),
            xytext=(
                self.edge_energy - 30,
                self.df.der[self.df.der.idxmax()] - 0.35 * scale_range
                    ),
            arrowprops=dict(
                facecolor='black',
                width=0.1,
                headwidth=3,
                shrink=0.05
            )
        )
        """
        ax.text(
            x=self.edge_energy - 1,
            y=self.df.der[self.df.der.idxmax()],
            s=str(self.edge_energy),
            ha='right'
        )
        ax.set_xlim([self.edge_energy - 50, self.edge_energy + 50])
#        ax.set_xticks([x + self.edge_energy for x in xticks_list])
#        ax.set_xticklabels([str(x + self.edge_energy) for x in xticks_list])

        for ind, reference in enumerate(self.reference_points):
            if reference <= self.edge_energy + 50:
                ax.axvline(x=reference, color='blue', linewidth=0.5)
                ax.text(
                    x=reference,
                    y=self.df.der[self.df.der.idxmax()] + 0.095 * scale_range
                    + 0.025 * ((-1) ** ind) * scale_range,  # I use the -1**ind
                    # that the values of the reference points don't overlap
                    s=str(reference),
                    ha='center'
                )

        return plt.savefig('Plots/{}.svg'.format(self.name))

    def print_information(self):
        print(self.name)
        print(self.edge_energy)
        print(self.reference_points)
        return


df_ref = pd.read_csv(
    'FoilsData.csv', names=['name', 'edge', 'ref'],
    sep=';'
)

el_list = []
edge_dict = {}  # eV
ref_dict = {}  # eV

for i in range(len(df_ref)):
    el_list.append(df_ref.name[i])
    edge_dict[df_ref.name[i]] = df_ref.edge[i]
    if df_ref.ref[i] == '[]':
        ref_dict[df_ref.name[i]] = []
    else:
        ref_dict[df_ref.name[i]] = \
            [float(x) for x in df_ref.ref[i][1:-1].split(',')]

for i in el_list:
    i = Element(i, edge_dict[i], ref_dict[i])
    i.plot_edge()

"""
TEST_ELEMENT = 'Ti'
test = Element(TEST_ELEMENT, edge_dict[TEST_ELEMENT], ref_dict[TEST_ELEMENT])
print('Die Daten von {} kommen aus: \n{}'.format(
    TEST_ELEMENT, test.data_origin
))
"""
