from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Juscute@localhost/song_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db = SQLAlchemy(app)

# Song model
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=False)
    release_year = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'release_year': self.release_year
        }

# CREATE (POST) - Create a new song
@app.route("/songs", methods=["POST"])
def create_song():
    data = request.get_json()
    if not data or "title" not in data or "artist" not in data:
        return jsonify({"error": "Invalid input data"}), 400

    new_song = Song(title=data["title"], artist=data["artist"], album=data["album"], release_year=data["release_year"])
    db.session.add(new_song)
    db.session.commit()
    return jsonify(new_song.to_dict()), 201

# READ (GET) - Retrieve all songs
@app.route("/songs", methods=["GET"])
def get_songs():
    songs = Song.query.all()
    return jsonify([song.to_dict() for song in songs]), 200

# READ (GET) - Retrieve a specific song
@app.route("/songs/<int:song_id>", methods=["GET"])
def get_song(song_id):
    song = Song.query.get(song_id)
    if song:
        return jsonify(song.to_dict()), 200
    return jsonify({"error": "Song not found"}), 404

# UPDATE (PUT) - Update a song
@app.route("/songs/<int:song_id>", methods=["PUT"])
def update_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404

    data = request.get_json()
    if not data or "title" not in data or "artist" not in data:
        return jsonify({"error": "Invalid input data"}), 400

    song.title = data["title"]
    song.artist = data["artist"]
    song.album = data["album"]
    song.release_year = data["release_year"]
    db.session.commit()
    return jsonify(song.to_dict()), 200

# DELETE (DELETE) - Delete a song
@app.route("/songs/<int:song_id>", methods=["DELETE"])
def delete_song(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"error": "Song not found"}), 404

    db.session.delete(song)
    db.session.commit()
    return "", 204

if __name__ == "__main__":
    app.run()
