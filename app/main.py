import argparse
import json

from agente import crear_agente, preguntar_agente
from gradio_app import  interfaz

def main() -> None:
    """
    Punto de entrada por consola para realizar consultas al agente inteligente via cmd.
    """

    #pregunta1 = '¿Cuál es la idea principal del documento?'
    #pregunta2 = '¿Cuáles son los beneficios activos y si se ofrecen cursos de capacitación?'

    parser = argparse.ArgumentParser(description="Agente inteligente para realizar consulta de las políticas de la organización")
    parser.add_argument("--question", required=True, help="Escriba su consulta a responder")
    args = parser.parse_args()

    agente = crear_agente()
    respuesta = preguntar_agente(agente, args.question)
    
    print(json.dumps(respuesta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    #main()
    interfaz.launch()
