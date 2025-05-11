# utils/gcp_utils.py

import logging  # Import logging

import google_crc32c
from google.cloud import secretmanager

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Initialize the Secret Manager client
secret_manager_client = secretmanager.SecretManagerServiceClient()


def get_secret(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str | None:
    """Retrieves a secret's payload from Google Secret Manager.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret.
        version_id: Version of the secret (defaults to 'latest').

    Returns:
        The secret payload as a string, or None if access fails.
    """
    if not project_id or not secret_id:
        logger.error(
            "GCP Project ID and Secret ID must be provided to get_secret.",
            extra={"project_id": project_id, "secret_id": secret_id},
        )
        return None

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    logger.info(f"Attempting to access secret.", extra={"secret_name": name})

    try:
        response = secret_manager_client.access_secret_version(request={"name": name})

        # Verify payload checksum (optional but recommended)
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            logger.warning(
                "Secret payload checksum verification failed.",
                extra={"secret_name": name},
            )
            # Depending on policy, you might return None or raise an error here.
            # For now, we proceed but log the warning.

        payload = response.payload.data.decode("UTF-8")
        logger.info(
            f"Successfully accessed secret.",
            extra={"secret_name": name, "secret_id": secret_id},
        )
        return payload
    except Exception as e:
        logger.error(
            f"Error accessing secret {name}: {e}",
            exc_info=True,  # Include exception info in the log
            extra={"secret_name": name},
        )
        return None
