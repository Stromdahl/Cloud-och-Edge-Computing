from bokeh.embed import components
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask, render_template

from dynamodb import get_all_values, Device

app = Flask(__name__)


@app.route("/")
def plot():
	raw_data = get_all_values()
	data = [Device.create_from_dict(value) for value in raw_data]
	temperature_values = [int(value.temperature) for value in data]
	time_values = [value.time for value in data]

	# prepare some data
	x = time_values
	y = temperature_values

	# create a new plot with a title and axis labels
	p = figure(title="Values", x_axis_type="datetime", x_axis_label='Time', y_axis_label='Temperature')

	p.line(x, y, legend_label="Temp.", line_width=2)

	#output_file("lines.html")
	#show(p)
	script1, div1 = components(p)
	cdn_js = CDN.js_files[0]
	cdn_css = CDN.css_files[0]

	return render_template("home.html", script1=script1, div1=div1, cdn_js=cdn_js, cdn_css=cdn_css)
