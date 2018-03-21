from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def root():
	return jsonify("Root Page")

@app.route("/1")
def page_one():
	return jsonify("Page 1")

@app.route("/2")
def page_two():
	return jsonify("Page 2")

@app.route("/exit")
def page_exit():
	return jsonify("Halted")

if __name__ == '__main__':
	app.run(debug=True)
