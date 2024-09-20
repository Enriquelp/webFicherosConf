import sys
from flask import Flask, flash, render_template, abort, make_response, request, send_from_directory
from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.fm_metamodel.models import FeatureModel, Constraint
from flamapy.metamodels.fm_metamodel.transformations import JSONWriter, JSONReader
from typing import Optional
import os
import subprocess

app = Flask(__name__)

pathFM = 'static/feature_models/' # Ruta hacia los FM
app.config['UPLOAD_FOLDER'] = 'uploads/' # Configurar el folder donde se guardarán los archivos subidos
app.secret_key = 'supersecretkey'  # Para habilitar mensajes flash

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
        file.save(filepath)
        print(f'filepath: {filepath}')

        try:
            # Procesar el archivo subido
            if feature_model == 'docker':
                template = 'static/templates/dockerfile_conf_template.txt.jinja'
                mapping = 'static/mapping_models/dockerfile_conf_mapping.csv'
                configuration = generate_conf(filepath, mapping, template, False, False, True)
            elif feature_model == 'kubernetes': 
                template = 'static/templates/Kubernetes_manifest_v2/Kubernetes_manifest_base.txt.jinja'
                mapping = 'static/mapping_models/Kubernetes_manifest_mapping_v2.csv'
                configuration = generate_conf(filepath, mapping, template, True, False, False)
                # Guardar el archivo de configuración
                with open("uploads/config.yaml", "w") as f: # Guarda el resultado en un fichero 
                    print('\n')
                    print_without_blank_lines(configuration, f)
                    print('\n')
            
            # Si el archivo se procesó correctamente, devolver el archivo de configuración
            send_from_directory(app.config['UPLOAD_FOLDER'], 'config.yaml', as_attachment=True)

            # Eliminar el archivo después de procesarlo
            os.remove(filepath)
            flash('Archivo procesado y eliminado correctamente')
        
        except Exception as e:
            # Manejo de errores si el procesamiento falla
            flash(f'Error al procesar el archivo: {str(e)}')
            # Asegurarse de eliminar el archivo si ocurre un error
            if os.path.exists(filepath):
                os.remove(filepath)
        
        
    return render_template('index.html', correct='ok')

# Función para generar la configuración final a partir del JSON subido
def generate_conf(config, map, template, kubernetes, details, dockerfile):
    # Llamar al script utilizando subprocess
    try:
        conf = subprocess.run(
            ['python', 'static/script/main_resolve_variability.py', config, map, template, kubernetes, details, dockerfile],
            capture_output=True, text=True
        )

        # Devolver el resultado del script
        return conf 
    
    except Exception as e:
        return str(e) 

# Manejo de errores 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def read_fm_file(filename: str) -> Optional[FeatureModel]:
    fm = UVLReader(filename).transform()
    json_fm = JSONWriter(path=None, source_model=fm).transform()
    response = make_response(json_fm)
    return response

def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verifica si la línea no está en blanco
            sys.stdout.write(line + '\n')  # Escribe la línea en stdout
            file.write(line + '\n')


if __name__ == '__main__':
    app.run(debug=True)
    