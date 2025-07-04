from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("data/pokedex.json", encoding="utf-8") as f:
        pokemons = json.load(f)
    return render_template("index.html", pokemons=pokemons)

if __name__ == "__main__":
    app.run(debug=True)
