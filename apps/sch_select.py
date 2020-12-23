### page 2 of app ###
#### scl_select ###

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib
from app import app

import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc



# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()



##### Import the data sets #########

boards_new_old_df = pd.read_csv(DATA_PATH.joinpath("active_case_data_school_board_new_old.csv"))
boards_students_df = pd.read_csv(DATA_PATH.joinpath("ONT_board_schools_students.csv"))

## Drop the previous index columns [0]
boards_students_df.drop(boards_students_df.columns[0], axis = 1, inplace = True)
boards_new_old_df.drop(boards_new_old_df.columns[0], axis = 1, inplace = True)

## II. ONTARIO SCHOOLS with COVID-19 CASES by DATE
url = "https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/8b6d22e2-7065-4b0f-966f-02640be366f2/download/schoolsactivecovid.csv"
try:
    df_active = pd.read_scv(url, encoding='latin-1')
except:
    df_active = pd.read_csv(url)

### Change 'reported_date' to date time and drop collected_date
df_active["reported_date"] = pd.to_datetime(df_active["reported_date"])
df_active.drop("collected_date", axis=1, inplace=True)

## Change the name of column 'school', to 'School' and 'total_confirmed_cases' to 'Active Cases'
df_active = df_active.rename({"school": "School", "total_confirmed_cases":"Active Cases"}, axis=1)

#### CLEAN UP THE ACTIVE DATA SET #####
## Change the name of one catholique french elementary school ##
cass = df_active[df_active.School.str.contains('taire catholique de Casselman')]
cass_index = cass.index
df_active.at[cass_index, 'School'] = 'Catholic Elementary School de Casselman'


## Clean the active data frame board name entries ##
algo_index = df_active[df_active["school_board"].str.contains("Algonquin Lakeshore Catholic District School Board")].index
df_active.at[algo_index, "school_board"] = "Algonquin and Lakeshore Catholic District School Board"

peel_index = df_active[df_active["school_board"].str.contains("Dufferin Peel Catholic District School Board")].index
df_active.at[peel_index, "school_board"] = "Dufferin-Peel Catholic District School Board"

ham1_index = df_active[df_active["school_board"].str.contains("Hamilton Wentworth Catholic District School Board")].index
df_active.at[ham1_index, "school_board"] = "Hamilton-Wentworth Catholic District School Board"

ham2_index = df_active[df_active["school_board"].str.contains("Hamilton Wentworth DSB")].index
df_active.at[ham2_index, "school_board"] = "Hamilton-Wentworth District School Board"

ham3_index = df_active[df_active["school_board"].str.contains("Hamilton Wentworth District School Board")].index
df_active.at[ham3_index, "school_board"] = "Hamilton-Wentworth District School Board"

kee_index = df_active[df_active["school_board"].str.contains("Keewatin Patricia District School Board")].index
df_active.at[kee_index, "school_board"] = "Keewatin-Patricia District School Board"

ea_index = df_active[df_active["school_board"].str.contains("KidsAbility School Authority")].index
df_active.at[ea_index, "school_board"] = "KidsAbility Education Authority"

ott_index = df_active[df_active["school_board"].str.contains("Ottawa Catholic School Board")].index
df_active.at[ott_index, "school_board"] = "Ottawa Catholic District School Board"

peter1_index = df_active[df_active["school_board"].str.contains("Peterborough Victoria Northum Clarington Catholic District School Board")].index
df_active.at[peter1_index, "school_board"] = "Peterborough Victoria Northumberland & Clarington Catholic District School Board"

peter2_index = df_active[df_active["school_board"].str.contains("Peterborough Victoria Northumberland & Clarington Catholic Di")].index
df_active.at[peter2_index, "school_board"] = "Peterborough Victoria Northumberland & Clarington Catholic District School Board"

prov_index = df_active[df_active["school_board"].str.contains("Provincial and Demonstration School")].index
df_active.at[prov_index, "school_board"] = "Provincial and Demonstration Schools"

