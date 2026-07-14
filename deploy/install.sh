#!/usr/bin/env bash
# Script de instalación y despliegue del agente en una instancia OCI.
# Ejecutar como usuario con permisos sudo (por ejemplo "opc" en Oracle Linux).
set -euo pipefail

APP_DIR="/opt/challenge-ai-agent"
SERVICE_NAME="challenge-ai-agent"

echo "==> Creando entorno virtual e instalando dependencias Python"
python3.12 -m venv "${APP_DIR}/venv"
"${APP_DIR}/venv/bin/pip" install --upgrade pip
"${APP_DIR}/venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

if [ ! -f "${APP_DIR}/.env" ]; then
    echo "==> No se encontró ${APP_DIR}/.env, creando uno a partir de .env.ejemplo"
    cp "${APP_DIR}/.env.ejemplo" "${APP_DIR}/.env"
    echo "    -> Editá ${APP_DIR}/.env y completá las variables de entorno.
fi

echo "==> Instalando el servicio systemd"
sudo cp "${APP_DIR}/deploy/challenge-ai-agent.service" "/etc/systemd/system/${SERVICE_NAME}.service"
sudo systemctl daemon-reload
sudo systemctl enable "${SERVICE_NAME}"
sudo systemctl restart "${SERVICE_NAME}"

echo "==> Listo. Estado del servicio:"
sudo systemctl status "${SERVICE_NAME}" --no-pager || true
echo ""
echo "Ver logs en vivo con: sudo journalctl -u ${SERVICE_NAME} -f"
