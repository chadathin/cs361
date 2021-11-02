from flask import Flask, render_template, request
#from flask_mysqldb import MySQL
#import yaml
import requests
import json


app = Flask(__name__)

def swap_region_codes(regionDict: dict):
	out={}
	for region in regionDict:
		out[region['name']] = region['id']
	return out

# Make GET request to get body regions for landing page
url = "https://wger.de/api/v2/exercisecategory/"
headers = {"Accept": "application/json"}
r = requests.get(url=url, headers=headers, timeout=1)
r = r.json()

regions = r["results"]
region_to_id_dict = swap_region_codes(regions)			# {'Abs': 10, 'Arms': 8, 'Back': 12, 'Calves': 14, 'Chest': 11, 'Legs': 9, 'Shoulders': 13}

# ============= ROUTES =============

@app.route("/")
def main():
	return render_template('landing.html', regions=regions)

@app.route("/Abs")
def show_abs():
	url = "https://wger.de/api/v2/exercise/"
	params = {"category": region_to_id_dict["Abs"], "language": 2}
	headers = {"Accept": "application/json"}
	abs_exercises = requests.get(url=url, params=params, headers=headers, timeout=1)
	abs_exercises = abs_exercises.json()

	print(abs_exercises) # <- For debugging

	return render_template('abs.html', abs_exercises=abs_exercises)

@app.route("/<exID>")
def show_ex(exID):
	url = "https://wger.de/api/v2/exercise/"

if __name__ == "__main__":
	app.run(debug=True, port=5000)