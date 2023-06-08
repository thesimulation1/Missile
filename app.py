from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import openpyxl

# from dashapp import server as application

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB, dbc.icons.FONT_AWESOME],
)

#styling





#load dataset
df = pd.read_excel('missle.xlsx')

facility_list = df['Facility Name'].unique()
#app layout

app.layout = dbc.Container([
    dbc.Row(

    html.H2(children='North Korean Missle Launch',
            className="text-center bg-primary text-white p-2",
            ),

    ),
    dbc.Row(
        [
    dbc.Col(
    dbc.Tabs(
        [
            dbc.Tab(dcc.Markdown('''

                        **Introduction**


                        The Belt and Road Initiative (BRI) is a global development strategy proposed by the Chinese government in 2013. 
                        It aims to enhance connectivity and promote economic cooperation between countries in Asia, Europe, Africa, and beyond. 
                        The initiative consists of two main components: the Silk Road Economic Belt and the 21st Century Maritime Silk Road.
                        The Silk Road Economic Belt refers to the land-based infrastructure network that seeks to revive the ancient Silk Road 
                        trading routes. It involves the construction of roads, railways, pipelines, and other transportation infrastructure across 
                        Central Asia, the Middle East, and Europe. These projects aim to facilitate trade and boost economic integration among 
                        participating countries. The 21st Century Maritime Silk Road focuses on developing maritime infrastructure and connectivity. It aims to improve 
                        port facilities, construct shipping lanes, and strengthen maritime cooperation between countries in the Indo-Pacific region, 
                        including Southeast Asia, South Asia, and East Africa. The initiative seeks to promote maritime trade and maritime cultural 
                        exchanges. The Belt and Road Initiative emphasizes economic cooperation and seeks to address infrastructure gaps in developing countries. 
                        It aims to foster regional integration, enhance trade, and spur economic growth by connecting markets and facilitating the 
                        flow of goods, capital, and information. It also aims to promote people-to-people exchanges, cultural understanding, and 
                        sustainable development.


                        **_"Since the inauguration of China’s Belt and Road Initiative in 2013, its bold vision has become China’s most important global 
                        economic and foreign policy instrument."_**






                        **Articles**
                        * [China's Massive Belt and Road Initiative](https://www.cfr.org/backgrounder/chinas-massive-belt-and-road-initiative)
                        * [What is China's Belt and Road Initiative?](https://www.chathamhouse.org/2021/09/what-chinas-belt-and-road-initiative-bri)
                        * [China’s $900 billion New Silk Road. What you need to know](https://www.weforum.org/agenda/2017/06/china-new-silk-road-explainer/)
                        * [How China’s Belt and Road Initiative is faring](https://www.gisreportsonline.com/r/belt-road-initiative/)


                        '''),
                    tab_id="tab1", label="Belt and Road Initiative"),

            dbc.Tab(
                [
                html.H4(children="Select Facilities"),
                dcc.Dropdown(id='facility_name',
                             value=['Tonghae Satellite Launching Ground', 'Chihari Missile Base',
                                    'Kittaeryong Missile Base'],
                             options=['Tonghae Satellite Launching Ground', 'Chihari Missile Base',
                                    'Kittaeryong Missile Base', 'Sohae Satellite Launching Station',
                                    'North Wonsan', 'Wonsan Kalma International Airport',
                                    'Sunchon Airbase', 'Hwangju', 'Kaesong', 'Unknown', 'Nampo',
                                    'Sinpo Shipyard', 'Panghyon Airbase', 'Kusong Testing Ground',
                                    'Pukchang Airfield'], multi=True, placeholder='Choose X Indicator...'
                             ),


                    ],

            tab_id="tab2", label="Data Set Description"
            ),
            dbc.Tab(
                dcc.Markdown('''

                        **Full Description**

                        AidData’s Global Chinese Development Finance Dataset, Version 2.0. records the known universe of projects (with development, commercial, or representational intent) supported by official financial and in-kind commitments (or pledges) from China from 2000-2017, with implementation details covering a 22-year period (2000-2021). The dataset captures 13,427 projects worth $843 billion financed by more than 300 Chinese government institutions and state-owned entities across 165 countries in every major region of the world. AidData systematically collected and quality-assured all projects in the dataset using the 2.0 version of our Tracking Underreported Financial Flows (TUFF) methodology.

                        **Funding**: This dataset was made possible through a cooperative agreement (AID-OAA-A-12-00096) between USAID's Global Development Lab and AidData at William and Mary under the Higher Education Solutions Network (HESN) Program. We also gratefully acknowledge financial support from the William and Flora Hewlett Foundation, the Ford Foundation, and the Smith Richardson Foundation. We also acknowledge that previous versions of the dataset would not have been possible without generous financial support from the John D. and Catherine T. MacArthur Foundation, Humanity United, United Nations University-WIDER, the Academic Research Fund of Singapore’s Ministry of Education, and the German Research Foundation.

                        [AidData’s Global Chinese Development Finance Dataset](https://www.aiddata.org/data/aiddatas-global-chinese-development-finance-dataset-version-2-0)
                        '''),
                tab_id="tab3", label="Data Set Description"),

        ],
        id="tabs",
        active_tab="tab1",
    ), width=3,lg=3
    ),


dbc.Col(


dcc.Graph(
            id='map',
            figure={}
                        ),width=9,lg=9

),
]
),



],
    fluid=True,

)

@app.callback(Output('map', 'figure'),
              Input('facility_name', 'value'))
def display_generic_map_chart(facility):
    dff = df.copy()
    if facility is None or len(facility) == 0:
        raise PreventUpdate

    else:
        df1 = dff[dff['Facility Name'].isin(facility)]
        #df_year = df1.groupby(['Commitment Year', 'Recipient', ])[indicator].sum().reset_index()
        fig = px.scatter_geo(df1, lat="Facility Latitude", lon="Facility Longitude", color='Missile Type', title='f by year')
        # fig.layout.coloraxis.colorbar.title =\'indicator'
        fig.update_layout(
            title_x=0.5,
            annotations=[dict(
                x=0.55,
                y=-0.1,
                xref='paper',
                yref='paper',
                text='Source: <a href="https://www.aiddata.org/data/aiddatas-global-chinese-development-finance-dataset-version-2-0">\
                            AidData A Research Lab at William and Mary</a>',
                showarrow=False
            )]
        )
        return fig




if __name__ == "__main__":
    app.run_server(debug=True)