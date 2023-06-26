from . import main
from .. import FlaskForm, StringField, DataRequired, SubmitField
from .. import render_template, request, current_app
from .. import googlemaps, json
from ..models import PlacesTable
from .. import db

class SearchForm(FlaskForm):
	place = StringField("What place(s) are you interested in?",
						validators=[DataRequired()])
	submit = SubmitField('Submit')

def search_places(place):
	gmaps = googlemaps.Client(key=current_app.config['MAPS_KEY'])
	places = gmaps.places(place)['results']
	return places

def place_is_in_db(place_id):
	if PlacesTable.query.filter_by(place_id=place_id).all():
		return True
	else:
		return False

@main.get('/')
def index():
	form = SearchForm()
	return render_template('index.html', form=form)

@main.get('/search')
def search():
	if request.args:
		places = search_places(request.args['place'])
		return render_template('search.html', places=places)
	return redirect('/')

@main.post('/add-places')
def add_places():
	places_selected = request.form
	places_inserted = []
	places_already_in_db = []
	for place_id in places_selected:
		place = places_selected[place_id].replace("'", '"')
		place = json.loads(place)

		if not place_is_in_db(place_id):
			place_to_be_inserted = PlacesTable(
				place_id=place_id,
				place_address=(place[1]),
				place_name=(place[0]),
				place_type=(place[2][0]))
			db.session.add(place_to_be_inserted)
			places_inserted.append((place[0], place[1]))
		else:
			places_already_in_db.append((place[0], place[1]))
	db.session.commit()
	return render_template('places-added.html',
							places_inserted=places_inserted,
							places_already_in_db=places_already_in_db)