prov2_index = df_active[df_active["school_board"].str.contains("Provincial Demonstration School")].index
df_active.at[prov2_index, "school_board"] = "Provincial and Demonstration Schools"

st_index = df_active[df_active["school_board"].str.contains("St Clair Catholic District School Board")].index
df_active.at[st_index, "school_board"] = "St Clair Catholic District School Board"

peel_index = df_active[df_active["school_board"].str.contains("Peel District School")].index
df_active.at[peel_index, "school_board"] = "Peel District School Board"

peel2_index = df_active[df_active["school_board"].str.contains("Peel District School ")].index
df_active.at[peel2_index, "school_board"] = "Peel District School Board"

df_active['municipality'] = df_active['municipality'].str.replace('\n', '')
df_active['municipality'] = df_active['municipality'].str.replace('\t', '')
df_active['municipality'] = df_active['municipality'].str.strip()

whitby_clean = df_active[df_active['municipality'].str.contains('.Whitby..')]
whitby_index = whitby_clean.index
df_active.at[whitby_index, 'municipality'] = 'Whitby'

ajax_clean = df_active[df_active['municipality'].str.contains('.Ajax..')]
ajax_index = ajax_clean.index
df_active.at[ajax_index, 'municipality'] = "Ajax"

### Filter the active data set for cases occurring on the last_reported datetime
df_active_now = df_active[df_active.reported_date == max(df_active.reported_date)]

municipalities = df_active_now.municipality.unique()
municipalities.sort()


#Drop Board Site from active_now:
board_site_index = df_active_now[df_active_now.School.str.contains('Board Site')].index
if len(board_site_index) > 0:
    df_active_now = df_active_now.drop(board_site_index)

#### todays date ####
today = datetime.datetime.now()
today = today.strftime("%B %d, %Y")


##### TABLE TO GRAPH #####
top_10_schools = df_active_now.groupby('School')['Active Cases'].sum().reset_index().sort_values(by = "Active Cases", ascending = False)
top_10_schools = top_10_schools[top_10_schools["Active Cases"] >= 5]
# top_10_schools = top_10_schools.rename({"total_confirmed_cases" : "Active Cases"}, axis = 1)
top_10_schools.reset_index(inplace = True)


fig13 = go.Figure(data=[
    go.Table(
        columnorder = [1, 2],
        columnwidth = [200, 50],
        header=dict(values=[['<b>SCHOOL</b>'],['<b>CASES</b>']],
                line_color='#F8F9F9',
                fill_color='#04ADBF',
                align=['left','center'],
                font = dict(color='#154360', size = 14, family = "Helvetica"),
                height = 25
                ),
        cells=dict(values= [top_10_schools[k].tolist() for k in top_10_schools.columns[1:]], # 2nd column
               line_color='#F8F9F9',
               fill_color=[['#F5F5F5','white']* len(top_10_schools)],
               align=['left', 'center'],
               font = dict(color = '#595959', size = 14, family = "Helvetica"),
               height = 25)
    )])
fig13.update_layout(autosize=False, width = 430, height = 450,
                    margin=dict(
                    l=10,
                    r=10,
                    b=20,
                    t=20,
                    pad=4))
fig13.layout.plot_bgcolor = '#F2F2F2'
fig13.layout.paper_bgcolor = '#F2F2F2'



