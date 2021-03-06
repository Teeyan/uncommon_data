from flask import Flask, render_template, jsonify, request
import tribe_clustering

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tribe', methods=['GET', 'POST'])
def generate():

    file = request.files['upload']
    json_data = tribe_clustering.tribe_cluster(file)
    return render_template('tribe.html', meta_tribe=json_data[0], tribe_colors=json_data[1])

if __name__ == '__main__':
    app.debug = True
    app.run(port=80, host="0.0.0.0", debug=True)
