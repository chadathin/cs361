from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import collections
import requests
import json
from sys import getsizeof
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecret'
app.config['SESSION_TYPE'] = 'filesystem'

sesh = Session(app)

def get_artist_id(artist_name: str)->int:
	"""
	:param artist_name: string with underscores instead of spaces, i.e. 'metallica' or 'they_might_be_giants'
	:return: TheAudioDB identifier (int)
	"""

	url = "https://www.theaudiodb.com/api/v1/json/1/search.php?s=" + str(artist_name)
	response = requests.get(url=url)
	response = response.json()
	return response['artists'][0]['idArtist']

def get_artist_albums(artist_ident: int) -> dict:
	"""
	:param artist_ident: int, artist ID from TheAudioDB
	:return: dict of albums released by artist
	"""
	url = "https://theaudiodb.com/api/v1/json/1/album.php?i="+str(artist_ident)
	response = requests.get(url=url)
	response = response.json()
	return response['album']

def scrub_albums(album_dict: dict) -> dict:
	"""
	:param album_dict: dict of albums
	:return: dict of lists of dicts featuring album name and type. Sorted by release year
	"""
	out = collections.OrderedDict()
	for album in album_dict:
		year = album['intYearReleased']
		name = album['strAlbum']
		type = album['strReleaseFormat']
		if year not in out.keys():
			out[year] = []
		if name not in out[year]:
			out[year].append({'name': name, 'type': type})
	return out

regions = ['Abs','Arms', 'Back', 'Calves', 'Chest', 'Legs', 'Shoulders']
muscles = {
	1:"Biceps Brachii",
	2:"Anterior Deltoid",
	3:"Serratus Anterior",
	4:"Pectoralis Major",
	5:"Triceps Brachii",
	6:"Rectus Abdominis",
	7:"Gastrocnemius",
	8:"Gluteus Maxiums",
	9:"Trapezius",
	10:"Quadriceps Femoris",
	11:"Biceps Femoris",
	12:"Latissimus Dorsi",
	13:"Brachialis",
	14:"External Obliques",
	15:"Soleus"
}

# ============= ROUTES =============

@app.route("/")
def main():
	return render_template('landing.html', regions=regions)

@app.route("/exercises", methods=["GET", "POST"])
def exercises():

	var = request.form['category']								#get the value of the clicked region button
	var = str(var).lower()
	url = "https://exerciseservice.herokuapp.com/exercise/"
	headers = {"Accept": "application/json"}
	params = {'category': var}
	result = requests.get(url=url, params=params, headers=headers)
	result = result.json()
	session['exercise_list'] = result["results"]

	return render_template("list.html", result=result)


@app.route("/info", methods=["GET", "POST"])
def showExercise():
	exId = request.form['exercise']
	ex_list = session.get('exercise_list')

	to_show = dict()

	for exercise in ex_list:
		if exercise['id'] == int(exId):
			to_show['name'] = exercise['name']
			to_show['desc'] = exercise['description']
			to_show['muscles'] = exercise['muscles']


	return render_template("exerciseInfo.html", show=to_show, muscle_list=muscles)

@app.route("/fetch/<artist>", methods=["GET"])
def fetch(artist):
	artist_id = get_artist_id(artist)
	albums = get_artist_albums(artist_id)
	discography = scrub_albums(albums)
	discography = jsonify(discography)
	discography.headers.add("Access-Control-Allow-Origin","*")
	return discography



if __name__ == "__main__":
	app.run()