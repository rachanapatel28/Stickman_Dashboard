import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import (
    Dash,
    dcc,
    html,
    Input,
    Output,
)  # pip install dash (version 2.0.0 or higher)


external_stylesheets = [
    "./assets/style.css",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
]
external_scripts = [
    "https://code.jquery.com/jquery-3.2.1.min.js",
    "https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
]
app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
)

# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("../data/dummy_data.csv")
df["year"] = df["start_date"].apply(lambda x: int(x.split("-")[0]))
df.reset_index(inplace=True, drop=True)
#print(df.head())


################################################################################
# Static Graph Functions
################################################################################
def update_year_vs_country_bubble_map():
    dff=df.copy()
    dff=dff[['year','location']].groupby(['year','location']).size().reset_index(name='counts')
    #print(dff)
    fig = px.scatter_geo(dff, locations="location", color='location', 
                         hover_name="location", size="counts",
                         animation_frame="year",
                         template='plotly_dark',
                         labels={'year':'Year','location':'Location','counts':'No. of Projects'},
                         #projection="natural earth")
                         title='Year vs Project Count - Country Wise Bubble Map',
                         projection="robinson")
    return fig


def update_year_vs_country_bar_graph():
    dff=df.copy()
    dff=dff['location'].value_counts().reset_index(name='counts')
    #print(dff)
    fig = px.bar(dff, 
            x='index',
            y='counts',
            template='plotly_dark',
            labels={'counts':'No. of Projects','index':'Location'},
            title='Year vs Project Count - Country Wise Bar Chart',
            )
    return fig

################################################################################
# LAYOUT
################################################################################

app.layout = html.Div(
    [
        html.H1("Stickman Services Dashboard", style={"text-align": "center", "color": "#FFFFFF"}),

        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id="total_projects_number",
                            children=len(df),
                            className="info_text",
                        ),
                        html.P("Total Projects"),
                    ],
                    id="total_projects",
                    className="pretty_container col-sm-6 row mt-1",
                ),
            ], className="d-flex justify-content-center row m-3",
            ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id="app_dev_projects_number",
                            children=len(df[df['service']=='App Development']),
                            className="info_text",
                        ),
                        html.P("App Development"),
                    ],
                    id="total_ad_projects",
                    className="pretty_container col-sm-1",
                ),
                html.Div(
                    [
                        html.H6(
                            id="dsac_projects_number",
                            children=len(df[df['service']=='Digital Strategy and Consultation']),
                            className="info_text",
                        ),
                        html.P("Digital Strategy and Consultation"),
                    ],
                    id="total_dsac_projects",
                    className="pretty_container col-sm-1",
                ),
                html.Div(
                    [
                        html.H6(
                            id="dts_projects_number",
                            children=len(df[df['service']=='Digital Transformation Service']),
                            className="info_text",
                        ),
                        html.P("Digital Transformation Service"),
                    ],
                    id="total_dts_projects",
                    className="pretty_container col-sm-1",
                ),
                html.Div(
                    [
                        html.H6(
                            id="gdwdad_projects_number",
                            children=len(df[df['service']=='Growth Driven Web Design and Development']),
                            className="info_text",
                        ),
                        html.P("Growth Driven Web Design and Development"),
                    ],
                    id="total_gdwdad_projects",
                    className="pretty_container col-sm-1",
                ),
            ],
            className="row m-1 d-flex justify-content-evenly",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="slct_year_for_service_yearly_pie_chart",
                            options=[
                                {"label": str(year), "value": year}
                                for year in sorted(df["year"].unique())
                            ],
                            multi=False,
                            value=df["year"].min(),
                            style={"width": "100%", "color": "black"},
                        ),
                        dcc.Graph(
                            id="service_yearly_pie_chart",
                            style={"width": "100%"},
                        ),
                    ],
                    className="col-md-5 mt-3",
                ),

                html.Div(
                    [
                        dcc.Dropdown(
                            id="slct_team_for_team_proj_line_graph",
                            options=[
                                {"label": str(team), "value": team}
                                for team in sorted(df["team"].unique())
                            ],
                            multi=False,
                            value=df["team"].min(),
                            style={"width": "100%", "color": "black"},
                        ),
                        dcc.Graph(
                            id="team_proj_line_graph", style={"width": "100%"}
                        ),
                    ],
                    className="col-md-7 mt-3",
                ),

            html.Div(
                    [
                        dcc.Dropdown(
                            id="slct_service_for_year_vs_price_service_line_chart",
                            options=[
                                {"label": str(service), "value": service}
                                for service in sorted(df["service"].unique())
                            ],
                            multi=False,
                            value=df["service"].min(),
                            style={"width": "100%", "color": "black"},
                        ),
                        dcc.Graph(
                            id="year_vs_price_service_line_chart",
                            style={"width": "100%"},
                        ),
                    ],
                    className="row mt-3",
                ),


            html.Div(
                    [
                        dcc.Graph(
                            id="year_vs_country_bubble_map",
                            style={"width": "100%"},
                            figure=update_year_vs_country_bubble_map()
                        ),
                    ],
                    className="col-md-7 mt-3",
                ),

            html.Div(
                    [
                        dcc.Graph(
                            id="year_vs_country_bar_graph",
                            style={"width": "100%"},
                            figure=update_year_vs_country_bar_graph()
                        ),
                    ],
                    className="col-md-5 mt-3",
                ),

            html.Div(
                    [
                        dcc.Dropdown(
                            id="slct_team_for_year_vs_price_team_line_chart",
                            options=[
                                {"label": str(team), "value": team}
                                for team in sorted(df["team"].unique())
                            ],
                            multi=False,
                            value=df["team"].min(),
                            style={"width": "100%", "color": "black"},
                        ),
                        dcc.Graph(
                            id="year_vs_price_team_line_chart",
                            style={"width": "100%"},
                        ),
                    ],
                    className="row mt-3",
                ),
            ],
            className="row m-3"
        ),
    ],
)

