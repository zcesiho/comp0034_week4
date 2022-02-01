# COMP0034 Lab 4 Activities

This builds on the paralympic app created in lab session 3. The directory structure of the app is:

```text
/paralympic_app/
    paralympic_app.py  # Creates the dash app
    create_charts.py  # Functions to create the charts for the dash app
    /assets/  # Directory for css, images etc
    /data/ # Directory containing the data files, including geojson
```

## Overview of Dash callbacks

A **callback function** is a Python function that is automatically called by Dash whenever an input component's property
changes.

The basic structure of the callback is:

```python
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
```

By writing this decorator, we're telling Dash to call this function whenever the value of the "input"
component (e.g. the dropdown) changes in order to update the children of the "output" component on the page (e.g. the
HTML div for the stats card).

You can use any name for the function that is wrapped by the `@app.callback` decorator. The convention is that the name
describes the callback output(s).

You can use any name for the function arguments, but you must use the same names inside the callback function as you do
in its definition, just like in a regular Python function. The arguments are positional: first the Input items and then
any State items are given in the same order as in the decorator.

You must use the same `id` you gave a Dash component in the `app.layout` when referring to it as either an input or
output of the `@app.callback` decorator.

The `@app.callback` decorator needs to be directly above the callback function declaration. If there is a blank line
between the decorator and the function definition, the callback registration will not be successful.

To create a callback:

- **Define the Input**. Identify the component id (e.g. id of an html element) and component property that the user will
  interact with.
- **Define the Outputs**. Identify the component id and property that will be updated after we make a change.
- **Write a Python function using the @callback decorator**. The function will be run when the Input has been selected.

For more information refer to the Dash callbacks online tuotrial and documentation:

- [Basic callbacks](https://dash.plotly.com/basic-callbacks)
- [Data sharing between callbacks](https://dash.plotly.com/sharing-data-between-callbacks)
- [Advanced callbacks](https://dash.plotly.com/advanced-callbacks)

## Task 1: Allow the first chart to be changed to show athletes, nations, events or sports

### Create a two column layout

Use Bootstrap to create a 1 row, 2 column layout. The first column will contain a selector, the second the chart.

The following shows a row with two columns based on a 12 column grid layout.

```python
dbc.Row([
    # This is for selector
    dbc.Col(width=3, children=[
        html.P('col 1')
    ]),
    # This is for the figure.
    dbc.Col(width=9, children=[
        html.P('col 2')
    ]),
]),
```

Amend the code for the first chart so that the chart replaces `html.P('col 2')`

### Create a selection box

Add a select element to the select the chart type. The Dash component to use
is [dcc.Dropdown](https://dash.plotly.com/dash-core-components/dropdown).

```python
dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montreal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='NYC'
),
```

In the first column, replace `html.P('col 1')` with a dropdown with the values: 'EVENTS', 'SPORTS', 'COUNTRIES', '
PARTICIPANTS'. These are the column headings in the dataframe.

Decide on a default, e.g. in the example code above this is `value='NYC`.

### Create a callback to update the chart when the selection changes

The syntax of a callback is:

```python
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
```

The Output for the callback is the line chart (`component_id='line-chart-time'`) and (`component_property='figure'`)

The Input for the callback is the dropdown (`component_id='type-dropdown'`) and the selected
value (`component_property=value`).

The callback function should take the value of the variable selected and pass it to
the `create_charts.line_chart_over_time(chart_type)` function to generate the line chart. It should return the new
figure (line chart).

## Allow users to select whether to display winter or summer for the 'ratio of male and female athletes' chart

Add check boxes so that the person can select whether to see summer, winter or both; then update the charts accordingly.

### Move the charts to a 2 column layout

Use the same approach as previously to create a 2 column layout for the chart and the check boxes.

```python
dbc.Row([
    dbc.Col(width=3, children=[
        html.P('col 1')
    ]),
    dbc.Col(width=9, children=[
        html.P('col 2')
    ]),
]),
```

Move the two charts to the second column replacing `html.P('col 2')`

### Create the checkboxes for Winter and Summer

To do this you can use the [dcc.Checklist components](https://dash.plotly.com/dash-core-components/checklist).

```python
dcc.Checklist(
    id='mf-ratio-checklist',
    options=[
        {'label': 'Winter', 'value': 'Winter'},
        {'label': 'Summer', 'value': 'Summer'}
    ],
    value=['Winter', 'Summer'],
    labelStyle={"display": "inline-block"},
),
```

### Add the call back

The callback should respond to changes in the checkbox and display or hide the relevant charts.

This time we have two outputs; the two charts. You will need to find the 'ids' of these.

To provide two outputs they need to be provided as a list `[]` e.g.

```python
@app.callback(
    [Output("my-id-1", "style"),
     Output("my-id-2", "style")],
    Input("my-checklist", "value"),
)
```

Rather than changing the 'figure' property, this time you will change the 'style' property to hide/show the figure.

To show or hide an element you can use `style={'display': 'block'}` and `style={'display': 'none'}` on an HTML div.
The 'Div' has been added to the app code for you.

The callback takes the checkbox list of values. The list can contain either or both of Winter and Summer. If neither are
selected the list would be empty.

The callback can check the content of the list of values, and based on the contents, set the style parameters for the
two Outputs.

The callback needs to return two values as a list `[display_val_1, display_val_2]`. The first will affect the first
Output in your list, and the second, the second Output in the list.

The values will be either `style={'display': 'block'}` or `style={'display': 'none'}`.

## Display information about a paralympic event when the hovering over a location on the OSM map

The chart is already in a two column layout. The first column will be used to display the 'HIGHLIGHTS' data from the
paralympics.csv.

This time we will create an [interactive graph](https://dash.plotly.com/interactive-graphing), so the input is a
property of the figure (dcc.Graph) rather than a selector. As given in the documentation:

> "The dcc.Graph component has four attributes that can change through user-interaction: `hoverData`, `clickData`,
`selectedData`, `relayoutData`. These properties update when you hover over points, click on points, or select regions of points in a graph."

This task is based on the HoverData example in the Dash tutorial.

```python
@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)
```

For this task you will use the `hoverData` from the `dcc.Graph(id='scatter-mapbox-osm', figure=fig_scatter_mapbox_OSM),`
to find the Location and Year of an event. The Location and Year can be passed to a function
called `get_event_highlights(location, year)` in `create_charts.py` that will get the highlight data. The data then
needs to be displayed in the `html.P('Click...', id='highlight-text')` element.

The hover data from the graph is returned as json so you will need to `import json`.

You will need to work out how to access elements of the json array for this callback, expect this exercise to be more
challenging!

## Further practice
There are a couple of tables and a choropleth map in the example. See if you can add interactivity to one of these.

A selection of online tutorials for further practice:

- [Creating powerful Pythonic dashboards with Dash - Part 1: Development](https://www.linkedin.com/pulse/creating-powerful-pythonic-dashboards-dash-part-1-russo-%E9%A9%AC%E9%87%8C%E5%A5%A5-)
- [Develop Data Visualization Interfaces in Python With Dash](https://realpython.com/python-dash/)
- [6 Steps to Interactive Python Dashboards with Plotly Dash](https://www.justintodata.com/python-interactive-dashboard-with-plotly-dash-tutorial/)
- [The Dash Callback - Input, Output, State, and more, Charming Data channel, YouTube](https://www.youtube.com/watch?v=mTsZL-VmRVE)
  This series of video tutorials is well presented and easy to understand.