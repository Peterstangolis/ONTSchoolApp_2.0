### Page 1 of App ###
#### metrics ####
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib
from app import app

import datetime

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#--------------------------------------------------------------------------------#
#### IMPORT THE DATA SETS ####

## I. SUMMARY OF COVID-19 CASES IN ONTARIO SCHOOLS
url = "https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7fbdbb48-d074-45d9-93cb-f7de58950418/download/schoolcovidsummary.csv"
df_summary = pd.read_csv(url)

#### Change the reported_date column to a datetime object and drop collected_date
df_summary["reported_date"] = pd.to_datetime(df_summary["reported_date"])
df_summary.drop("collected_date", axis=1, inplace=True)


#-------------------------------------------------------------------------------#

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


#Drop Board Site from active_now:
board_site_index = df_active_now[df_active_now.School.str.contains('Board Site')].index
if len(board_site_index) > 0:
    df_active_now = df_active_now.drop(board_site_index)


### Filter the active data set for cases occurring on the last_reported datetime
df_active_now = df_active[df_active.reported_date == max(df_active.reported_date)]


### Group the active_now data set by municipality
df_municipality_now = df_active_now.groupby("municipality")['Active Cases'].sum().reset_index().sort_values(by=["Active Cases"], ascending=False).head(30)


## Change the column heading to municipality
df_municipality_now = df_municipality_now.rename({'municipality': 'Municipality'}, axis = 1)

## Set the index of summary dataset to the reported date to sum / average cases by week
datetime_index = pd.DatetimeIndex(df_summary.reported_date.values)
df_weekly = df_summary.set_index(datetime_index)
df_weekly.drop('reported_date', axis=1, inplace = True)

## Add week number to weekly data set
df_weekly['week_num'] = df_weekly.index.isocalendar().week

## Determining the last entries in the data set (student, staff, total)
# Latest Total School Case Number
value_t  = df_summary.loc[df_summary.index[-1], 'new_total_school_related_cases']

# Previous Day School Total
reference_t = df_summary.loc[df_summary.index[-2], 'new_total_school_related_cases']

#Latest Total School Case Number
value_student  = df_summary.loc[df_summary.index[-1], 'new_school_related_student_cases']

# Previous Day School Total
reference_student = df_summary.loc[df_summary.index[-2], 'new_school_related_student_cases']

# Latest Total School Case Number
value_staff  = df_summary.loc[df_summary.index[-1], 'new_school_related_staff_cases']

# Previous Day School Total
reference_staff = df_summary.loc[df_summary.index[-2], 'new_school_related_staff_cases']

# Number of boards with cases
schools_w_cases = df_summary.current_schools_w_cases[df_summary.reported_date == max(df_summary.reported_date)].values[0]
y_schools_w_cases = df_summary.loc[df_summary.index[-2], 'current_schools_w_cases']

# Number of schools closed
value = df_summary.loc[df_summary.index[-1], 'current_schools_closed']
value_yest = df_summary.loc[df_summary.index[-2], 'current_schools_closed']

## Schools with 2 or more active cases
df_schools_total_active_now = df_active_now.groupby(["municipality","School"])['Active Cases'].sum().reset_index().sort_values(by = "Active Cases", ascending = False)
schools_w_two_or_more = df_schools_total_active_now[df_schools_total_active_now["Active Cases"] >= 2].School.count()

## days remaining in school year
days_remain = 194 - df_summary.reported_date.count()


### GENERATE 5 DAY ROLLING AVERAGE TO CHART
for i in range(0, df_summary.shape[0]-4):
    df_summary.loc[df_summary.index[i + 4], "SMA_5"] = np.round(((df_summary.iloc[i, 4]+ df_summary.iloc[i+1, 4] + df_summary.iloc[i+2, 4] + df_summary.iloc[i+3, 4] + df_summary.iloc[i+4, 4])/5),1)


