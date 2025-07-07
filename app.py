from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokedex.db'
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    type1 = db.Column(db.String(10), nullable=False)
    type2 = db.Column(db.String(10))

@app.route("/")
def index():
    pokemons = Pokemon.query.all()
    return render_template("index.html", pokemons=pokemons)

@app.route("/detail/<int:pokemon_id>")
def detail(pokemon_id):
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return render_template("detail.html", pokemon=pokemon)

if __name__ == "__main__":
    app.run(debug=True)
