from datetime import datetime

import matplotlib.pyplot as plt
from flask import Flask, render_template, jsonify

from dynamodb import get_all_values, Device

app = Flask(__name__)


def get_current_time():
    now = datetime.now()
    return "Current time: " + now.strftime("%H:%M:%S")


def get_current_sensor_values():
    values = [Device.create_from_dict(value) for value in get_all_values()]
    values.sort(key=lambda v: v.time)
    temperature = values[-1].data["temperature"]
    soil_moisture = values[-1].data["moisture"]
    return temperature, soil_moisture


def plot(values, ylabel, path):
    plt.clf()
    plt.plot(values)
    plt.ylabel(ylabel)
    plt.savefig(path)


def generate_data_plot_image():
    values = get_all_values()
    values = [Device.create_from_dict(value) for value in values]
    values.sort(key=lambda v: v.time)
    temperature_values = [int(value.data["temperature"]) for value in values]
    moisture_values = [int(value.data["moisture"]) for value in values]
    humidity_values = [int(value.data["humidity"]) for value in values]

    plot(temperature_values, "Values", "static/images/temperature_plot.png")


@app.route('/plot.png', methods=["POST"])
def plot_png():
    generate_data_plot_image()
    return render_template('plot_model.html')


@app.route("/update_sensor_values", methods=["POST"])
def update_sensor_values():
    temperature, soil_moisture = get_current_sensor_values()
    return jsonify('', render_template('sensor_values_model.html', temp=temperature, moist=soil_moisture))


@app.route("/update_current_time", methods=["POST"])
def update_current_time():
    return jsonify('', render_template('current_time_model.html', time=get_current_time()))


@app.route('/')
def homepage():
    temperature, soil_moisture = get_current_sensor_values()
    generate_data_plot_image()
    return render_template('home.html', time=get_current_time(), temp=temperature, moist=soil_moisture)


if __name__ == '__main__':
    app.run()