### Change the names of the columns in df_summary:
df_summary.rename(columns = {"new_total_school_related_cases" : "New Total Cases", "new_school_related_student_cases" : "New Student", "new_school_related_staff_cases":"New Staff"}, inplace=True)
df_summary.rename(columns = {"cumulative_school_related_cases" : "Cumulative Total", "cumulative_school_related_student_cases" : "Cumulative Student", "cumulative_school_related_staff_cases" : "Cumulative Staff"}, inplace=True)

### Number of schools in ONT that have had at least 1 covid case:
schl_total = max(df_summary['current_total_number_schools'])
s = df_active["School"].nunique()
print(s)
perc_schl = round(s / schl_total, 1) * 100
print(perc_schl)




## New Reported Cases Today Metric1
fig2 = go.Figure()
fig2.add_trace(go.Indicator(
        value = value_t,
        delta = {'reference': reference_t, 'increasing': {'color': "#BF2D17"}, 'decreasing' : {'color' : '#1D6DF2'}},
        mode = "number+delta",
        title = {"text" : " <br><span style = 'font-size: 0.9em; color:#595959'><b>REPORTED CASES </span>"},
        number = {"font" : {"size" : 42, 'color' : '#04ADBF'}}
    )
              ),
fig2.layout.paper_bgcolor = '#F2F2F2'
fig2.layout.plot_bgcolor = '#F2F2F2'

## New Student Cases Today Metric2
fig3 = go.Figure()
fig3.add_trace(
    go.Indicator(
        value = value_student,
        delta = {'reference': reference_student, 'increasing': {'color': "#BF2D17"}, 'decreasing' : {'color' : '#1D6DF2'}},
        mode = "number+delta",
        title = {"text" : " <br><span style = 'font-size: 1.0em; color:#595959'><b>STUDENTS</span>"},
        number = {"font" : {"size" : 42, 'color' : '#04ADBF'}},
        domain = {'row': 0, 'column' : 0},
     )
),
fig3.layout.paper_bgcolor = '#F2F2F2'
fig3.layout.plot_bgcolor = '#F2F2F2'

## New Staff Cases Today Metric3
fig4 = go.Figure()
fig4.add_trace(
    go.Indicator(
        mode = "number+delta",
        value = value_staff,
        delta = {"reference": reference_staff, 'increasing': {'color': "#BF2D17"}, 'decreasing' : {'color' : '#1D6DF2'}},
        title = {"text" : " <br><span style = 'font-size: 1.0em; color:#595959'><b>STAFF</span>"},
        number = {"font" : {"size" : 42, 'color': '#04ADBF'}}
    )
),
fig4.layout.paper_bgcolor = '#F2F2F2'

## Total Schools with Active Cases Metric4
fig5 = go.Figure()
fig5.add_trace(
    go.Indicator(
        mode = 'number+delta',
        value = schools_w_cases,
        delta = {'reference' : y_schools_w_cases, 'increasing': {'color': "#BF2D17"}, 'decreasing' : {'color' : '#1D6DF2'}},
        title = {"text" : " <br><span style = 'font-size: 0.9em; color:#FFFFFF'><b>SCHOOLS W/ <br>ACTIVE CASES</span>"},
        number = {"font" : {"size" : 42, 'color': '#F2F2F2'}}
    )
),
fig5.layout.paper_bgcolor = '#04ADBF'

## Schools Closed Metric5
fig6 = go.Figure()
fig6.add_trace(
    go.Indicator(
        mode = 'number+delta',
        value = value,
        delta = {'reference' : value_yest, 'increasing': {'color': "#BF2D17"}, 'decreasing' : {'color' : '#1D6DF2'}},
        title = {"text" : " <br><span style = 'font-size: 1.0emm; color:#FFFFFF'><b>SCHOOLS CLOSED</span>"},
        number = {"font" : {"size" : 42, 'color': '#F2F2F2'}})
),
fig6.layout.plot_bgcolor = '#04ADBF'
fig6.layout.paper_bgcolor = '#04ADBF'

