import os
import argparse
import csv
import sys
from typing import Any

import jinja2

from spl_implementation.utils import utils
from spl_implementation.models import VEngine
import subprocess

import click

# ARGUMENTOS CLICK
@click.command()
@click.option('--config', '-c', required=True, type=click.Path(exists=True), default='', help='Ruta al fichero de configuracion del FM')
@click.option('--map', '-m', required=True, type=click.Path(exists=True), default='', help='Ruta al fichero del mapping')
@click.option('--template', '-t', required=True, type=click.Path(exists=True), default='', help='ruta al fichero template')
@click.option('--kubernetes', '-k', is_flag=True, help='Indica si se debe comprobar la validez del resultado para kubernetes')
@click.option('--details', is_flag=True, help='Indica si se debe dar detalles de optimización del fichero YAML')
@click.option('--dockerfile', '-d', is_flag=True, help='Indica si se debe comprobar la validez del resultado para kubernetes')

def main(config, map, template, kubernetes, details, dockerfile):
    kubeconform = "validators/kubeconform.exe"
    kube_score = "validators/kube-score.exe"
    hadolint = 'validators/hadolint.exe'
    vengine = VEngine()

    vengine.load_configuration(config)
    vengine.load_mapping_model(map)
    vengine.load_template(template)

    result = vengine.resolve_variability()

    with open("salida.yaml", "w") as f: # Guarda el resultado en un fichero 
        print('\n')
        print_without_blank_lines(result, f)
        print('\n')
    
    if(kubernetes): # Comprueba si existe algun error en el YAML de kubernetes
        rdo = subprocess.run([kubeconform, "salida.yaml"], capture_output=True, text=True)
        if (rdo.stdout != ''):
            print(f"\033[91m ERROR: {rdo.stdout} \033[0m") # Imprime el resultado de la comprobacion en rojo
        if(details):
            details = subprocess.run([kube_score, "score", "salida.yaml"], capture_output=True, text=True) # Analiza el resultado en busca de recomendaciones
            print(f"\033[92m RECOMMENDATIONS: {details.stdout} \033[0m")
    if (dockerfile):
         rdo = subprocess.run([hadolint, "salida.yaml"], capture_output=True, text=True)
         print(f"\033[91m ERROR: {rdo.stdout} \033[0m") # Imprime el resultado de la comprobacion en rojo
def print_without_blank_lines(text, file):
    for line in text.splitlines():
        if line.strip():  # Verifica si la línea no está en blanco
            sys.stdout.write(line + '\n')  # Escribe la línea en stdout
            file.write(line + '\n')

if __name__ == '__main__':
    main()