import json


def load_json(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        return json.load(archivo)