import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, ALL, callback
import numpy as np
import math

class Pairs_GO:
    def __init__(self, name, contacts, marker_args, mirror=True):
        self.name = name
        self.contacts = contacts
        self.m_color, self.m_size, self.m_symbol = marker_args
        self.m_line_width = 0.25 if 'x' == self.m_symbol else 0
        self.resid_i = self.contacts[:,0]
        self.resid_j = self.contacts[:,1]
        self.mirror = mirror
        if self.mirror:
            self.mirror_i = np.hstack((self.resid_i, self.resid_j))
            self.mirror_j = np.hstack((self.resid_j, self.resid_i))
            self.scatter = go.Scattergl(x=self.mirror_i, y=self.mirror_j, 
                                        mode='markers', marker_size=self.m_size, marker_color=self.m_color, marker_symbol=self.m_symbol, marker_line_width=self.m_line_width,
                                        name=self.name)
        else:
            self.scatter = go.Scattergl(x=self.resid_i, y=self.resid_j, 
                                        mode='markers', marker_size=self.m_size, marker_color=self.m_color, marker_symbol=self.m_symbol, marker_line_width=self.m_line_width,
                                        name=self.name)
    def update_pairs(self, cutoff):
        if self.mirror:
            self.scatter = go.Scattergl(x=self.mirror_i[:cutoff], y=self.mirror_j[:cutoff], 
                                        mode='markers', marker_size=self.m_size, marker_color=self.m_color, marker_symbol=self.m_symbol, marker_line_width=self.m_line_width,
                                        name=self.name)
        else:
            self.scatter = go.Scattergl(x=self.resid_i[:cutoff], y=self.resid_j[:cutoff], 
                                        mode='markers', marker_size=self.m_size, marker_color=self.m_color, marker_symbol=self.m_symbol, marker_line_width=self.m_line_width,
                                        name=self.name)
class Monomer_GO(Pairs_GO):
    def __init__(self, name, filepath, marker_args, mirror=True):
        super().__init__(name, np.unique(np.loadtxt(filepath), axis=0), marker_args, mirror)
class DI_GO(Pairs_GO):
    def __init__(self, name, filepath, marker_args, region_length=None, mirror=False):
        super().__init__(name, np.loadtxt(filepath), marker_args, mirror)
        if region_length is not None:
            self.region_length = region_length
        else:
            min_i = min(self.resid_i)
            min_j = min(self.resid_j)
            max_i = max(self.resid_i)
            max_j = max(self.resid_j)
            self.region_length = max(max_i, max_j) - min(min_i, min_j)

        self.max_len = self.region_length * 10
        self.tick_len = math.ceil(self.max_len / 1000)
        self.slider_ID = f'DI_slider_{name}'
        self.slider = dcc.Slider(min=0, max=self.max_len, step=self.tick_len, value=50, marks=None, id={"type": "DI_slider", "index": self.slider_ID}, updatemode='drag', tooltip={"placement": "bottom", "always_visible": True})
    def update_pairs(self, cutoff):
        return super().update_pairs(cutoff)

app = Dash(__name__)

# Set custom order to true if you want control over which layers are displayed on top
custom_order = True
# Some colors that are used in 
potential_colors_light = px.colors.qualitative.Light24.copy()
potential_colors_dark = px.colors.qualitative.Dark24.copy()
monomers = []
DI_pair_GOs = []



monomers.append(Monomer_GO('Cry1Ab Monomer', f"/Users/moleculego/Projects/BT_R1/Cry1Ab/Structural_Info/monomer_6dj4_allatom_8", [potential_colors_light.pop(0), 3, 'circle'], mirror=True))

#Add new contacts via appending to monomers or DI_pair_GOs. DI pairs are contacts with adjustable top n DI pairs (slider)
# The format is _GO(name, filepath, [color, size, shape], ...)

DI_pair_GOs.append(DI_GO("Cry1Ab Full3D DIs", f"Berliner_3D_align_ranked_matched.DI", [potential_colors_dark.pop(0), 5, 'x']))





app.layout = html.Div([
    #dcc.Slider(0, 2000, 1, value=50, marks=None, id='DI_slider', updatemode='drag', tooltip={"placement": "bottom", "always_visible": True}),
    html.Div([
        dcc.Graph(id='contact-map')
    ], style={"display" : "inline-block", "border": "2px solid powderblue", "width":"70%"}),
    html.Div(children=[
        html.Div([
            html.H3(DI_pair_GO.name), 
            DI_pair_GO.slider
        ]) for DI_pair_GO in DI_pair_GOs
    ], style={"display" : "inline-block", "border": "2px solid powderblue", "width":"25%", 'verticalAlign': 'top'}),
    html.Div([
            html.Div([
                html.H1("Monomeric Contacts Checklist"),
                dcc.Checklist(options=[monomer.name for monomer in monomers], id="monomer-checklist", value=[])
            ], style={"display" : "inline-block", "border": "2px solid powderblue", "width":"45%"}),
            html.Div([
                html.H1("DI Pairs Checklist"),
                dcc.Checklist(options=[DI_pair_GO.name for DI_pair_GO in DI_pair_GOs], id="di-pair-checklist", value=[])
            ], style={"display" : "inline-block", "border": "2px solid powderblue", "width":"45%"}),
    ])
])
@callback(
    Output('contact-map', 'figure'),
    Input('contact-map', 'relayoutData'),
    Input('monomer-checklist', 'value'),
    Input('di-pair-checklist', 'value'),
    Input({"type": "DI_slider", "index": ALL}, 'value')
)
def update_figure(relay_data, monomer_checklist, di_pair_checklist, slider_list):
    fig = go.Figure()
    fig.update_layout(width=800, height=700, autosize=False)

    for idx, slider_val in enumerate(slider_list):
        DI_pair_GOs[idx].update_pairs(slider_val)
    
    if custom_order:
        for monomer in monomers:
            if monomer.name in monomer_checklist:
                fig.add_trace(monomer.scatter)

        for DI_pair_GO in DI_pair_GOs:
            if DI_pair_GO.name in di_pair_checklist:
                fig.add_trace(DI_pair_GO.scatter)

    else:
        for monomer in monomers:
            fig.add_trace(monomer.scatter)
            if monomer.name in monomer_checklist:
                fig.update_traces(visible=True, selector=({'name': monomer.name}))
        for DI_pair_GO in DI_pair_GOs:
            fig.add_trace(DI_pair_GO.scatter)
            if DI_pair_GO.name in di_pair_checklist:
                fig.update_traces(visible=True, selector=({'name': DI_pair_GO.name}))

    if len(fig.data) > 0:
        y_mins = []
        y_maxs = []
        for trace_data in fig.data:
            y_mins.append(min(trace_data.y, default=0))
            y_maxs.append(max(trace_data.y, default=0))
        y_min = min(y_mins, default=0)
        y_max = max(y_maxs, default=0)
        fig.update_yaxes(range=[y_max, y_min])
    
    if relay_data and 'xaxis.range[0]' in relay_data:
        fig.update_xaxes(range=[relay_data["xaxis.range[0]"], relay_data["xaxis.range[1]"]])
    if relay_data and 'yaxis.range[0]' in relay_data:
        fig.update_yaxes(range=[relay_data["yaxis.range[0]"], relay_data["yaxis.range[1]"]])

    return fig


if __name__ == '__main__':
    app.run(debug=True)