import config
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob import ContentSettings
from azure.storage.blob.aio import BlobServiceClient


async def upload_image_to_blob_storage_with_identity(
    file_path, container_name, blob_name
):
    credential = DefaultAzureCredential()
    async with BlobServiceClient(
        account_url=config.AZURE_STORAGE_ACCOUNT_URL, credential=credential
    ) as blob_service_client:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        with open(file_path, "rb") as data:
            await blob_client.upload_blob(
                data,
                overwrite=True,
                content_settings=ContentSettings(content_type="image/jpeg"),
            )
        blob_url = blob_client.url
        return blob_url


async def upload_image_to_blob_storage(file_path, container_name, blob_name):
    async with BlobServiceClient.from_connection_string(
        config.AZURE_STORAGE_CONNECTION_STRING
    ) as blob_service_client:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        with open(file_path, "rb") as data:
            await blob_client.upload_blob(
                data,
                overwrite=True,
                content_settings=ContentSettings(content_type="image/jpeg"),
            )
        blob_url = blob_client.url
        return blob_url


async def delete_blob_from_blob_storage(container_name, blob_name):
    async with BlobServiceClient.from_connection_string(
        config.AZURE_STORAGE_CONNECTION_STRING
    ) as blob_service_client:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        await blob_client.delete_blob()