layout = html.Div(
    html.Div(
        children = [

        html.Div(
            [
            # Top Row of Dashboard - Title
            html.Div(
            [
            html.H1(children = "COVID-19 CASES IN ONTARIO SCHOOLS",
                style = {
                    'textAlign': 'center',
                    'color' : 'white',
                    'padding-top' : '20px',
                    #'padding-left': '20px',
                    'font-size' : '45px',
                    #'margin-top' : '10px',
                    'font-weight': 'bold',
                    #'font-family' : 'Monaco',
                    #'font-variant-caps': 'small-caps',
                }),

            html.P(children = f" LAST UPDATED:  {max(df_active.reported_date).date()}",
                style = {
                    'textAlign': 'center',
                    'color': '#F2F2F2',
                    #'padding-left' : '30px',
                    'font-size' : '20px',
                    #'font-weight' : 'normal',
                    #'font-family' : 'Monaco',
                    'font-variant-caps': 'small-caps'
                }),
            ], className = 'row',
               style = {
                        'backgroundColor' : '#04ADBF',
                        'height' : '70%'
                        })
            ]
            ),


            html.Div([
                html.Label("SELECT MUNICIPALITY TO VIEW CASES ON RIGHT:",
                           style = {"fontSize" : "18px", "color" : "#595959", 'font-weight' : 'bold',
                                    "padding" : "20px", "fontFamily" : "Helvetica", "border-left" : 'medium solid white'}),
                #html.P("MUNICIPALITY:", style = {"fontSize" : "18px", "color" : "#595959", "padding-left" : "20px", "padding-bottom" : "10px"}),
                dcc.Dropdown(
                    id = "munic-input",
                    style = {'width' : '80%',  "padding-left" : "20px",  "border-left" : 'medium solid white'},
                    options = [{'label': x, 'value': x} for x in municipalities],
                    value= "Toronto"),
                html.Label("SELECT SCHOOL FROM ABOVE MUNICIPALITY TO VIEW CASES ON RIGHT:",
                     style = {"fontSize" : "18px", "color" : "#595959", "font-weight": "bold", "padding" : "20px", "fontFamily" : "Helvetica", "border-left" : 'medium solid #04ADBF'}),
                dcc.Dropdown(
                    id = "school-input",
                    style = {"width" : "80%", "padding-left" : "20px", "padding-bottom" : "20px",  "border-left" : 'medium solid #04ADBF'},
                    options = [{'label' : 'William G Miller Junior Public School', 'value' : 'William G Miller Junior Public School'}],
                    value = 'William G Miller Junior Public School'
                    ),

                # html.Div(
                #   html.P("Where will this land")
                #  ),
                    ], className = "six columns",
                       style = {"backgroundColor" : "#F2F2F2", 'border-radius': '5px',
                                                        'box-shadow': '5px 5px 5px grey',
                                                        'background-color': '#F2F2F2',
                                                        'border' : '1px solid #BFBFBF',
                                                        'padding' : '5px', "margin" : "20px", "margin-left" : "40px"}),



            html.Div(
                [
                html.Label(id = "breakdown", children = f"COVID-19 Case Breakdown on {max(df_active.reported_date).date()}",
                            style = {"fontSize" : "16px", "font-weight" : "bold", "padding" : "10px", "padding-left" : "20px", "fontFamily" : "Helvetica", 'color' : '#595959'}
                        ),

                html.Label("i. Data obtained from the Government of Ontario website 'Schools COVID-19 Data'",
                            style = {"fontSize" : "12px", "padding-left" : "10px", "fontFamily" : "Helvetica"}),
                            ],
                        className = "six columns",
                        style = {"backgroundColor" : "#F2F2F2", 'border-radius': '5px',
                                'box-shadow': '5px 5px 5px grey',
                                'background-color': '#F2F2F2',
                                'border' : '1px solid #BFBFBF',
                                'padding' : "5px", "margin-left" : "10px", "width" : "44%", "margin-top" : "20px", "margin-bottom" : "20px"}
                            ),

            html.Div(
            [
                html.Div([
                            dcc.Graph(
                                id = "mun_schools",
                                figure = {},
                                style = {
                                    'width' : '15vh', 'height' : '12vh',
                                    'background' : '#04ADBF',
                                    'padding' : '5px',
                                    'border-radius' : '5px',
                                    'box-shadow': '5px 5px 5px grey',
                                    'border' : '1px solid #BFBFBF',
                                    #'margin-bottom' : '20px'
                                    }),
                                    ], className = "one columns", style = {"margin" : "10px", "width" : "10%"}),

                html.Div([
                            dcc.Graph(
                                id = "mun_cases",
                                figure = {},
                                style = {
                                    'width' : '15vh', 'height' : '12vh',
                                    #'margin-bottom' : '20px',
                                    'background' : '#04ADBF',
                                    'padding' : '5px',
                                    #'border-bottom' : '4px solid #85C1E9',
                                    #'border-top' : '4px solid #85C1E9'
                                    #'border-left' : '4px solid #85C1E9',
                                    'border-radius' : '5px',
                                    'box-shadow': '5px 5px 5px grey',
                                    'border' : '1px solid #BFBFBF'}
                                ),
                                ], className = "one columns", style = {"margin" : "10px", "width" : "10%"}),

                html.Div([
                           dcc.Graph(
                               id = "student",
                               figure = {},
                               style = {
                                   'width' : '15vh', 'height' : '12vh',
                                   #'margin-bottom' : '30px',
                                   #'margin-top' : '10px',
                                   #'margin-left' : '10px',
                                   #'margin-right' : '20px',
                                   'background' : '#F2F2F2',
                                   'padding' : '5px',
                                   'border-radius' : '5px',
                                   'box-shadow': '5px 5px 5px grey',
                                   'border' : '1px solid #BFBFBF'}
                                  )
                                  ], className = "one columns", style = {"margin" : "10px", "width" : "10%"}),

                html.Div([
                            dcc.Graph(
                                id = 'staff',
                                figure = {},
                                style = {
                                    'width' : '15vh', 'height' : '12vh',
                                    'padding' : '5px',
                                    'border-radius' : '5px',
                                    'box-shadow': '5px 5px 5px grey',
                                    'border' : '1px solid #BFBFBF',
                                    'background' : '#F2F2F2', "left-margin" : "60px"}
                                    )
                                ], className = "one columns", style = {"margin" : "10px", "width" : "10%"})

                        ], className = "row", style = {}),

            html.Div(
            [

                html.Div(
                [
                    html.Label(id = "graph1", children = "% of Schools in School Board with at least 1 Confirmed COVID-19 Case",
                                style = {"padding" : "5px", "fontFamily" : "Helvetica", "font-weight" : "bold", "size" : 14, "margin=left" : "20px", 'color' : '#595959'}),
                    dcc.Graph(
                        id = "perc_schools",
                        figure = {},

                ),

                html.P("ii. Data obtained from Ontario Governments Website \n 'Ontario Public School Contact Information', updated Dec 2020",
                    style = {"fontSize" : "11px", "fontFamily" : "Helvetica",'color' : '#595959', 'padding-left' : '10px' }),

                ], className = "four columns",
                    style = {'background' : '#F2F2F2',
                            'padding' : '5px',
                            #'border-bottom' : '4px solid #85C1E9',
                            #'border-top' : '4px solid #85C1E9'
                            #'border-left' : '4px solid #85C1E9',
                            'border-radius' : '5px',
                            'box-shadow': '5px 5px 5px grey',
                            'border' : '1px solid #BFBFBF'}
                ),

                html.Div(
                [
                    html.Label("COVID-19 Cases per 100k Students Based on 5 Day Moving Average",
                                style = {"padding" : "5px", "fontFamily" : "Helvetica", "font-weight" : "bold", "size" : 14, "margin=left" : "20px", 'color' : '#595959' }),
                    dcc.Graph(
                        id = "cases-per",
                        figure = {}

                    ),

                    html.P("iii. Data obtained from Ontario Governments Website \n 'Ontario Public Schools Enrolment', 2019-2020 academic year",
                        style = {"fontSize" : "11px", "fontFamily" : "Helvetica",'color' : '#595959', 'padding-left' : '10px' }),



                ], className = "four columns",
                   style = {'background' : '#F2F2F2',
                     'padding' : '5px',
                     #'border-bottom' : '4px solid #85C1E9',
                     #'border-top' : '4px solid #85C1E9'
                     #'border-left' : '4px solid #85C1E9',
                     'border-radius' : '5px',
                     'box-shadow': '5px 5px 5px grey',
                     'border' : '2px solid #BFBFBF', "margin-left" : "20px"}
                ),

                html.Div(
                [
                    html.Label("Ontario Schools with >= 5 Active, Confirmed COVID-19 Cases",
                                style = {"padding" : "5px", "fontFamily" : "Helvetica", "font-weight" : "bold", "margin-left" : "10px", 'color' : '#595959', 'size' : 14 }),
                    dcc.Graph(
                    id = "table",
                    figure = fig13,
                    ),

                    html.P("")
                ], className = "four columns",
                   style = {'background' : '#F2F2F2',
                            'padding' : '5px',
                            #'border-bottom' : '4px solid #85C1E9',
                            #'border-top' : '4px solid #85C1E9'
                            #'border-left' : '4px solid #85C1E9',
                            'border-radius' : '5px',
                            'box-shadow': '5px 5px 5px grey',
                            'border' : '1px solid #F2F2F2', "margin-left" : "50px", "width" : "30%"}
                ),
                ], className = "row", style = {"margin-left" : "40px", "margin-top" : "20px", "margin-right" : "1px"}
                ),

        html.Div([
            html.Footer(""),
            html.A("I. Source", href="https://data.ontario.ca/dataset/summary-of-cases-in-schools",
                        target = "_blank",
                        style = {
                            'textAlign' : 'left',
                            'color' :  '#D9D9D9',
                            #'padding-left' : '30px',
                            'font-size' : '12px',
                            'font-variant-caps': 'small-caps'
                        }),

            html.Label("Ontario Schools Covid-19 Dataset",
                        style = {
                            'textAlign' : 'left',
                            'color' :  '#D9D9D9',
                            #'padding-left' : '30px',
                            'font-size' : '12px',
                            'font-variant-caps': 'small-caps'}),

            html.A("ii. Source", href= "https://data.ontario.ca/dataset/ontario-public-school-contact-information",
                    target = "_blank",
                    style = {
                        'textAlign' : 'center',
                        'color' :  '#D9D9D9',
                        #'padding-left' : '30px',
                        'font-size' : '12px',
                        'font-variant-caps': 'small-caps'}),

            html.Label("Ontario Public Schools Contact Information Dataset:",
                    style = {
                        'textAlign' : 'left',
                        'color' :  '#D9D9D9',
                        #'padding-left' : '30px',
                        'font-size' : '12px',
                        'font-variant-caps': 'small-caps'}),



            html.A("iii. Source", href= "https://data.ontario.ca/dataset/ontario-public-schools-enrolment",
                    target = "_blank",
                    style = {
                        'textAlign' : 'left',
                        'color' :  '#D9D9D9',
                        #'padding-left' : '30px',
                        'font-size' : '12px',
                        'font-variant-caps': 'small-caps'}),

            html.Label("Ontario Public Schools Enrolment Dataset:",
                    style = {
                        'textAlign' : 'left',
                        'color' :  '#D9D9D9',
                        #'padding-left' : '30px',
                        'font-size' : '12px',
                        'font-variant-caps': 'small-caps'}),

                ], className = "twelve columns", style = {"padding" : "15px",
                                'backgroundColor' : "#04ADBF", "margin-top" : "10px"}
                )





# End of Initial Div
], className = 'ten columns offset-by-one', style = {"backgroundColor" : "#D9D9D9"}

), style = {"backgroundColor" : "#D9D9D9", "fontFamily" : "Helvetica"}

)