## Schools with at least 2 cases  Metric6
fig7 = go.Figure()
fig7.add_trace(
    go.Indicator(
        mode = 'number',
        value = schools_w_two_or_more,
        title = {"text" : " <br><span style = 'font-size: 1.0em; color:#FFFFFF'><b>SCHOOLS WITH >= 2 <br>ACTIVE CASES</span>"},
        number = {"font" : {"size" : 42, 'color': '#F2F2F2'}}
)),
fig7.layout.plot_bgcolor = '#04ADBF'
fig7.layout.paper_bgcolor = '#04ADBF'


## School Days remaining vs Elapsed
# fig9 = go.Figure()
# fig9.add_trace(
#     go.Indicator(
#         mode = "gauge+number",
#         value = df_sum.reported_date.count(),
#         title = {'text': f"<span style='font-size:1.0em; color:#2E86C1'> Schools Days Completed: <br>{days_remain} To Go </span>"},
#         number = {"font" : {"size" : 40, 'color' : '#2E86C1'}},
#         gauge = {
#             'axis' : { 'range' : [0, 195], 'tickcolor': '#447FA6'},
#             'bar' : {'color' : 'white'},
#             'bordercolor' :'lightgrey',
#             'threshold' : {'line' : {'color': "red", 'width' : 4}, 'thickness': 0.90, 'value' : 194},
#             'steps' : [
#                 {'range' : [0, 100], 'color' : '#447FA6'},
#                 {'range' : [100, 195], 'color' : '#447FA6'}
#             ]}
#     ),
# )
# fig9.layout.plot_bgcolor = '#F2F4F4'
# fig9.layout.paper_bgcolor = '#F2F4F4'

## 5 Day Moving Average Line CHART
fig10 = px.line(df_summary, x = "reported_date", y = df_summary["SMA_5"])
fig10.update_xaxes(tickangle= 0,
                 autorange=True,
                 tickfont=dict(size= 11),
                 showgrid = False, gridcolor = 'lightgrey'
                 );

fig10.update_yaxes(showgrid = True, gridcolor = 'lightgrey',
                   title = "5 Day Rolling Average",
                  secondary_y = False);
fig10.update_traces(line=dict(width=3.1, color = '#D35400'))
fig10.layout.plot_bgcolor = '#F2F4F4'
fig10.layout.paper_bgcolor = '#F2F4F4'


fig11 = make_subplots(specs = [[{"secondary_y" : True}]])
fig11.add_trace(
    go.Scatter(x = df_summary["reported_date"], y = df_summary["SMA_5"]),
              secondary_y = True,
              )
# fig11.update_layout(
#     title_text = "<b>5 Day Moving Average of Daily COVID-19 School Case Totals</b>",
#     font = dict(
#         family = "Verdana",
#         size = 14,
#         color = 'black'))
fig11.update_xaxes(title_text = "Reported Date", showgrid=False, gridcolor = '#2E86C1',
                  showline = True, zerolinewidth = 0.8, linecolor = 'lightgrey')
fig11.update_yaxes(title_text = "Avg COVID-19 Cases", showgrid = True, gridcolor = 'lightgrey')

fig11.update_traces(line=dict(width=3.1, color = '#D35400'))
fig11.update_layout(font = dict(
                            family = "Helvetica",
                            color = "#595959",
                            size = 14
                    ))
