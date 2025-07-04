from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.db'
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)

@app.route("/")
def index():
    pokemons = Pokemon.query.all()
    return render_template("index.html", pokemons=pokemons)

if __name__ == "__main__":
    app.run(debug=True)