################################################################################
# INTERACTION CALLBACKS
################################################################################


@app.callback(
    Output(component_id="team_proj_line_graph", component_property="figure"),
    [
        Input(
            component_id="slct_team_for_team_proj_line_graph",
            component_property="value",
        )
    ],
)
def update_team_timeline_graph(option_slctd):

    dff = df.copy()
    dff = (
        dff[["year", "team", "proj_no"]][dff["team"] == option_slctd]
        .groupby("year")["proj_no"]
        .count()
        .reset_index()
    )
    # Plotly Express

    fig = px.line(
        data_frame=dff,
        x=dff["year"],
        y=dff["proj_no"],
        line_group=None,
        color=None,
        line_dash=None,
        symbol=None,
        hover_name=None,
        hover_data=None,
        custom_data=None,
        text=None,
        facet_row=None,
        facet_col=None,
        facet_col_wrap=0,
        facet_row_spacing=None,
        facet_col_spacing=None,
        error_x=None,
        error_x_minus=None,
        error_y=None,
        error_y_minus=None,
        animation_frame=None,
        animation_group=None,
        category_orders=None,
        labels={"proj_no": "No. of Projects", "year": "Year"},
        orientation=None,
        color_discrete_sequence=None,
        color_discrete_map=None,
        line_dash_sequence=None,
        line_dash_map=None,
        symbol_sequence=None,
        symbol_map=None,
        markers=False,
        log_x=False,
        log_y=False,
        range_x=None,
        range_y=None,
        line_shape=None,
        render_mode="auto",
        title=f"Year vs Projects for {option_slctd.title()}",
        template="plotly_dark",
        width=None,
        height=None,
    )

    return fig


@app.callback(
    Output(
        component_id="service_yearly_pie_chart", component_property="figure"
    ),
    [
        Input(
            component_id="slct_year_for_service_yearly_pie_chart",
            component_property="value",
        )
    ],
)
def update_services_pie_chart(option_slctd):
    dff = df.copy()
    dff = (
        dff[["year", "service", "proj_no"]][dff["year"] == option_slctd]
        .groupby("service")["proj_no"]
        .count()
        .reset_index()
    )
    fig = px.pie(
        data_frame=dff,
        names="service",
        values="proj_no",
        color=None,
        color_discrete_sequence=None,
        color_discrete_map=None,
        hover_name=None,
        hover_data=None,
        custom_data=None,
        labels={"service": "Services", "proj_no": "No. of Projects"},
        title="Yearly Services Count",
        template="plotly_dark",
        width=None,
        height=None,
        opacity=None,
        hole=0.4,
    )
    return fig

@app.callback(
    Output(
        component_id="year_vs_price_service_line_chart", component_property="figure"
    ),
    [
        Input(
            component_id="slct_service_for_year_vs_price_service_line_chart",
            component_property="value",
        )
    ],
)
def update_year_vs_price_service_line_chart(option_slctd):
    dff = df.copy()
    dff=dff[["year", "service", "price"]][dff["service"] == option_slctd].groupby("year")["price"].agg([np.min,np.max,np.mean]).reset_index()
    #print(dff)

    fig = go.Figure()
    fig.update_layout(template='plotly_dark', 
            title=f"Year vs Average Price for {option_slctd.title()}",
            xaxis_title="Year",
            yaxis_title="Average Price"
            )

    fig.add_trace(go.Scatter(
        x=dff["year"], y=dff["mean"],
        mode='lines',        
        showlegend=False,
        name=option_slctd.title()
    ))
    fig.add_trace(go.Scatter(
        x=dff["year"],
        y=dff["amax"],
        mode='none',
        fill='tonexty', 
        fillcolor='rgba(99, 110, 250,0.)',
        showlegend=False,
        name=option_slctd.title()
    ))
    fig.add_trace(go.Scatter(
        x=dff["year"],
        y=dff["amin"],
        mode='none',
        fill='tonexty', 
        fillcolor='rgba(99, 110, 250,0.2)',
        showlegend=False,
        name=option_slctd.title()
    ))


    return fig

@app.callback(
    Output(
        component_id="year_vs_price_team_line_chart", component_property="figure"
    ),
    [
        Input(
            component_id="slct_team_for_year_vs_price_team_line_chart",
            component_property="value",
        )
    ],
)
def update_year_vs_price_team_line_chart(option_slctd):
    dff = df.copy()
    dff=dff[["year", "team", "price"]][dff["team"] == option_slctd].groupby("year")["price"].agg([np.min,np.max,np.mean]).reset_index()
    #print(dff)

    fig = go.Figure()
    fig.update_layout(template='plotly_dark', 
            title=f"Year vs Average Price for {option_slctd.title()}",
            xaxis_title="Year",
            yaxis_title="Average Price"
            )

    fig.add_trace(go.Scatter(
        x=dff["year"], y=dff["mean"],
        mode='lines',        
        showlegend=False,
        name=option_slctd.title()
    ))
    fig.add_trace(go.Scatter(
        x=dff["year"],
        y=dff["amax"],
        mode='none',
        fill='tonexty', 
        fillcolor='rgba(99, 110, 250,0.)',
        showlegend=False,
        name=option_slctd.title()
    ))
    fig.add_trace(go.Scatter(
        x=dff["year"],
        y=dff["amin"],
        mode='none',
        fill='tonexty', 
        fillcolor='rgba(99, 110, 250,0.2)',
        showlegend=False,
        name=option_slctd.title()
    ))


    return fig


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)
