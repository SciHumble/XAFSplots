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

    def __init__(self, name: str):
        self.name = name
        self.data_origin = []

        if os.path.isfile('Data/{}.xmu'.format(self.name)) is True:
            self.df_heph = pd.read_table(
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
            self.df_ref_heph = pd.read_csv('Data/HephaestusData.csv')
            self.edge_heph = self.df_ref_heph.at[
                    self.df_ref_heph[self.df_ref_heph['name'] == self.name].index.item(),
                    'edge']
            if self.df_ref_heph.at[self.df_ref_heph[self.df_ref_heph['name'] == self.name].index.item(), 'ref'] == '[]':
                self.ref_heph = []
            else:
                self.ref_heph = [
                    float(x) for x in
                    self.df_ref_heph.at[
                        self.df_ref_heph[
                            self.df_ref_heph['name'] == self.name].index.item(),
                        'ref'][1:-1].split(',')
                ]
            self.search_edge_heph = self.df_ref_heph.at[
                self.df_ref_heph[self.df_ref_heph['name'] == self.name].index.item(),
                'raw_edge'
            ]
            if self.search_edge_heph == 0:
                self.search_edge_heph = self.edge_heph

        if os.path.isfile('Data/{}.csv'.format(self.name)) is True:
            self.df_ref_xafs = pd.read_csv('Data/XAFSMaterials.csv')
            self.edge_xafs = self.df_ref_xafs.at[
                self.df_ref_xafs[
                    self.df_ref_xafs['name'] == self.name].index.item(),
                'edge'
            ]
            self.edge_energy = self.edge_xafs
            if self.df_ref_xafs.at[self.df_ref_xafs[self.df_ref_xafs[
                                                        'name'] == self.name].index.item(), 'ref'] == '[]':
                self.ref_xafs = []
            else:
                self.ref_xafs = [
                    float(x) for x in self.df_ref_xafs.at[
                                          self.df_ref_xafs[
                                              self.df_ref_xafs[
                                                  'name'] == self.name].index.item(),
                                          'ref'
                                      ][1:-1].split(',')
                ]
            self.reference_points = self.ref_xafs
            self.df_xafs = pd.read_csv(
                'Data/{}.csv'.format(self.name),
                sep=';',
                names=['e0', 'der']
                )
            self.df_xafs['e'] = self.df_xafs.e0 + self.edge_energy
            self.data_origin.append('XAFS Materials')
            self.search_edge_xafs = self.df_ref_xafs.at[
                    self.df_ref_xafs[self.df_ref_xafs['name'] == self.name].index.item(),
                    'raw_edge'
                ]
            if self.search_edge_xafs == 0:
                self.search_edge_xafs = self.edge_xafs

        if os.path.isfile('Data/{}.xmu'.format(self.name)) is True:
            self.edge_energy = self.edge_heph
            self.reference_points = self.ref_heph


    def plot_edge(self):
        """This will plot the Data in Range of +-50 eV around the theoretical
         K-edge and save it in a file called: Element.svg"""

        fig = plt.figure()
        ax = fig.add_subplot(111)
        margin = 5  # I assume that the from my data is around the region of
        # +-5 eV
        ax.set_xlabel('Energy (eV)')
        ax.set_ylabel('Absorption')
        ax.grid(axis='both')
        color_heph = 'dodgerblue'
        color_xafs = 'crimson'

        if self.data_origin == ['Hephaestus', 'XAFS Materials']:
            scale_range = self.df_heph.der[self.df_heph.der.idxmax()] \
                          - self.df_heph.der[self.df_heph.der.idxmin()]
            # Hephaestus
            id_max_heph = self.df_heph.der[(self.df_heph['e'] < self.search_edge_heph + margin) &
                            (self.df_heph['e'] > self.search_edge_heph - margin)].idxmax()
            x_offset_heph = self.edge_heph - self.df_heph.e[id_max_heph]
            ax.plot(
                self.df_heph.e + x_offset_heph,
                self.df_heph.der,
                label='Hephaestus',
                color=color_heph
            )

            # XAFS Materials
            id_max_xafs = self.df_xafs.der[(self.df_xafs['e'] < self.search_edge_xafs + margin) &
                            (self.df_xafs['e'] > self.search_edge_xafs - margin)].idxmax()
            x_offset_xafs = self.edge_xafs - self.df_xafs.e[id_max_xafs]
            ax.plot(
                self.df_xafs.e + x_offset_xafs,
                self.df_xafs.der / (
                    self.df_xafs.der[self.df_xafs.der.idxmax()] /
                    self.df_heph.der[self.df_heph.der.idxmax()]),
                # Normalization of the values
                label='XAFS Materials',
                color=color_xafs
            )
            ax.text(
                x=self.edge_energy - 1,
                y=self.df_heph.der[self.df_heph.der.idxmax()],
                s=str(self.edge_energy),
                ha='right'
            )

        elif self.data_origin == ['Hephaestus']:
            scale_range = self.df_heph.der[self.df_heph.der.idxmax()] \
                          - self.df_heph.der[self.df_heph.der.idxmin()]
            id_max_heph = self.df_heph.der[
                (self.df_heph['e'] < self.search_edge_heph + margin) &
                (self.df_heph['e'] > self.search_edge_heph - margin)].idxmax()
            x_offset_heph = self.edge_heph - self.df_heph.e[id_max_heph]
            ax.plot(
                self.df_heph.e + x_offset_heph,
                self.df_heph.der,
                label='Hephaestus',
                color=color_heph
            )

        elif self.data_origin == ['XAFS Materials']:
            scale_range = self.df_xafs.der[self.df_xafs.der.idxmax()] \
                          - self.df_xafs.der[self.df_xafs.der.idxmin()]
            id_max_xafs = self.df_xafs.der[
                (self.df_xafs['e'] < self.search_edge_xafs + margin) &
                (self.df_xafs['e'] > self.search_edge_xafs - margin)].idxmax()
            x_offset_xafs = self.edge_xafs - self.df_xafs.e[id_max_xafs]
            ax.plot(
                self.df_xafs.e + x_offset_xafs,
                self.df_xafs.der,
                label='XAFS Materials',
                color=color_xafs
            )

        else:
            print(f'There is no Data for {self.name}')
            return

        ax.axvline(x=self.edge_energy, color='black', linewidth=1)
        ax.set_xlim([self.edge_energy - 50, self.edge_energy + 50])
        ax.legend()

        if 'Hephaestus' in self.data_origin:

            ax.text(
                x=self.edge_energy - 1,
                y=self.df_heph.der[self.df_heph.der.idxmax()],
                s=str(self.edge_energy),
                ha='right'
            )
            ax.text(
                x=self.edge_energy - 30,
                y=self.df_heph.der[
                      self.df_heph.der.idxmax()] + 0.1 * scale_range,
                s=self.name,
                ha='center',
                fontsize=15
            )
            for ind, reference in enumerate(self.reference_points):
                y_coor_offset = 0
                if ind == 0:
                    place_one = reference
                if ind == 2 and place_one > reference - 12:
                    y_coor_offset = 0.05 * scale_range
                if reference <= self.edge_energy + 50:
                    ax.axvline(x=reference, color='black', linewidth=0.5)
                    ax.text(
                        x=reference,
                        y=self.df_heph.der[self.df_heph.der.idxmax()] + 0.095 * scale_range
                          + 0.025 * ((
                                         -1) ** ind) * scale_range + y_coor_offset,
                        # I use the -1**ind that the values of the reference
                        # points don't overlap
                        s=str(reference),
                        ha='center'
                    )
        else:
            ax.text(
                x=self.edge_energy - 1,
                y=self.df_xafs.der[self.df_xafs.der.idxmax()],
                s=str(self.edge_energy),
                ha='right'
            )
            ax.text(
                x=self.edge_energy - 30,
                y=self.df_xafs.der[self.df_xafs.der.idxmax()] + 0.1 * scale_range,
                s=self.name,
                ha='center',
                fontsize=15
            )
            for ind, reference in enumerate(self.reference_points):
                y_coor_offset = 0
                if ind == 0:
                    place_one = reference
                if ind == 2 and place_one > reference - 12:
                    y_coor_offset = 0.05 * scale_range
                if reference <= self.edge_energy + 50:
                    ax.axvline(x=reference, color='black', linewidth=0.5)
                    ax.text(
                        x=reference,
                        y=self.df_xafs.der[self.df_xafs.der.idxmax()] + 0.095 * scale_range
                          + 0.025 * ((
                                         -1) ** ind) * scale_range + y_coor_offset,
                        # I use the -1**ind that the values of the reference
                        # points don't overlap
                        s=str(reference),
                        ha='center'
                    )

        plt.savefig(f'Plots/{self.name}.svg')

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
    i = Element(i)
    i.plot_edge()
