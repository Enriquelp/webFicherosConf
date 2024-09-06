from flask import Flask, render_template, abort, make_response
from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.fm_metamodel.models import FeatureModel, Constraint
from flamapy.metamodels.fm_metamodel.transformations import JSONWriter, JSONReader
from typing import Optional
import os

app = Flask(__name__)

pathFM = 'static/feature_models/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/load_page/<page>')
def load_page(page):
    if page not in ['docker', 'kubernetes']:
        abort(404)
    return render_template(f'{page}.html')

@app.route('/load_fm/<model>')
def load_model(model):
    fm = f'{pathFM}{model}.uvl'
    if not os.path.exists(fm):
        abort(404)
    return read_fm_file(fm)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def read_fm_file(filename: str) -> Optional[FeatureModel]:
    fm = UVLReader(filename).transform()
    json_fm = JSONWriter(path=None, source_model=fm).transform()
    response = make_response(json_fm)
    return response

if __name__ == '__main__':
    app.run(debug=True)