fig11.layout.plot_bgcolor = '#F2F2F2'
fig11.layout.paper_bgcolor = '#F2F2F2'


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
                    'font-size' : '50px',
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

        # labels
        html.Div([
            html.Label("*Newly reported COVID-19 Cases based on the last reported date.  Change from previous day cases noted.",
                        style = {"color" : "#595959", "fontSize" :"14px", "padding" : "15px", 'border-bottom' : '1px sold #595959'},
                        className = "six columns"),
            html.Label(f"In the timeframe of the first reported date; {min(df_active.reported_date).date()} to the last reported date; {max(df_active.reported_date).date()}, of the {schl_total} ONT Schools, {s} or {perc_schl}% have had at least 1 confirmed case. ",
                        style = {"color" : "#595959", "fontSize" :"14px", "padding" : "15px", 'border-bottom' : '1px sold #595959'},
                        className = "five columns"),
        ], className = "row"),

        # Section of Metrics:
        html.Div(
        [
            html.Div(
                dcc.Graph(
                    id = 'metric1',
                    figure = fig2,
                    style = {
                        'width' : '17vh', 'height' : '14vh',
                        #'margin-bottom' : '20px',
                        #'margin-top' : '20px',
                        'margin-left' : '30px',
                        #'margin-right' : '20px',
                        'background' : '#04ADBF',
                        #'padding' : '10px',
                        #'border-bottom' : '4px solid #85C1E9',
                        #'border-top' : '4px solid #85C1E9'
                        #'border-radius' : '25px',
                        'border-radius': '5px',
                        'box-shadow': '5px 5px 5px grey',
                        #'background-color': '#85C1E9',
                        #'padding': '10px',
                        #'margin-bottom': '10px',
                        #'margin-left': '10px',
                        'border' : '1px solid #BFBFBF',
                        'padding' : '5px'
                    }),
                className = "two columns",
                style = {"backgroundColor" : "#D9D9D9"#"padding-left" : '10px'
                }),


            html.Div(
                dcc.Graph(
                    id = 'metric2',
                    figure = fig3,
                    style = {
                        'width' : '17vh', 'height' : '14vh',
                        #'margin-bottom' : '20px',
                        #'margin-top' : '20px',
                        'margin-left' : '10px',
                        #'margin-right' : '20px',
                        'background' : '#04ADBF',
                        'padding' : '5px',
                        #'border-bottom' : '4px solid #85C1E9',
                        #'border-top' : '4px solid #85C1E9'
                        #'border-radius' : '25px',
                        'border-radius': '5px',
                        'box-shadow': '5px 5px 5px grey',
                        'border' : '1px solid #BFBFBF',
                        #'background-color': '#85C1E9',
                        #'padding': '10px',
                        #'margin-bottom': '10px',
                        #'margin-left': '10px',

                    }),
                className = "two columns",
                style = {#"padding-left" : '10px'
                }),

            html.Div(
                dcc.Graph(
                    id = 'metric3',
                    figure = fig4,
                    style = {
                        'width' : '17vh', 'height' : '14vh',
                        #'margin-bottom' : '20px',
                        #'margin-top' : '20px',
                        #'margin-left' : '10px',
                        #'margin-right' : '20px',
                        #'background' : '#85C1E9',
                        #'border-bottom' : '4px solid #85C1E9',
                        #'border-top' : '4px solid #85C1E9'
                        #'border-radius' : '25px',
                        'border-radius': '5px',
                        'box-shadow': '5px 5px 5px grey',
                        'background-color': '#04ADBF',
                        'border' : '1px solid #BFBFBF',
                        'padding' : '5px',
                        #'padding': '10px',
                        #'margin-bottom': '10px',
                        #'margin-left': '10px'
                    }),
                className = "two columns",
                style = {"padding-left" : '10px'
                }),

            html.Div(
                dcc.Graph(
                    id = 'metric4',
                    figure = fig5,
                    style = {
                        'width' : '17vh', 'height' : '14vh',
                        #'margin-bottom' : '20px',
                        #'margin-top' : '10px',
                        #'margin-left' : '10px',
                        #'margin-right' : '20px',
                        #'background' : '#85C1E9',
                        #'padding' : '10px',
                        #'border-bottom' : '4px solid #85C1E9',
                        #'border-top' : '4px solid #85C1E9'
                        #'border-radius' : '25px',
                        'border-radius': '5px',
                        'box-shadow': '5px 5px 5px grey',
                        'background-color': '#F2F2F2',
                        'border' : '1px solid #BFBFBF',
                        'padding' : '5px',
                        #'margin-bottom': '10px',
                        #'margin-left': '10px'
                    }),
                className = "two columns",
                style = {#"padding-left" : '10px'
                }),

            html.Div(
                dcc.Graph(
                    id = 'metric5',
                    figure = fig6,
                    style = {
                        'width' : '17vh', 'height' : '14vh',
                        #'margin-bottom' : '20px',
                        #'margin-top' : '20px',
                        #'margin-left' : '10px',
                        #'margin-right' : '20px',
                        #'background' : '#85C1E9',
                        #'padding' : '10px',
                        #'border-bottom' : '4px solid #85C1E9',
                        #'border-top' : '4px solid #85C1E9'
                        #'border-radius' : '25px',
                        'border-radius': '5px',
                        'box-shadow': '5px 5px 5px grey',
                        'background-color': '#F2F2F2',
                        'border' : '1px solid #BFBFBF',
                        'padding' : '5px',
                        #'padding': '10px',
                        #'margin-bottom': '10px',
                        #'margin-left': '10px'
                    }),
                className = "two columns",
                style = {#"padding-left" : '10px'
                }),


            html.Div(
                dcc.Graph(
                    id = 'metric6',
                    figure = fig7,
                    style = {
                        'width' : '17vh', 'height' : '14vh',
                        #'margin-bottom' : '20px',
                        #'margin-top' : '20px',
                        #'margin-left' : '10px',
                        'margin-right' : '10px',
                        #'background' : '#85C1E9',
                        #'padding' : '10px',
                        #'border-bottom' : '4px solid #85C1E9',
                        #'border-top' : '4px solid #85C1E9'
                        #'border-radius' : '25px',
                        'border-radius': '5px',
                        'box-shadow': '5px 5px 5px grey',
                        'background-color': '#F2F2F2',
                        'border' : '1px solid #BFBFBF',
                        'padding' : '5px',
                        #'padding': '10px',
                        #'margin-bottom': '10px',
                        #'margin-left': '10px'
                    }),
                className = "two columns",
                style = {#"padding-left" : '10px'
                }),

            # end of metric div
            ], className = "row",
            style = {"backgroundColor" : "#D9D9D9", "padding" : "10px"
            }),



        # start of selection divide
        html.Div(
            [
                html.Div(
                [

                html.Label("SELECT TO VIEW CUMULATIVE COVID-19 CASE TOTALS",
                    style = {"fontSize" : "16px", "color" : "#04ADBF", 'font-weight' : 'bold', 'padding-top' : '20px',
                            'padding-bottom' : '10px', "margin-left" : "20px"}),
                dcc.Dropdown(
                        id = "line_chart",
                         options = [
                                {'label' : "Cumulative Cases  vs  New Daily Cases", "value" : "New Total Cases_Cumulative Total"},
                                {'label' : "Cumulative Student Cases  vs  New Daily Student Cases", "value" : "New Student_Cumulative Student"},
                                {'label' : "Cumulative Staff Cases  vs  New Daily Staff Cases", "value" : "New Staff_Cumulative Staff"}
                                ],
                                value="New Total Cases_Cumulative Total",
                                style={
                                    #'display': 'inline-block',
                                    'margin-right' : '10px',
                                    'margin-left' : '10px',
                                    'textAlign' : 'left',
                                    'width' : '80%'}
                            ),

                 html.Label("Cumulative COVID-19 Cases in Ontario Schools vs Daily Reported Cases (Total, Staff & Student)",
                    style = {"fontSize" : "16px", "color" : "#595959", "margin-left" : "20px", "margin-top" : "20px",
                            "font-weight" : "bold", 'border-top' : '1px solid lightgrey'}),


                dcc.Graph(
                            id="line-graph",
                            figure = {
                                "layout" : {"height" : 390}
                            },
                            style = {"margin-bottom" : "0px"})

                 ], className = "six columns", style = {"backgroundColor" : "#F2F2F2", 'border-radius': '5px',
                                                        'box-shadow': '5px 5px 5px grey',
                                                        'background-color': '#F2F2F2',
                                                        'border' : '1px solid #BFBFBF',
                                                        'padding' : '5px', "height" : 'auto'}),


             html.Div([
                html.Label("5 - DAY MOVING AVERAGE OF DAILY CASES AMONG STAFF, STUDENTS & UNSPECIFIED", style = {"fontSize" : "18px", "color": "#595959", 'font-weight' : 'bold',
                                                    "padding" : "20px", "textAlign" : "left",
                                                    'border-bottom' : '1px solid lightgrey'}),

                dcc.Graph(figure = fig11),
                ],className = "six columns", style = {"backgroundColor" : "#F2F2F2", 'border-radius': '5px',
                                                    'box-shadow': '5px 5px 5px grey',
                                                    'background-color': '#F2F2F2',
                                                    'border' : '1px solid #BFBFBF',
                                                    'padding' : '5px', 'height' : 'auto'})

             ], className = "row",
                style = {"backgroundColor" : "#D9D9D9", 'padding-right' : '30px', 'padding-left' : '30px', 'padding-top' : '20px', 'padding-bottom' : '20px'}),

    html.Div([
        html.Footer(""),
        html.P("*The data for the metrics and graphs were aquired from the Government of Ontario's Website below:",
                style = {"font-size" : "14", 'fontFamily' : 'Helvetica', 'color' : '#D9D9D9'}),
        html.A("Source", href="https://data.ontario.ca/dataset/summary-of-cases-in-schools",
                    target = "_blank",
                    style = {
                        'textAlign' : 'center',
                        'color' :  '#D9D9D9',
                        #'padding-left' : '30px',
                        'font-size' : '18px',
                        'font-variant-caps': 'small-caps'
                    })
                    ], style = {"padding-left" : "30px", 'backgroundColor' : "#04ADBF"}
                    )





