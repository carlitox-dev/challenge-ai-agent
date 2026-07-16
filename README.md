
# 🤖 Poli — Agente Inteligente Documental

### Agente conversacional basado en RAG (*Retrieval-Augmented Generation*) para realizar consultas en lenguaje natural.


[![Python](https://img.shields.io/badge/Python-blue)](https://python.org)
[![Groq](https://img.shields.io/badge/API_Model-Groq-red)](https://groq.com/)
[![Embeddings](https://img.shields.io/badge/Embeddings-HuggingFace-yellow)]()
[![OCI](https://img.shields.io/badge/Infraestructure-OCI-red)](https://www.oracle.com/cloud)
[![FAISS](https://img.shields.io/badge/Vector_Store-FAISS-green)]()
[![Gradio](https://img.shields.io/badge/Interface-Gradio-orange)]()
[![Nginx](https://img.shields.io/badge/Proxy-Nginx-green)](https://nginx.org/)
[![MIT](https://img.shields.io/badge/License-MIT-orange)]()

---

Agente conversacional basado en RAG (*Retrieval-Augmented Generation*) que permite consultar, en lenguaje natural, la documentación interna de onboarding para nuevos desarrolladores de Santo Pegasus Soluciones.

El agente recupera fragmentos relevantes del documento fuente y genera respuestas precisas y contextualizadas usando un modelo de lenguaje de gran escala.



## 🗒️ Índice

1. [Descripción general](#descripción-general)
2. [Arquitectura de la solución](#arquitectura-de-la-solución)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Tecnologías y herramientas](#tecnologías-y-herramientas)
5. [Instrucciones de instalación y ejecución](#instrucciones-de-instalación-y-ejecución)
6. [Despliegue en OCI](#despliegue-en-oci)
7. [Ejemplos de preguntas y respuestas](#ejemplos-de-preguntas-y-respuestas)



## ✨ Descripción general

**Poli** es un asistente virtual especializado en la documentación de onboarding de Santo Pegasus Soluciones. 

Responde preguntas sobre:

* Misión y Visión de la organización.
* Estructura y roles del equipo
* Beneficios y políticas internas
* Pila Tecnológica Principal
* Acceso y cuentas
* Políticas de seguridad
* Flujos y procesos operativos, y mucho más


El agente procesa el documento fuente una única vez, construye un índice vectorial persistente en disco y lo reutiliza en consultas posteriores, minimizando el tiempo de respuesta y el costo computacional.


## 💻 Arquitectura de la solución

```
                      Usuario
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                  Interfaz Gradio                    │
│              (gradio_app.py · puerto 7860)          │
└────────────────────────┬────────────────────────────┘
                         │ pregunta
                         ▼
┌─────────────────────────────────────────────────────┐
│                    Agente RAG                       │
│                   (agente.py)                       │
│                                                     │
│  1. Resuelve la ruta del documento fuente           │
│  2. Carga los documentos (PDF / CSV)                │
│  3. Obtiene o crea el índice vectorial FAISS        │
│  4. Construye un retriever (top-4 chunks)           │
│  5. Invoca el LLM con contexto recuperado           │
└───────────┬─────────────────────────┬───────────────┘
            │                         │
            ▼                         ▼
┌─────────────────────┐   ┌────────────────────────────┐
│  Carga de documentos│   │    Vector Store (FAISS)    │
│  (document_loader)  │   │    (vector_store.py)       │
│                     │   │                            │
│  PyPDFLoader (PDF)  │   │  HuggingFace Embeddings    │
│  pandas (CSV)       │   │  all-MiniLM-L6-v2          │
└─────────────────────┘   │  Persistido en:            │
                          │  storage/vector_index/     │
                          └────────────────────────────┘
                                       │
                                       ▼
                          ┌───────────────────────────┐
                          │    LLM (Groq / LLaMA)     │
                          │  llama-3.3-70b-versatile  │
                          └───────────────────────────┘
```

### 🔀 Flujo de procesamiento

```
Inicio
  │
  ├─► ¿Existe índice vectorial en disco?
  │     │
  │    Sí ──────► Cargar FAISS desde storage/vector_index/
  │    No ──────► Cargar PDF/CSV → Chunking → Embeddings → Crear y guardar índice
  │
  └─► Retriever recupera top-4 chunks relevantes
        │
        └─► LLM genera respuesta con contexto → Usuario
```

## 📁 Estructura del proyecto

```
challenge-ai-agent/
│
├── app/                          # Código fuente principal
│   ├── main.py                   # Punto de entrada; lanza la interfaz Gradio
│   ├── agente.py                 # Construcción del agente RAG (RetrievalQA)
│   ├── gradio_app.py             # Definición de la interfaz web con Gradio
│   ├── document_loader.py        # Carga de documentos PDF y CSV
│   ├── vector_store.py           # Creación, persistencia y carga del índice FAISS
│   ├── config.py                 # Configuración centralizada vía variables de entorno
│   └── secrets_manager.py        # Integración con OCI Vault para gestión de secretos
│
├── data/                         # Documentos fuente para base de conocimiento
│   └── documento.pdf             # Documento de onboarding principal (carga manual)
│
├── storage/                      # Índice vectorial persistido en disco (generado en runtime)
│   └── vector_index/
│       └── documento/            # Carpeta del índice FAISS para el documento activo
│
├── deploy/                       # Artefactos de despliegue en OCI
│   ├── install.sh                # Script de instalación: venv, dependencias y servicio systemd
│   └── challenge-ai-agent.service # Unidad systemd para ejecutar la app como servicio
│
├── screenshots/                  # Capturas de la aplicación desplegada y funcionando en la nube 
│
├── requirements.txt              # Dependencias Python necesarias para el proyecto
├── .env.ejemplo                  # Plantilla de variables de entorno (copiar a .env)
├── .env                          # Variables de entorno activas
├── .gitignore                    # Archivos excluidos del control de versiones
├── LICENSE                       # Licencia MIT
└── README.md                     # Documentación principal del proyecto
```

### 📋 Descripción de los módulos principales

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada. Expone la interfaz Gradio en `0.0.0.0:7860`. |
| `agente.py` | Ensambla el pipeline RAG: resolución de rutas, carga de documentos, vector store y LLM. |
| `gradio_app.py` | Define la UI conversacional, maneja el historial de chat y delega al agente. |
| `document_loader.py` | Abstrae la carga de PDF (PyPDF) y CSV (pandas) en documentos LangChain. |
| `vector_store.py` | Gestiona el ciclo de vida del índice FAISS: chunking, embeddings, persistencia y carga. |
| `config.py` | Centraliza toda la configuración mediante variables de entorno con valores por defecto. |
| `secrets_manager.py` | Recupera secretos desde OCI Vault usando Instance Principals, con fallback a `~/.oci/config`. |


## 🧑‍💻Tecnologías y herramientas

|Capa|Tecnología|Versión mínima|
|-|-|-|
|Lenguaje|Python|3.12|
|Framework de agentes|LangChain|0.3.0|
|LLM provider|Groq (LLaMA 3.3 70B)|langchain-groq 0.3.6|
|Embeddings|HuggingFace `all-MiniLM-L6-v2`|sentence-transformers 3.0|
|Vector store|FAISS (CPU)|faiss-cpu 1.8.0|
|Carga de documentos|PyPDF / pandas|pypdf 5.0, pandas 2.2|
|Interfaz de usuario|Gradio|5.38.0|
|Infraestructura|Oracle Cloud (OCI)|Oracle Linux 9.7|
|Gestor de servicio|systemd|—|
|Proxy inverso|NGINX|—|



## ⌨️ Instrucciones de instalación y ejecución

### Requisitos previos

* Python 3.12
* `git`
* Cuenta en [Groq](https://console.groq.com) para obtener una API Key activa

### 1\. Clonar el repositorio

```bash
git clone https://github.com/carlitox-dev/challenge-ai-agent
cd challenge-ai-agent
```

### 2\. Crear el entorno virtual e instalar dependencias

```bash
python3.12 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3\. Configurar variables de entorno

```bash
cp .env.ejemplo .env
```

Editá `.env` y completá los valores:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx # Completá con tu API Key generado en tu cuenta de Groq
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
```

### 4\. Ejecutar la aplicación

**Interfaz web Gradio:**

```bash
cd app
python main.py
```

La interfaz quedará disponible en `http://localhost:7860`.


## ☁️ Despliegue en OCI

### Requisitos

* Instancia OCI con Oracle Linux 9.7 y Python 3.12
* El usuario de la instancia (`opc`) con acceso a `sudo`

### 1\. Transferir / Clonar el proyecto a la instancia OCI

```bash
# Desde tu máquina local
scp -r challenge-ai-agent/ opc@167.234.232.34:/opt/
```

O, clonar el repositorio. Ver punto 1 del paso Instrucciones de Instalación

### 2\. Ejecutar el script de instalación

```bash
ssh opc@167.234.232.34
cd /opt/challenge-ai-agent
bash deploy/install.sh
```

El script instala el entorno virtual, las dependencias, y registra el servicio en systemd.

### 3\. Verificar el servicio

```bash
sudo systemctl status challenge-ai-agent
sudo journalctl -u challenge-ai-agent -f     # logs en tiempo real
```

### 4\. Exponer la aplicación con NGINX

```bash
sudo dnf install -y nginx
sudo systemctl enable --now nginx
```

Crear `/etc/nginx/conf.d/gradio.conf`:

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass         http://127.0.0.1:7860;
        proxy_http_version 1.1;
        # Necesario para WebSockets — Gradio los usa intensivamente para el chat en tiempo real
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
        proxy_set_header   Host            $host;
        proxy_set_header   X-Real-IP       $remote_addr;
        proxy_read_timeout 300s;
    }
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
```

### 5\. Abrir el puerto en el firewall y la Security List de OCI

```bash
# Firewall del sistema operativo
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --reload
```

En la consola de OCI: **Networking → VCN → Security Lists → Ingress Rules**
Agregar regla: `TCP / Source 0.0.0.0/0 / Destination port 80`.

La aplicación quedará accesible en `http://167.234.232.34`.


## 🤔 Ejemplos de preguntas y respuestas

Las siguientes preguntas son representativas de lo que el agente puede responder a partir del documento de onboarding.

--- 
**Pregunta:** ¿Cómo está organizado el equipo de desarrollo?

**Respuesta:**

> Según el texto proporcionado, el equipo de desarrollo de Santo Pegasus Soluciones parece estar organizado de la siguiente manera:
>   * Hay desarrolladores Senior o Pleno que actúan como "buddies" o mentores para los nuevos miembros del equipo, acompañándolos durante sus primeros 30 días.
>   * El equipo tiene una estructura jerárquica, con desarrolladores Senior o Pleno que revisan y aprueban el código de los demás miembros del equipo.
>  * El equipo utiliza un sistema de revisión de código, donde se asignan revisores para evaluar y aprobar los cambios de código antes de que se mergen en la rama principal.
>   * El equipo utiliza herramientas como Jira para gestionar los tickets y el flujo de trabajo.

> Sin embargo, no se proporciona información detallada sobre la estructura organizativa del equipo, como la existencia de equipos específicos, líderes de equipo o roles específicos.

---

**Pregunta:** ¿Ofrecen trabajo remoto?

**Respuesta:**

> Sí, Santo Pegasus ofrece un modelo híbrido de trabajo que incluye la opción de trabajar de manera remota. De hecho, se menciona que la mayoría del equipo trabaja de manera remota, con encuentros presenciales opcionales o requeridos en casos específicos. También se menciona que la asistencia presencial es opcional, salvo en eventos específicos del equipo, lo que sugiere que el trabajo remoto es una opción común en la empresa.

---

**Pregunta:** ¿Qué herramientas necesito instalar para configurar mi entorno de desarrollo?

**Respuesta:**

> Según el manual de onboarding, necesitarás instalar las siguientes herramientas para configurar tu entorno de desarrollo:
> * Slack
> * Acceso a GitHub (organización privada)
> * Configuración del entorno local para Back-end (sección 4 del manual)
> * Configuración del entorno local para Front-end (sección 5 del manual)
> Además, se menciona que necesitarás configurar tu correo corporativo (@santopegasus.com) y tener acceso a Jira para trabajar con tickets. Sin embargo, no se especifica si Jira necesita ser instalado o si es una herramienta web a la que se accede a través de un navegador.

> Es posible que necesites instalar otras herramientas adicionales, pero según la información proporcionada, estas son las mencionadas explícitamente en el manual.

---

**Pregunta:** ¿Cuáles son las políticas de seguridad que debo seguir?

**Respuesta:**

> Según el texto, las políticas de seguridad que debes seguir son:
> * No hardcodear credenciales: No debes incluir credenciales directamente en el código.
> * Validación de entradas: Debes validar las entradas para evitar problemas de seguridad.
> * No exponer información sensible: No debes exponer información sensible en el código o en otros lugares.
> * Uso de 1Password: Debes usar 1Password como gestor de contraseñas corporativo para almacenar todas las contraseñas relacionadas con sistemas de la empresa.
> * Reglas básicas de gestión de contraseñas:
>   * No reutilizar contraseñas entre sistemas.
>   * Todas las contraseñas corporativas deben tener al menos 20 caracteres y ser generadas por 1Password.
> Además, se menciona que la empresa sigue una política de "Artesanía del Código" y "Honestidad Técnica", lo que implica que se debe escribir código claro y honesto, y admitir errores si se cometen.

---

### Preguntas fuera del contexto

**Pregunta:** Pronóstico del tiempo para hoy?

**Respuesta:**

> No tengo información sobre el pronóstico del tiempo para hoy. La información proporcionada se refiere a una guía de ingeniería back-end y políticas de una empresa, pero no incluye datos sobre el clima. Si necesitas saber el pronóstico del tiempo, te recomiendo consultar un servicio de meteorología en línea o una aplicación de clima.

---

**Nota:** Las respuestas anteriores son ejemplos ilustrativos. El contenido exacto dependerá del documento `data/documento.pdf` configurado en el proyecto.

---

## 👨‍💻 Autor

**Carlos Patiño**

* GitHub: https://github.com/carlitox-dev
* LinkedIn: https://www.linkedin.com/in/carlospatino89/
* Correo: copb89@gmail.com
