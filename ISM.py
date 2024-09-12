import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_csv('Data/RH data.csv')
data['depart'] = data["Attrition"].apply( lambda x: 1 if x=='Yes' else 0)
data['actif'] = data["Attrition"].apply( lambda x: 0 if x=='Yes' else 1)

NbrEmploye = f'{data.shape[0]}'
Departs = f"{data[data['Attrition']=='Yes'].shape[0]}"
Actifs = f"{data[data['Attrition']!='Yes'].shape[0]}"
taux_depart = f"{np.round(data[data['Attrition']=='Yes'].shape[0]/data.shape[0]*100,2)} %"
age_moyen = f"{int(np.round(data['Age'].mean(),0))}"

dep_dep = data.groupby(['Department'])["depart"].sum().reset_index()
fig_pie = px.pie(dep_dep,names='Department',values='depart',title= "Repartition des employes par Departement")




def tranche_ag(value):
    if value<10:
        return "0-20"
    elif value >=20 and value<30:
        return "20-30"
    elif value>=30 and value<40:
        return "30-40"
    elif value >= 40 and value <50:
        return "40-50"
    else:
        return "50 et plus"

data["tranche_age"] = data["Age"].apply(lambda x: tranche_ag(x))

df_ag = data.groupby('tranche_age').sum()['depart'].reset_index()
bar_fig = px.bar(df_ag,x='tranche_age',y='depart', title= "Nombre de departs par tranche d'age")
bar_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

# Creation de la heatmap
tableau = pd.pivot_table(data,values='Employee Count', index= 'Job Role',columns="Job Satisfaction", aggfunc='sum')
heatmap = px.imshow(tableau,color_continuous_scale=px.colors.sequential.Blues_r,text_auto=True, title= "Nombre d'employes par Roles et Satisfaction")
heatmap.update_layout(plot_bgcolor='rgba(0,0,0,0)')


dep_field = data.groupby('Education Field')['depart'].sum().reset_index()
bar2 = px.bar(dep_field, y = "Education Field", x= "depart",text_auto=True,title= "Nombre de departs par fillière")
bar2.update_layout(plot_bgcolor='rgba(0,0,0,0)')

# Creation des Pie chart avec un Hole

list_age = sorted(data['CF_age band'].unique().tolist())
list_age.insert(0,list_age.pop(4))
plots = make_subplots(rows=1,cols=len(list_age),specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
plots = make_subplots(rows=1,cols=len(list_age),specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
for i,ag in enumerate(list_age):
    f = px.pie(data[data['CF_age band']==ag],values='depart',names='Gender', labels='depart',hole=0.5,title='Babou')
    for tt in f.data:
        plots.add_trace(tt,row=1,col=(i+1))
    plots.add_annotation(dict(text=ag, x=(2.05* i + 1) / 10-0.01, y=-0.08, font_size=20, showarrow=False, xref='paper', yref='paper', xanchor='center', yanchor='middle'))
    plots.add_annotation(dict(text=f"{data[data['CF_age band']==ag].shape[0]}", x=(2.05* i + 1) / 10-0.01, y=0.5, font_size=35, showarrow=False, xref='paper', yref='paper', xanchor='center', yanchor='middle',))
plots.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                  paper_bgcolor='rgba(0,0,0,0)',
                    title='Taux de depart par sex et par tranche d\'age')
def create_card(title,value):
    carte = dbc.Card(
        dbc.CardBody(
            [html.H2(title),
             html.P([value], style={'textAlign': 'center', 'fontSize': 24})]
        )
    )
    return carte

app = dash.Dash('__nam__',    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = html.Div([
    dbc.Row([
            dbc.Col([html.H1('ISM RH Dashboard')], width={'size':3, 'offset':4}),
            dbc.Col([dcc.Dropdown(id='edu',
                                 options=[{'label':x, 'value':x} for x in data["Education Field"].unique()],
                                 placeholder = 'Education'
                                 )],width={'size':2, 'offset':0}
                    ),
            # dbc.Col([dcc.Dropdown(id='dep',
            #                      options=[{'label':x, 'value':x} for x in data["Department"].unique()],
            #                      placeholder = 'Department'
            #                      )],width={'size':2, 'offset':0}
            #         )
            ]),
    html.Br(),
    dbc.Row([
        dbc.Col(id='val1',children=[create_card("Nbe Employer",NbrEmploye)], width={'size':2,'offset':1}),
        dbc.Col(id='val2',children=[create_card("Nbe Departs",Departs)], width={'size':2}),
        dbc.Col(id='val3',children=[create_card("Nbe Actifs",Actifs)], width={'size':2}),
        dbc.Col(id='val4',children=[create_card("Taux de depart",taux_depart)], width={'size':2}),
        dbc.Col(id='val5',children=[create_card("Age moyen",age_moyen)], width={'size':2})]
            )

    ,
    dbc.Row([
        dbc.Col(id='pie',children=[dcc.Graph(figure=fig_pie)], width={'size':3}),
        dbc.Col(id='bar',children=[dcc.Graph(figure=bar_fig)], width={'size':4}),
        dbc.Col(id='heat',children=[dcc.Graph(figure=heatmap)], width={'size':4})
    ]),
    dbc.Row([
        dbc.Col(id='bar2',children=[dcc.Graph(figure=bar2)], width={'size':4}),
        dbc.Col(id='plots',children=[dcc.Graph(figure=plots)], width={'size':8}),
    ])

])
@callback(
    [Output('val1','children'),
        Output('val2','children'),
        Output('val3','children'),
        Output('val4', 'children'),
        Output('val5', 'children'),],
        Input('edu','value')
        # Input('dep', 'value')
)

def update(dep):
    if not dep:
        NbrEmploye = f'{data.shape[0]}'
        Departs = f"{data[data['Attrition'] == 'Yes'].shape[0]}"
        Actifs = f"{data[data['Attrition'] != 'Yes'].shape[0]}"
        taux_depart = f"{np.round(data[data['Attrition'] == 'Yes'].shape[0] / data.shape[0] * 100, 2)} %"
        age_moyen = f"{int(np.round(data['Age'].mean(), 0))}"
    else:
        NbrEmploye = f'{data[data["Education Field"]==dep].shape[0]}'
        Departs = f"{data[data['Education Field']==dep]['depart'].sum()}"
        Actifs = f"{data[data['Education Field']==dep]['actif'].sum()}"
        taux_depart = f"{np.round(data[data['Education Field']==dep]['depart'].sum() / data[data['Education Field']==dep].shape[0] * 100, 2)} %"
        age_moyen = f"{int(np.round(data[data['Education Field']==dep]['Age'].mean(), 0))}"

    card1 = create_card("Nbe Employer", NbrEmploye)
    card2 = create_card("Nbe Departs",Departs)
    card3 = create_card("Nbe Actifs",Actifs)
    card4 = create_card("Taux de depart",taux_depart)
    card5 = create_card("Age moyen",age_moyen)


    return card1, card2,card3,card4,card5

if __name__ == '__main__':
    app.run(debug=True, port=8786)
