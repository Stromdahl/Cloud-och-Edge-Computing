from datetime import datetime
from queue import Queue
from threading import Thread

from flask import Flask, jsonify, Response, render_template, request

from DynamoDB.dynamodb import get_all_values, Device
from mqtt_pub_sub import MQTT

app = Flask(__name__)
app.debug = True
queue = Queue()


def event_stream():
	while True:
		message = queue.get()
		data = {
			"id": message["id"],
			"temperature": message["temperature"],
			"humidity": message["humidity"],
			"moisture": message["moisture"]
		}
		yield f'data: {data["id"]}: {data}\n\n'
		queue.task_done()


@app.route("/")
def line_chart():
	legend = 'Temperatures'
	raw_data = get_all_values()
	data = [Device.create_from_dict(d) for d in raw_data]
	data.sort(key=lambda v: v.time)
	temperatures = [d.temperature for d in data]
	times = [datetime.utcfromtimestamp(d.time).strftime('%Y-%m-%d %H:%M') for d in data]
	return render_template('index.html', values=temperatures, labels=times, legend=legend)


@app.route('/api/stream')
def stream():
	return Response(event_stream(), mimetype='text/event-stream')


@app.route('/api/post')
def post():
	message = request.args.get('sentence')
	queue.put(message)
	return "Sent"


@app.route("/data")
def store_data():
	raw_data = get_all_values()
	data = [Device.create_from_dict(d) for d in raw_data]
	data.sort(key=lambda v: v.time)
	temperatures = [str(d.temperature) for d in data]
	times = [datetime.utcfromtimestamp(d.time).strftime('%Y-%m-%d %H:%M') for d in data]
	return jsonify(temperatures=temperatures, times=times)


if __name__ == "__main__":
	print("if main")
	mqtt = MQTT(queue, listener=True, topic='Mattias/0/data').bootstrap_mqtt()
	mqtt_thread = Thread(target=mqtt.start)
	mqtt_thread.start()
	app.run(threaded=True)
