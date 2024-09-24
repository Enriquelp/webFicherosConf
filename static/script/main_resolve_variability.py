import os
import argparse
import csv
import sys
from typing import Any

import jinja2

from spl_implementation.utils import utils
from spl_implementation.models import VEngine
import subprocess

def main(config, map, template, kubernetes, details, dockerfile, dest):
    kubeconform = "static/validators/kubeconform.exe"
    hadolint = 'static/validators/hadolint.exe'
    error = ''
    

    # Carga los archivos necesarios
    vengine = VEngine()
    vengine.load_configuration(config)
    vengine.load_mapping_model(map)
    vengine.load_template(template)

    # Resuelve la variabilidad
    result = vengine.resolve_variability()

    # Guarda el resultado en un fichero 
    with open(dest, "w") as f: 
        print_without_blank_lines(result, f)


    # Comprueba si existe algun error en el YAML de kubernetes
    if(kubernetes): 
        rdo = subprocess.run([kubeconform, dest], capture_output=True, text=True)
        if (rdo.stdout != ''):
            error = f"ERROR: {rdo.stdout}" 
    # Comprueba si existe algun error en el Dockerfile
    if (dockerfile):
         rdo = subprocess.run([hadolint, dest], capture_output=True, text=True)
         if (rdo.stdout != ''):
            error = f"ERROR: {rdo.stdout}"     

    return result, error

def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verifica si la línea no está en blanco
            # sys.stdout.write(line + '\n')  # Para mostrar la configuracion en la terminal
            file.write(line + '\n')

if __name__ == '__main__':
    main()