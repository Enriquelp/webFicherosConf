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
    kube_score = "static/validators/kube-score.exe"
    hadolint = 'static/validators/hadolint.exe'
    vengine = VEngine()

    vengine.load_configuration(config)
    vengine.load_mapping_model(map)
    vengine.load_template(template)

    result = vengine.resolve_variability()

    with open(dest, "w") as f: # Guarda el resultado en un fichero 
        print_without_blank_lines(result, f)

    return result

def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verifica si la línea no está en blanco
            # sys.stdout.write(line + '\n')  # Para mostrar la configuracion en la terminal
            file.write(line + '\n')

if __name__ == '__main__':
    main()