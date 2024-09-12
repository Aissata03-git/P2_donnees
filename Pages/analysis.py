import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import matplotlib.pyplot as plt
global data

dash.register_page(__name__, name="analysis",path="/analysis", order=1)
data = pd.read_csv('Data/RH data.csv')
data.drop(columns=['-2','0'],axis=1,inplace=True)
data['depart'] = data['Attrition'].apply(lambda t: 1 if t=='Yes' else 0)

NbrEmploye = f'{data.shape[0]}'
Departs = f"{data[data['Attrition']=='Yes'].shape[0]}"
Actifs = f"{data[data['Attrition']!='Yes'].shape[0]}"
taux_depart = f"{np.round(data[data['Attrition']=='Yes'].shape[0]/data.shape[0]*100,2)} %"
age_moyen = f"{int(np.round(data['Age'].mean(),0))}"

pie_fig = px.pie(data,values='depart',names='Department',color_discrete_sequence=px.colors.sequential.Blues_r,
             labels='depart',title='Depart par Departement')
pie_fig.update_traces(textinfo='value,percent',textposition='outside')
pie_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                  paper_bgcolor='rgba(0,0,0,0)')

gender_fig = px.bar(data,'Employee Number','Gender',color='Gender', title='Repartition des Clien par genre')
gender_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                  paper_bgcolor='rgba(0,0,0,0)')

def age_group(N):
    a = min(data['Age'])
    b = max(data['Age'])
    p = (b-a)/(N-1)
    group =  data['Age'].apply(lambda x: next((str(round(a + (k-1)*p)) + '-' + str(round(a + k*p)) for k in range(N+1) if x in range(round(a + (k-1)*p), round(a + k*p)+1)), 'out'))
    return group
data['group']=age_group(10)
df_age = data.groupby('group').count()['Employee Number'].reset_index()
age_fig = px.bar(df_age,'group','Employee Number',color_continuous_scale=px.colors.sequential.Blues_r)
age_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                  paper_bgcolor='rgba(0,0,0,0)')
tableau = pd.pivot_table(data,values='Employee Count',index='Job Role',columns='Job Satisfaction',aggfunc='sum',#margins=True,
                             # margins_name='Total'
                        )
heat = px.imshow(tableau,color_continuous_scale=px.colors.sequential.Blues_r[::-1], text_auto=True)
heat.update_layout(xaxis=dict(side='top',dtick=1 ,  showgrid=True),
    coloraxis_showscale=False)
heat.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                  paper_bgcolor='rgba(0,0,0,0)')

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
    card = dbc.Card(
        dbc.CardBody([
            html.H4(title, style={'textAlign': 'center'},className="ms-2 text-primary"),
            html.P(value,
                   style={'textAlign': 'center',
                          # 'color': 'black',
                          'fontSize': 24},className="ms-2 text-primary"
                   )]),
        # color="#D8D3D3"
    )
    return card

card1 = create_card( "Total Employés", NbrEmploye)
card2 = create_card( "Nbre Départs", Departs)
card3 = create_card("Employés Actifs", Actifs,)
card4 = create_card("Taux de Departs", taux_depart)
card5 = create_card("Age Moyen", age_moyen)

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(
                            [dbc.NavbarBrand(
                                "RH Dashboard",
                                className="ms-2 text-primary",
                            )], width={'size':2 ,'offset':0}
                        ),),
        dbc.Row(
            [dbc.Col(id='val1',children=[card1]),
            dbc.Col(id='val2',children=[card2]),
            dbc.Col(id='val3',children=[card3]),
            dbc.Col(id='val4',children=[card4]),
            dbc.Col(id='val5',children=[card5])]
        ),
        html.Br(),
        dbc.Row(
                [dbc.Col([dcc.Graph(id='pie',figure=pie_fig)],width={'size':3}),
                dbc.Col([dcc.Input(id='N',value=10,type="number",placeholder='age group'),dcc.Graph(id='age',figure=age_fig)],width={'size':5}),
                dbc.Col([dcc.Graph(id='heat',figure=heat)],width={'size':4}),]
        ),
        html.Br(),
        dbc.Row(
            [dbc.Col([dcc.Graph(id='sex', figure=gender_fig)],width={'size':3}),
             dbc.Col([dcc.Graph('sub',figure=plots)])]
        )
    # Add more components here
],class_name="mt-5  justify-content-center"
)

