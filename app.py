from flask import Flask, render_template, jsonify, request
from tools.clima import get_climate_by_city

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clima', methods=['POST'])
def clima():
    data = request.get_json()
    city_name = data['cidade']
    climate_info = get_climate_by_city(city_name)
    return jsonify(climate_info)

if __name__ == '__main__':
    app.run(debug=True)