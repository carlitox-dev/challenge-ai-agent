from pathlib import Path
from typing import List, Tuple

import gradio as gr

from agente import crear_agente, preguntar_agente

current_agent = None

def cargar_agente():
    """
    Carga o reutiliza el agente para el archivo subido por el usuario.

    El índice vectorial se persiste en disco, por lo que si el documento ya fue
    procesado anteriormente, la carga será más rápida y no reconstruirá los chunks.
    """
    global current_agent, current_file

    current_agent = crear_agente()


def chatear_con_agente(message: str, history: List[dict]) -> Tuple[List[dict], List[dict]]:
    """Envía preguntas al agente y mantiene el historial del chat.

    El usuario puede realizar tantas preguntas como necesite sobre el documento
    cargado, reutilizando el mismo agente durante la sesión.
    """
    global current_agent

    if current_agent is None:
        history.append(
            {
                "role": "assistant",
                "content": "Primero debes subir un archivo y presionar 'Procesar documento'.",
            }
        )
        return history, history

    history.append({"role": "user", "content": message})

    resultado = preguntar_agente(current_agent, message)
    respuesta = resultado["answer"]
    # fuentes = resultado["sources"]

    # if respuesta:
    #     sources_text = "\n".join(
    #         [f"- source: {item['source']} | page: {item['page']}" for item in fuentes]
    #     )
    #     full_answer = f"{respuesta}\n\nFuentes:\n{sources_text}"
    # else:
    #     full_answer = respuesta

    history.append({"role": "assistant", "content": respuesta})
    return history, history


def limpiar_chat() -> tuple[list, list]:
    """
    Limpia el historial visual del chat.
    """
    return [], []

with gr.Blocks(title="Agente Inteligente Documental") as interfaz:
    
    gr.Markdown("# Agente Inteligente Documental")
    gr.Markdown("Hola! Soy _**Poli**_, tu Asistente con Inteligencia Artificial. 🤖")
    gr.Markdown("Puedo ayudarte a resolver cualquier duda sobre la documentación de _Onboarding para Nuevos Desarrolladores_, " \
    "como: estructura del equipo, beneficios, configuración de entornos, políticas de seguridad y más.")
    gr.Markdown("¿Qué qué te gustaría consultar? 🤔❓")

    cargar_agente()

    chatbot = gr.Chatbot(label="Conversación")
    msg = gr.Textbox(
        label="Consulta:",
        placeholder="Escribe una pregunta sobre las políticas de la organización...",
    )

    with gr.Row():
        send_button = gr.Button("Enviar", variant="primary")
        clear_button = gr.Button("Limpiar chat")

    chat_state = gr.State([])

    send_button.click(chatear_con_agente, inputs=[msg, chat_state], outputs=[chatbot, chat_state]).then(lambda: "", None, msg)
    msg.submit(chatear_con_agente, inputs=[msg, chat_state], outputs=[chatbot, chat_state]).then(lambda: "", None, msg)
    clear_button.click(limpiar_chat, inputs=None, outputs=[chatbot, chat_state]).then(lambda: "", None, msg)


if __name__ == "__main__":
    interfaz.launch()