@callback(
    Output('val1','children'),
     Output('val2','children'),
     Output('val3','children'),
     Output('val4','children'),
     Output('val5','children'),
     Output('pie','figure'),
     Output('heat','figure'),
     Output('sex','figure'),
     Output('sub','figure'),
     Output('age','figure'),
    Input('education','value'),
    Input('N','value')

)

def update(val,N):
    data = pd.read_csv('Data/RH data.csv')
    data.drop(columns=['-2', '0'], axis=1, inplace=True)
    data['depart'] = data['Attrition'].apply(lambda t: 1 if t == 'Yes' else 0)
    data['group'] = age_group(10)
    if val:
        data = data[data['Education Field']==val]
    if N:
        data['group'] = age_group(N)
    NbrEmploye = f'{data.shape[0]}'
    Departs = f"{data[data['Attrition'] == 'Yes'].shape[0]}"
    Actifs = f"{data[data['Attrition'] != 'Yes'].shape[0]}"
    taux_depart = f"{np.round(data[data['Attrition'] == 'Yes'].shape[0] / data.shape[0] * 100, 2)} %"
    age_moyen = f"{int(np.round(data['Age'].mean(), 0))}"

    pie_fig = px.pie(data, values='depart', names='Department', color_discrete_sequence=px.colors.sequential.Blues_r,
                     labels='depart', title='Depart par Departement')
    pie_fig.update_traces(textinfo='value,percent', textposition='outside')
    pie_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                          paper_bgcolor='rgba(0,0,0,0)')

    gender_fig = px.bar(data, 'Employee Number', 'Gender', color='Gender', title='Repartition des Clien par genre')
    gender_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                             paper_bgcolor='rgba(0,0,0,0)')
    card1 = create_card("Total Employés", NbrEmploye)
    card2 = create_card("Nbre Départs", Departs)
    card3 = create_card("Employés Actifs", Actifs, )
    card4 = create_card("Taux de Departs", taux_depart)
    card5 = create_card("Age Moyen", age_moyen)

    df_age = data.groupby('group').count()['Employee Number'].reset_index()
    age_fig = px.bar(df_age, 'group', 'Employee Number', color_continuous_scale=px.colors.sequential.Blues_r)
    age_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                          paper_bgcolor='rgba(0,0,0,0)')
    tableau = pd.pivot_table(data, values='Employee Count', index='Job Role', columns='Job Satisfaction', aggfunc='sum',
                             # margins=True,
                             # margins_name='Total'
                             )
    heat = px.imshow(tableau, color_continuous_scale=px.colors.sequential.Blues_r[::-1], text_auto=True)
    heat.update_layout(xaxis=dict(side='top', dtick=1, showgrid=True),
                       coloraxis_showscale=False)
    heat.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                       paper_bgcolor='rgba(0,0,0,0)')

    list_age = sorted(data['CF_age band'].unique().tolist())
    idx = len(list_age)-1
    list_age.insert(0, list_age.pop(idx))
    col = len(list_age)
    spec = [{'type': 'domain'} for i in range(len(list_age))]
    plots = make_subplots(rows=1, cols=col, specs=[
        spec])
    # plots = make_subplots(rows=1, cols=len(list_age), specs=[
    #     [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])
    for i, ag in enumerate(list_age):
        f = px.pie(data[data['CF_age band'] == ag], values='depart', names='Gender', labels='depart', hole=0.5,
                   title='Babou')
        for tt in f.data:
            plots.add_trace(tt, row=1, col=(i + 1))
        plots.add_annotation(
            dict(text=ag, x=(2.05 * i + 1) / 10 - 0.01, y=-0.08, font_size=20, showarrow=False, xref='paper',
                 yref='paper', xanchor='center', yanchor='middle'))
        plots.add_annotation(
            dict(text=f"{data[data['CF_age band'] == ag].shape[0]}", x=(2.05 * i + 1) / 10 - 0.01, y=0.5, font_size=35,
                 showarrow=False, xref='paper', yref='paper', xanchor='center', yanchor='middle', ))
    plots.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                        paper_bgcolor='rgba(0,0,0,0)',
                        title='Taux de depart par sex et par tranche d\'age')
    df_age = data.groupby('group').count()['Employee Number'].reset_index()
    age_fig = px.bar(df_age, 'group', 'Employee Number', color_continuous_scale=px.colors.sequential.Blues_r)
    age_fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color
                          paper_bgcolor='rgba(0,0,0,0)')
    return card1,card2,card3,card4,card5,pie_fig,heat,gender_fig,plots,age_fig