################################ CALLBACK ############################################

# returns the number of schools based on the municipality entered
@app.callback(
     Output(component_id = "mun_schools", component_property =  "figure"),
     [Input(component_id = "munic-input", component_property = "value")])
def municipality_schools(municipality):
    schools_in_mun = df_active_now[df_active_now.municipality == municipality]["School"].nunique()
    figure = go.Figure()
    figure.add_trace(
     go.Indicator(
        mode = 'number',
        value = schools_in_mun,
        title = {"text" : " <br><span style = 'font-size: 1.0em; color:#595959'># SCHOOLS <br>WITH CASES</span>"},
        number = {"font" : {"size" : 42, "color" : "#04ADBF"}}))
    figure.update_layout(autosize=True,
                        margin=dict(
                        l=10,
                        r=10,
                        b=20,
                        t=50,
                        pad=4))
    figure.layout.plot_bgcolor = 'white'
    figure.layout.paper_bgcolor = 'white'
    return figure

# returns teh number of student cases based on the school selected
@app.callback(
     Output(component_id = 'student', component_property =  'figure'),
     [Input(component_id = "school-input", component_property = "value")])

def school_metric1(school):
    if len(school) > 0:
        students = (df_active_now[df_active_now["School"] == school].confirmed_student_cases.values)[0]
        figure = go.Figure()
        figure.add_trace(
            go.Indicator(
                mode = 'number',
                value = students,
                #delta = {'reference' : students},
                title = {"text" : " <br><span style = 'font-size: 1.0em; color:#FFFFFF'>STUDENT</span>"},
                number = {"font" : {"size" : 42, "color" : "white"}}))
        figure.layout.plot_bgcolor = '#04ADBF'
        figure.layout.paper_bgcolor = '#04ADBF'
        return figure

