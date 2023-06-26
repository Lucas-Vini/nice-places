from . import db

class PlacesTable(db.Model):
	__tablename__ = 'places'
	place_id = db.Column(db.String(64), primary_key = True)
	place_address = db.Column(db.String(128))
	place_name = db.Column(db.String(64))
	place_type = db.Column(db.String(32))

	def __repr__(self):
		return '<Place %r>' % self.place_name