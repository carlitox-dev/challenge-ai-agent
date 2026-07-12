"""
Módulo para obtener secretos desde OCI Vault (Identity & Security > Vault > Secrets).

Autenticación:
    Utiliza por defecto "Instance Principals", el mecanismo recomendado cuando
    la aplicación corre dentro de una instancia de cómputo de OCI: la instancia
    obtiene credenciales temporales automáticamente a través del servicio de
    metadata, sin necesidad de almacenar claves de API en el servidor.

    Para que funcione, la instancia debe pertenecer a un Dynamic Group y debe
    existir una Policy que le otorgue permiso de lectura sobre los secretos,
    por ejemplo:

        Allow dynamic-group <nombre-dynamic-group> to read secret-family \
            in compartment <nombre-compartment>

    Si la app se ejecuta fuera de OCI (por ejemplo en desarrollo local), se
    hace fallback automático a las credenciales del archivo ~/.oci/config.
"""

import base64
import logging
from functools import lru_cache

import oci
from oci.secrets import SecretsClient
from oci.exceptions import ServiceError, ConfigurationError

logger = logging.getLogger(__name__)


def _obtener_signer():
    """
    Devuelve el signer de autenticación a usar contra la API de OCI.

    Prioriza Instance Principals. Si falla (por ejemplo, al no estar
    corriendo dentro de una instancia OCI), intenta con el perfil "DEFAULT"
    del archivo de configuración local de la OCI CLI.
    """
    try:
        return oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
    except Exception as exc:
        logger.warning(
            "No fue posible autenticar via Instance Principals (%s). "
            "Se intentará usar el archivo de configuración local de OCI (~/.oci/config).",
            exc,
        )
        config = oci.config.from_file()
        return oci.signer.Signer(
            tenancy=config["tenancy"],
            user=config["user"],
            fingerprint=config["fingerprint"],
            private_key_file_location=config.get("key_file"),
            pass_phrase=config.get("pass_phrase"),
        )


@lru_cache(maxsize=1)
def _cliente_secretos() -> SecretsClient:
    """
    Crea (una única vez, gracias al cache) el cliente de Secrets de OCI.
    """
    signer = _obtener_signer()
    return SecretsClient(config={}, signer=signer)


@lru_cache(maxsize=32)
def obtener_secreto(secret_ocid: str) -> str:
    """
    Recupera y decodifica el valor en texto plano de un secreto de OCI Vault.

    El resultado se cachea en memoria por OCID para evitar llamadas
    repetidas a la API en cada consulta.

    Args:
        secret_ocid (str): OCID del secreto (ocid1.vaultsecret.oc1...).

    Returns:
        str: Valor en texto plano del secreto.
    """
    if not secret_ocid:
        raise ValueError("Se requiere el OCID del secreto para poder consultarlo.")

    cliente = _cliente_secretos()

    try:
        respuesta = cliente.get_secret_bundle(secret_id=secret_ocid)
    except (ServiceError, ConfigurationError) as exc:
        logger.error("Error al obtener el secreto '%s' desde OCI Vault: %s", secret_ocid, exc)
        raise

    contenido_base64 = respuesta.data.secret_bundle_content.content
    return base64.b64decode(contenido_base64).decode("utf-8")
