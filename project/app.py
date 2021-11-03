from flask import Flask, render_template, request
import collections
import requests
import json

app = Flask(__name__)

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

	return exercise_list.json()[0]


@app.route("/fetch/<artist>")
def fetch(artist):
	artist_id = get_artist_id(artist)
	albums = get_artist_albums(artist_id)
	discography = scrub_albums(albums)
	return discography



if __name__ == "__main__":
	app.run()