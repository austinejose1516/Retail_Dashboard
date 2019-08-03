# Importing Necessary Libraries

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, Tabs, Panel, RangeSlider, TableColumn, DataTable, TextInput, Button, Paragraph
from bokeh.layouts import layout
from bokeh.themes import built_in_themes
from bokeh.transform import cumsum
from bokeh.palettes import Greys256, Plasma256, Category20c
from math import pi

# Sales By Department Visualizations

df = pd.read_csv('/Users/austinejose/Desktop/My Files/Work/Newcastle Service Station/2018/Feb_Totals.csv')
df.columns = ['Product_Name', 'Quantity', 'Avg_SP', 'Curr_SP', 'Retail_Value', 'Ratio', 'Department']
df = df.round(0)

source  = ColumnDataSource(data = df)

TOOLTIPS = [
    ("Name", "@Product_Name"),
    ("Quantity", "@{Quantity}"),
    ("Retail Value", "@{Retail_Value}"),
]

p = figure(x_range = [], plot_height = 700, plot_width = 1300, title = "Sales By Departments",
           toolbar_location = "below", tooltips=TOOLTIPS)

p.vbar(x = "Product_Name", top = "Quantity", width = 0.6, source = source, color = 'skyblue')
p.xgrid.grid_line_color = "white"
p.x_range.range_padding = 0.05
p.xaxis.major_label_orientation = pi/4
p.xaxis.axis_label = "Product Name"
p.yaxis.axis_label = "Retail Value"
p.outline_line_color = "black"

def filter_source(attr, old, new):
    new_source = df[df['Department']==select.value]
    source.data = ColumnDataSource.from_df(new_source)
    p.x_range.factors = [str(x) for x in new_source['Product_Name']]

menus = df['Department'].unique().tolist()
select = Select(title = 'Choose Department', options = menus, value = 'Bill Pay')
select.on_change('value', filter_source)

# Sales Analysis Visualization

def filter_value(attr, old, new):
    current = df[(df['Quantity'] >= slider.value[0]) & (df['Quantity'] <= slider.value[1])]
    source.data = {
        'Quantity'       : current.Quantity,
        'Retail_Value'   : current.Retail_Value,
        'Product_Name'   : current.Product_Name
    }

slider = RangeSlider(title="Quantity", start=0, end=6150, value=(0, 60), step=50, format="0,0")
slider.on_change('value', filter_value)

q = figure(title = 'All Sales', tooltips=TOOLTIPS)

q.triangle('Quantity', 'Retail_Value', fill_alpha = 0.2, size = 5, source = source)
q.xaxis.axis_label = 'Quantity'
q.yaxis.axis_label = 'Retail Value'

columns = [
    TableColumn(field="Product_Name", title="Product Name"),
    TableColumn(field="Quantity", title="Quantity"),
    TableColumn(field="Retail_Value", title="Retail Value")
]

data_table = DataTable(source=source, columns=columns, width=700, height = 600)

# Sales Pie Chart Visualization

TOOLTIPS1 = [
    ("Name", "@Department"),
    ("Quantity", "@{Quantity}"),
    ("Retail Value", "@{Retail_Value}"),
]

newdf = df.groupby('Department', as_index=False).sum()

df2 = newdf.sort_values(by = 'Quantity', ascending=False)
df2 = df2.head(20)

df3 = newdf.sort_values(by = 'Retail_Value', ascending=False)
df3 = df2.head(20)

df2['angle1'] = df2['Quantity']/df2['Quantity'].sum() * 2*pi
df2['color'] = Category20c[len(df3['Department'])]
df3['angle2'] = df3['Retail_Value']/df3['Retail_Value'].sum() * 2*pi
df3['color'] = Category20c[len(df3['Department'])]

r1 = figure(plot_height=500, title="Sales based on Quantity", toolbar_location = "below",
           tooltips=TOOLTIPS1)
r2 = figure(plot_height=500, title="Sales based on Retail Value", toolbar_location = "below",
           tooltips=TOOLTIPS1)

r1.wedge(x=0, y=1, radius=0.6,
        start_angle=cumsum('angle1', include_zero=True), end_angle=cumsum('angle1'),
        line_color="white", source=df2, fill_color='color')
r2.wedge(x=0, y=1, radius=0.6,
        start_angle=cumsum('angle2', include_zero=True), end_angle=cumsum('angle2'),
        line_color="white", source=df3, fill_color='color')

# Wastage Data Visualizations

wastage = pd.read_csv('/Users/austinejose/Desktop/My Files/Work/Newcastle Service Station/wastage/u_waste.csv')

source_waste = ColumnDataSource(data = wastage)

TOOLTIPS_1 = [
    ("Name", "@Product"),
    ("Quantity", "@{Adj_Qty}"),
    ("Retail Value", "@{Adj_Value}"),
]

s = figure(x_range = [], plot_height = 700, plot_width = 1300, title = "Sales By Departments",
           toolbar_location = "below", tooltips=TOOLTIPS_1)

s.vbar(x = "Product", top = "Adj_Qty", width = 0.6, source = source_waste, color = 'skyblue')
s.xgrid.grid_line_color = "white"
s.x_range.range_padding = 0.05
s.xaxis.major_label_orientation = pi/4
s.xaxis.axis_label = "Product Name"
s.yaxis.axis_label = "Quantity"
s.outline_line_color = "black"

def filter_source_1(attr, old, new):
    new_source_1 = wastage[wastage['Dept']==select_1.value]
    source_waste.data = ColumnDataSource.from_df(new_source_1)
    s.x_range.factors = [str(x) for x in new_source_1['Product']]

menus_1 = wastage['Dept'].unique().tolist()
select_1 = Select(title = 'Choose Department', options = menus_1, value = 'Dairy')
select_1.on_change('value', filter_source_1)

# Fuel Data Visualizations

diesel = pd.read_csv('/Users/austinejose/Desktop/My Files/Work/Newcastle Service Station/fuel/unleaded.csv')
unleaded = pd.read_csv('/Users/austinejose/Desktop/My Files/Work/Newcastle Service Station/fuel/diesel.csv')

TOOLTIPS = [
    ("Date", "@Date"),
    ("Retail Value", "@{Value}"),
]

f = figure(x_axis_type="datetime", plot_width=1000, plot_height=350, tooltips = TOOLTIPS)

f.line('Unnamed: 0', 'Profit', source=diesel, line_width = 2, color = 'green')
f.line('Unnamed: 0', 'Profit', source=unleaded, line_width = 2, color = 'skyblue')
f.circle('Unnamed: 0', 'Profit', fill_color="green", size=8, source = diesel)
f.circle('Unnamed: 0', 'Profit', fill_color="skyblue", size=8, source = unleaded)
f.xgrid.grid_line_color = "white"
f.x_range.range_padding = 0.05
f.xaxis.axis_label = "Date"
f.yaxis.axis_label = "Retail Value"

# Final Layout

tab1 = Panel(child = column(select, p), title = 'Sales By Departments')
tab2 = Panel(child = column(slider, row(q, data_table)), title = 'Sales Analysis')
tab3 = Panel(child = row(r1, r2), title = 'Overall Sales')
tab4 = Panel(child = column(select_1, s), title = 'Wastage Chart')
tab5 = Panel(child = f, title = "Fuel Sales")
tabsdisplay = Tabs(tabs = [tab1, tab2, tab3, tab4, tab5])

curdoc().add_root(tabsdisplay)
curdoc().title = "SPAR Dashboard"
