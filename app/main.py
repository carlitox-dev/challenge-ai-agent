import argparse
import json

from agente import crear_agente, preguntar_agente

def main() -> None:
    """
    Punto de entrada por consola para realizar consultas al agente inteligente.

    Ejemplo:
    python src/main.py --file data/ejemplo.pdf --question "¿Cuál es el objetivo del documento?"
    """

    pregunta = '¿Cuál es la idea principal del documento?'

    parser = argparse.ArgumentParser(description="Agente inteligente para PDF o CSV")
    #parser.add_argument("--question", required=True, help="Pregunta a responder")
    parser.add_argument("--question", default=pregunta, help="Pregunta a responder")
    args = parser.parse_args()

    agent = crear_agente()
    response = preguntar_agente(agent, args.question)
    
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
