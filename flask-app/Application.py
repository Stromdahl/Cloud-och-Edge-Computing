from flask import Flask
from flask import render_template
from datetime import time, datetime

from DynamoDB.dynamodb import get_all_values, Device

app = Flask(__name__)


@app.route("/simple_chart")
def chart():
	legend = 'Monthly Data'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
	values = [10, 9, 8, 7, 6, 4, 7, 8]
	return render_template('chart.html', values=values, labels=labels, legend=legend)


@app.route("/line_chart")
def line_chart():
	legend = 'Temperatures'
	raw_data = get_all_values()
	data = [Device.create_from_dict(d) for d in raw_data]
	data.sort(key=lambda v: v.time)
	temperatures = [d.temperature for d in data]
	times = [datetime.fromtimestamp(d.time) for d in data]
	return render_template('line_chart.html', values=temperatures, labels=times, legend=legend)



if __name__ == "__main__":
	app.debug()
	app.run(debug=True)

