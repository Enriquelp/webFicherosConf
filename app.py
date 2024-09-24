import sys
sys.path.append('./static/script')  # Agrega el directorio al path para importar el módulo main_resolve_variability
from flask import Flask, flash, jsonify, render_template, abort, make_response, request, send_file, send_from_directory
from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.fm_metamodel.models import FeatureModel, Constraint
from flamapy.metamodels.fm_metamodel.transformations import JSONWriter, JSONReader
from typing import Optional
import os
import subprocess
from static.script.main_resolve_variability import main as generate_conf

app = Flask(__name__)

pathFM = 'static/feature_models/' # Ruta hacia los FM
app.config['UPLOAD_FOLDER'] = 'uploads' # Configurar el folder donde se guardarán los archivos subidos
app.secret_key = 'supersecretkey'  # Para habilitar mensajes flash
error = ''  # Variable para almacenar errores

@app.route('/')
def index():
    global error 
    error = ''
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

@app.route('/upload', methods=['POST'])
def upload_file():
    
    # Obtener el archivo subido
    file = request.files['file']
    
    # Obtener el valor del feature model
    feature_model = request.form.get('feature_model')

    # Verificar que el archivo existe y tiene un nombre
    if file and file.filename:
        # Guardar el archivo temporalmente
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        dest = os.path.join(app.config['UPLOAD_FOLDER'], 'config')
        file.save(filepath)
        global error 
        error = ''

        # Eliminar el archivo de configuración si existe antes de generar el nuevo
        if os.path.exists(dest):
            os.remove(dest)

        # Procesar el archivo subido y crear el archivo de config.yaml
        try:
            if feature_model == 'docker':
                template = 'static/templates/dockerfile_conf_template.txt.jinja'
                mapping = 'static/mapping_models/dockerfile_conf_mapping.csv'

                # Procesar el archivo subido y crear el archivo de config.txt
                configuration, error = generate_conf(filepath, mapping, template, False, False, True, dest)
                print(error)
                # Eliminar el archivo JSON después de procesarlo
                os.remove(filepath)
                return send_file(dest, as_attachment=True, download_name='Dockerfile')
            
            elif feature_model == 'kubernetes': 
                template = 'static/templates/Kubernetes_manifest_v2/Kubernetes_manifest_base.txt.jinja'
                mapping = 'static/mapping_models/Kubernetes_manifest_mapping_v2.csv'

                # Procesar el archivo subido y crear el archivo de config.yaml
                configuration, error = generate_conf(filepath, mapping, template, True, False, False, dest)
                print(error)
                # Eliminar el archivo JSON después de procesarlo
                os.remove(filepath)
                return send_file(dest, as_attachment=True, download_name='config.yaml')
            
        # Manejo de errores si el procesamiento falla
        except Exception as e:
            # Asegurarse de eliminar el archivo JSON si ocurre un error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": f"Error al procesar el archivo: {str(e)}"}), 500
    
@app.route('/check', methods=['GET'])
def check_errors():
    if error != '':
        return jsonify(f"error: {error}"), 200
    else:
        return jsonify(f"There are no errors"), 200

# Manejo de errores 404
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
    