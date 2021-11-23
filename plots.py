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
        self.data_origin = []
        if os.path.isfile('Data/{}.xmu'.format(self.name)) is True:
            self.df_hepha = pd.read_table(
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
            self.data_origin.append('Hephaestus')
        if os.path.isfile('Data/{}.csv'.format(self.name)) is True:
            self.df_xafsmat = pd.read_csv(
                'Data/{}.csv'.format(self.name),
                sep=';',
                names=['e0', 'der']
                )
            self.df_xafsmat['e'] = self.df_xafsmat.e0 + self.edge_energy
            self.data_origin.append('XAFS Materials')

    def plot_edge(self):
        """This will plot the Data in Range of +-50 eV around the theoretical
         K-edge and save it in a file called: Element.svg"""
        df_ref_heph = pd.read_csv('Data/HephaestusData.csv')
        df_ref_xafs = pd.read_csv('Data/XAFSMaterials.csv')
        for origin_name in self.data_origin:
            edge_search = self.edge_energy
            if origin_name == 'Hephaestus':
                df = self.df_hepha
                df_ref_heph = pd.read_csv('Data/HephaestusData.csv')
                self.edge_energy = df_ref_heph.at[
                    df_ref_heph[df_ref_heph['name'] == self.name].index.item(),
                    'edge']
                if df_ref_heph.at[df_ref_heph[df_ref_heph['name'] == self.name].index.item(), 'ref'] == '[]':
                    self.reference_points = []
                else:
                    self.reference_points = [
                        float(x) for x in
                        df_ref_heph.at[
                            df_ref_heph[
                                df_ref_heph['name'] == self.name].index.item(),
                            'ref'][1:-1].split(',')
                    ]
                datapoint_edge = df_ref_heph.at[
                    df_ref_heph[df_ref_heph['name'] == self.name].index.item(),
                    'raw_edge'
                ]
                if datapoint_edge != 0:
                    edge_search = datapoint_edge
            elif origin_name == 'XAFS Materials':
                df = self.df_xafsmat
                df_ref_xafs = pd.read_csv('Data/XAFSMaterials.csv')
                self.edge_energy = df_ref_xafs.at[
                    df_ref_xafs[df_ref_xafs['name'] == self.name].index.item(),
                    'edge'
                ]
                if df_ref_xafs.at[df_ref_xafs[df_ref_xafs['name'] == self.name].index.item(), 'ref'] == '[]':
                    self.reference_points = []
                else:
                    self.reference_points = [
                        float(x) for x in df_ref_xafs.at[
                            df_ref_xafs[
                                df_ref_xafs['name'] == self.name].index.item(),
                            'ref'
                        ][1:-1].split(',')
                    ]
                datapoint_edge = df_ref_xafs.at[
                    df_ref_xafs[df_ref_xafs['name'] == self.name].index.item(),
                    'raw_edge'
                ]
                if datapoint_edge != 0:
                    edge_search = datapoint_edge

            margin = 5
            id_max = df.der[(df['e'] < edge_search + margin) &
                            (df['e'] > edge_search - margin)].idxmax()
            # I assume that the from my data is around the region of +-5 eV
            x_offset = self.edge_energy - df.e[id_max]
            scale_range = df.der[df.der.idxmax()] \
                - df.der[df.der.idxmin()]

            xticks_list = []
            for count in range(-5, 6):
                xticks_list.append(count * 10)

            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(df.e + x_offset, df.der)
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
                y=df.der[df.der.idxmax()],
                s=str(self.edge_energy),
                ha='right'
            )
            ax.set_xlim([self.edge_energy - 50, self.edge_energy + 50])

            for ind, reference in enumerate(self.reference_points):
                y_coor_offset = 0
                if ind == 0:
                    place_one = reference
                if ind == 2 and place_one > reference - 12:
                    y_coor_offset = 0.05 * scale_range
                if reference <= self.edge_energy + 50:
                    ax.axvline(x=reference, color='blue', linewidth=0.5)
                    ax.text(
                        x=reference,
                        y=df.der[df.der.idxmax()] + 0.095 * scale_range
                        + 0.025 * ((-1) ** ind) * scale_range + y_coor_offset,
                        # I use the -1**ind that the values of the reference
                        # points don't overlap
                        s=str(reference),
                        ha='center'
                    )
            ax.text(
                x=self.edge_energy + 50,
                y=df.der[df.der.idxmin()] - 0.18 * scale_range,
                s=origin_name,
                ha='center'
            )
            ax.text(
                x=self.edge_energy - 30,
                y=df.der[df.der.idxmax()] + 0.1 * scale_range,
                s=self.name,
                ha='center',
                fontsize=15
            )

            plt.savefig(f'Plots/{self.name}_{origin_name[0:4]}.svg')

        return

    def print_information(self):
        print(self.name)
        print(self.edge_energy)
        print(self.reference_points)
        return


df_ref = pd.read_csv(
    'FoilsData.csv', names=['name', 'edge', 'ref', 'raw_edge'],
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
