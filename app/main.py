import argparse
import json

from agente import crear_agente, preguntar_agente

def main() -> None:
    """
    Punto de entrada por consola para realizar consultas al agente inteligente.
    """

    pregunta = '¿Cuál es la idea principal del documento?'
    pregunta2 = '¿Cuáles son los beneficios activos y si se ofrecen cursos de capacitación?'

    parser = argparse.ArgumentParser(description="Agente inteligente para realizar consulta sobre documentos PDF o CSV")
    parser.add_argument("--question", required=True, help="Escriba la consulta a responder")
   # parser.add_argument("--question", default=pregunta2, help="Pregunta a responder")
    args = parser.parse_args()

    agente = crear_agente()
    respuesta = preguntar_agente(agente, args.question)
    
    print(json.dumps(respuesta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
