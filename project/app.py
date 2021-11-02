from flask import Flask, render_template, request
#from flask_mysqldb import MySQL
#import yaml
import requests
import json

app = Flask(__name__)

regions = ['Abs','Arms', 'Back', 'Calves', 'Chest', 'Legs', 'Shoulders']

# ============= ROUTES =============

@app.route("/")
def main():
	return render_template('landing.html', regions=regions)

@app.route("/exercises", methods=["POST"])
def exercises():
	var = request.form['region']
	var = str(var).lower()

	url = "https://exerciseservice.herokuapp.com/exercise/"
	params = {'category': var}
	print(params)
	exercise_list = requests.get(url=url, params=params)

	return exercise_list.json()[30]

# @app.route("/Abs")
# def show_abs():
# 	url = "https://wger.de/api/v2/exercise/"
# 	params = {"category": region_to_id_dict["Abs"], "language": 2}
# 	headers = {"Accept": "application/json"}
# 	abs_exercises = requests.get(url=url, params=params, headers=headers, timeout=1)
# 	abs_exercises = abs_exercises.json()
#
# 	print(abs_exercises) # <- For debugging
#
# 	return render_template('abs.html', abs_exercises=abs_exercises)

# @app.route("/<exID>")
# def show_ex(exID):
# 	url = "https://wger.de/api/v2/exercise/"

if __name__ == "__main__":
	app.run(debug=True, port=5000)