# returns the number of staff cases based on school selected
@app.callback(
     Output(component_id = 'staff', component_property =  "figure"),
     [Input(component_id = "school-input", component_property = "value")])

def school_metric2(school):
    staff = (df_active_now[df_active_now["School"] == school].confirmed_staff_cases.values)[0]
    figure = go.Figure()
    figure.add_trace(
        go.Indicator(
            mode = 'number',
            value = staff,
            #delta = {'reference' : staff},
            title = {"text" : " <br><span style = 'font-size: 1.0em; color:#FFFFFF'>STAFF</span>"},
            number = {"font" : {"size" : 42, "color" : "white"}}))
    figure.layout.plot_bgcolor = '#04ADBF'
    figure.layout.paper_bgcolor = '#04ADBF'
    return figure

# returns the number of cases in a select municipality
@app.callback(
     Output(component_id = "mun_cases", component_property =  "figure"),
     [Input(component_id = "munic-input", component_property = "value")])
def municipality_cases(municipality):
    cases = df_active_now[df_active_now.municipality == municipality]["Active Cases"].sum()
    figure = go.Figure()
    figure.add_trace(
        go.Indicator(
            mode = 'number',
            value = cases,
            title = {"text" : f" <span style = 'font-size: 1.0em; color:#595959'>CONFIRMED CASES IN <b><br> {municipality}:</span>"},
            number = {"font" : {"size" : 42, "color" : '#04ADBF'}}))
    figure.update_layout(autosize=True,
                        margin=dict(
                        l=10,
                        r=10,
                        b=20,
                        t=50,
                        pad=4))
    figure.layout.plot_bgcolor = 'white'
    figure.layout.paper_bgcolor = 'white'
    return figure


