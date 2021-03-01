from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, output_file, show
from bokeh.resources import CDN

from dynamodb import get_all_values, Device


def main():
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

	output_file("lines.html")
	show(p)
	script1, div1 = components(p)
	cdn_js = CDN.js_files
	cdn_css = CDN.css_files
	print()


if __name__ == '__main__':
	main()