# End of Initial Div
], className = 'ten columns offset-by-one', style = {"backgroundColor" : "#D9D9D9"}

),style = {"backgroundColor" : "#D9D9D9", "fontFamily" : "Helvetica"}

)


# updates the line chart based on student, staff or total selected
@app.callback(
     Output(component_id = "line-graph", component_property =  'figure'),
     [Input(component_id = "line_chart", component_property = "value")])
def update_line(selection):
    new = selection.split("_")[0]
    cu = selection.split("_")[1]
    figure= make_subplots(specs = [[{"secondary_y": True}]])  # One cell plot
    trace1 = go.Bar(x = df_summary["reported_date"],
                    y = df_summary[new],
                    name = "Daily Case Totals",
                    marker = dict(color = '#04ADBF',
                                 line = dict(width = 1), opacity = 0.4)
                    )

    trace2 = go.Scatter(x = df_summary["reported_date"],
                        y = df_summary[cu],
                        marker = dict(line = dict(width = 1),
                                     size = 8),
                        line = dict(color= '#D35400', width = 2.2),
                        name = "Accumulated Cases")

    figure.update_traces(opacity = 0.6)

    figure.add_trace(trace1, secondary_y = False)

    figure.add_trace(trace2, secondary_y = True)

    figure.update_layout(legend = dict(x=0.1, y=0.9), hovermode='x')

    figure.update_xaxes(tickangle= 0, autorange=True,
                        rangebreaks = [
                        dict(bounds = ["sat", "mon"])], title = "", tickfont=dict(size= 14, family = "Helvetica"), title_font =dict(size = 14, family = "Helvetica"
                        ))

    figure.update_yaxes(showgrid = False, title = "Daily Reported Cases", secondary_y = False, dtick = 100,  title_font=dict(size = 14, family = "Helvetica"))

    figure.update_yaxes(showgrid = True, gridcolor = 'lightgrey', title = "Cumulative Cases", secondary_y = True, title_font=dict(size = 14, family = "Helvetica"))

    figure.update_layout(#title = f"{new} vs {cu}",
                        legend = dict(bgcolor = 'lightgrey'),
                        font = dict(
                                family = 'Helvetica',
                                size = 14,
                                color = '#595959'))
    figure.layout.paper_bgcolor = '#F2F2F2'
    figure.layout.plot_bgcolor = '#F2F2F2'

    return figure