# returns a list of schools based on the municipality
@app.callback(
     Output(component_id = "school-input", component_property =  'options'),
     [Input(component_id = "munic-input", component_property = "value")])
def set_school_options(selected_municipality):
    schools = list(df_active_now[df_active_now["municipality"].str.contains(selected_municipality)]["School"].unique())
    schools.sort()
    return [{'label' : i, 'value' : i} for i in schools]


@app.callback(
     Output(component_id = "perc_schools", component_property =  "figure"),
     [Input(component_id = "munic-input", component_property = "value")])
def perc_graph(municipality):
    muni_boards = df_active_now[df_active_now["municipality"] == municipality]
    schools_per_board = muni_boards.groupby("school_board")["School"].nunique().reset_index()
    merge1 = pd.merge(boards_students_df, boards_new_old_df, how = 'left', left_on = 'Board Name', right_on = 'school_board_new')
    merge2 = pd.merge(schools_per_board, merge1, how = 'left', left_on = 'school_board', right_on = 'school_board')
    if municipality == "Toronto":
        merge2.at[0, 'School Count'] = 1
        merge2.at[0, "Board Name"] = "Bloorview SA"
    merge2["Percent of Schools"] = round((merge2["School"] / merge2["School Count"]) * 100,1)
    merge2["Percent of Schools"] = merge2["Percent of Schools"]

    figure = px.bar(merge2, x = 'Board Name', y = 'Percent of Schools',
            hover_data = ['School', 'School Count'],
            labels = {'School' : 'Schools Affected', 'School Count' : 'Schools in Board'},
            color = 'Percent of Schools', color_continuous_scale = 'Oryel',
            text = "Percent of Schools", opacity = 0.6
            #title = "% of Schools in Board with Active COVID-19 Cases"
            )
    figure.update(layout_coloraxis_showscale=False)
    figure.update_layout(xaxis_title = "", yaxis_title = "% of Schools",
                        font=dict(family = "Helvetica", size = 14, color = '#595959'))
    figure.update_traces(textposition = "outside", texttemplate = "%{y:.1f}%")
    if municipality == "Toronto":
            figure.update_yaxes(range = [0, 110])
    figure.update_yaxes(ticksuffix="%", gridcolor = 'lightgrey', showticklabels = False)
    figure.layout.plot_bgcolor = 'white'
    figure.layout.paper_bgcolor = 'white'
    return figure


