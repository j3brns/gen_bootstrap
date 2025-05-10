# utils/gcp_utils.py

import google_crc32c
from google.cloud import secretmanager

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
        print("Error: GCP Project ID and Secret ID must be provided.")
        # In a real app, consider raising an exception or logging more formally
        return None

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    print(f"Attempting to access secret: {name}")  # Temporary print for debugging

    try:
        response = secret_manager_client.access_secret_version(request={"name": name})

        # Verify payload checksum (optional but recommended)
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print("Warning: Secret payload checksum verification failed.")
            # Depending on policy, you might return None or raise an error here

        payload = response.payload.data.decode("UTF-8")
        print(f"Successfully accessed secret: {secret_id}")  # Temporary print
        return payload
    except Exception as e:
        print(f"Error accessing secret {name}: {e}")
        # Consider more specific exception handling and logging
        return None
