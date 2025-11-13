from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

apiKey ="1320e414b5414686ac59e14362f5a2d3"
api_url = "https://spoonacular.com/"

app = Flask(__name__)
app.secret_key = "cuando_donde_tiras_queso"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=["POST"])
def search():
    pokemon_name = request.form.get('Api', '').strip().lower()

    if not pokemon_name:
        flash('Ingrese un pokemon', 'error')
        return redirect(url_for('index'))

    try:
        resp = requests.get(f"{POKEAPI}{pokemon_name}")
        if resp.status_code == 200:
            pokemon_data = resp.json()
            
            pokemon_info = {
                'name': pokemon_data['name'].title(),
                'id': pokemon_data['id'],
                'height': pokemon_data['height'] / 10,
                'weight': pokemon_data['weight'] / 10,
                'sprite': pokemon_data['sprites']['front_default'],
                'types': [t['type']['name'].title() for t in pokemon_data['types']],
                'abilities': [a['ability']['name'].title() for a in pokemon_data['abilities']],
            }
            return render_template('pokemon.html', pokemon=pokemon_info)
        else:
            flash(f'Pokemon "{ pokemon_name }" no encontrado', 'error')
            return redirect(url_for('index'))
    except requests.exceptions.RequestException as e:
        flash('Error al buscar el Pokemon', 'error')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)