@app.callback(
Output(component_id = "cases-per", component_property =  "figure"),
[Input(component_id = "munic-input", component_property = "value")])
def cases_per_graph(municipality):
    previous_seven = max(df_active["reported_date"]) - datetime.timedelta(days = 7)
    previous_day = max(df_active["reported_date"]) - datetime.timedelta(days = 1)
    prev_7 = (df_active["reported_date"] >= previous_seven) & (df_active["reported_date"] <= previous_day)
    df_previous_7 = df_active[prev_7]
    df_muni = df_previous_7[df_previous_7["municipality"] == municipality]
    merge1 = pd.merge(boards_students_df, boards_new_old_df, how = 'left', left_on = 'Board Name', right_on = 'school_board_new')
    g1 = df_muni.groupby(["school_board", "reported_date"])["confirmed_student_cases"].sum().reset_index()
    g2 = g1.groupby("school_board")["confirmed_student_cases"].mean().reset_index()
    m3 = pd.merge(g2, merge1, how = 'left', left_on = 'school_board', right_on = 'school_board')
    if municipality == "Toronto":
        m3.at[0, 'School Count'] = 1
        m3.at[0, "Board Name"] = "Bloorview SA"
    m3["Cases per 100k Students"] = round((m3["confirmed_student_cases"] * 100000) / m3["Enrolment"], 1)
    #m = max(m3["Cases per 100k Students"]) +

    figure = px.bar(m3, x = 'Board Name', y = 'Cases per 100k Students',
            hover_data = ['confirmed_student_cases'],
            labels = {'confirmed_staff_cases' : '7 Day Avg. Student Cases:'},
            color = 'Cases per 100k Students', color_continuous_scale = 'Oryel',
            text = "Cases per 100k Students", opacity = 0.6
            #title = "% of Schools in Board with Active COVID-19 Cases"
            )
    figure.update(layout_coloraxis_showscale=False)
    figure.update_layout(xaxis_title = "", yaxis_title = "COVID-19 Cases (per 100k)",
                        font=dict(family = "Helvetica", size = 14, color = '#595959'), uniformtext_minsize=12)
    #figure.update_yaxes(color = "lightgrey")
    figure.update_traces(textposition = "outside")
    figure.update_yaxes(gridcolor = 'lightgrey')
    figure.layout.plot_bgcolor = 'white'
    figure.layout.paper_bgcolor = 'white'
    return figure


@app.callback(
Output("breakdown", "children"),
Input("munic-input", "value"),
Input("school-input", "value"))

def text_return(muni, schl):
    muni = muni.upper()
    schl = schl.upper()
    return f"Cases in {muni} schools  and {schl}"



@app.callback(
Output("graph1", "children"),
Input("munic-input", "value"))

def muni_return(muni):
    muni = muni.upper()
    return f"% of Schools in {muni} with at least 1 Confirmed, Active COVID-19 Case"
