import config
from azure.identity.aio import DefaultAzureCredential
from ollama import AsyncClient
from openai import AsyncAzureOpenAI
from utils import (
    delete_blob_from_blob_storage,
    upload_image_to_blob_storage_with_identity,
)


class LlmClient:
    def __init__(self):
        if config.LLM_MODE == "azure":
            self.client = AzureClient()
        elif config.LLM_MODE == "local":
            self.client = OllamaClient()
        else:
            raise ValueError(f"LLM_MODE: {config.LLM_MODE} not supported")

    async def query_code_async(
        self,
        system_prompt,
        user_prompt,
        context,
        set_context_in_user_prompt=False,
        ref_image_path=None,
        test_image_path=None,
    ) -> str:
        # Found the below setup (context in system) not as effective as putting the context in the user prompt
        # when performing a summary of summaries and other scenarios.
        # The context in the system prompt was effective when analysing code though
        # which is why the flag here is available
        if set_context_in_user_prompt:
            user_prompt = f"{user_prompt} ```\nContext:\n" + context + "\n```"
        else:
            system_prompt = f"{system_prompt} ```\nContext:\n" + context + "\n```"

        user_message = {
            "role": "user",
            "content": user_prompt,
            "images": [ref_image_path, test_image_path]
            if ref_image_path and test_image_path
            else [],
        }

        if config.LLM_MODE == "azure" and ref_image_path and test_image_path:
            # reference_image_url = await upload_image_to_blob_storage(
            reference_image_url = await upload_image_to_blob_storage_with_identity(
                ref_image_path,
                config.AZURE_STORAGE_CONTAINER_NAME,
                "reference_image.jpg",
            )
            # test_image_url = await upload_image_to_blob_storage(
            test_image_url = await upload_image_to_blob_storage_with_identity(
                test_image_path,
                config.AZURE_STORAGE_CONTAINER_NAME,
                "test_image.jpg",
            )

            user_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt,
                    },
                    {
                        "image_url": {"url": reference_image_url, "detail": "auto"},
                        "type": "image_url",
                    },
                    {
                        "image_url": {"url": test_image_url, "detail": "auto"},
                        "type": "image_url",
                    },
                ],
            }

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            user_message,
        ]

        query_response = await self.client.query_code_async(
            messages=messages,
        )
        await self.client.close()
        if config.LLM_MODE == "azure" and ref_image_path and test_image_path:
            await delete_blob_from_blob_storage(
                config.AZURE_STORAGE_CONTAINER_NAME, "reference_image.jpg"
            )
            await delete_blob_from_blob_storage(
                config.AZURE_STORAGE_CONTAINER_NAME, "test_image.jpg"
            )
        return query_response


class AzureClient:
    def __init__(self):
        # self.client = AsyncAzureOpenAI(
        #     api_key=config.AZURE_OPENAI_API_KEY,
        #     api_version=config.AZURE_API_VERSION,
        #     azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        # )
        credential = DefaultAzureCredential()
        self.client = AsyncAzureOpenAI(
            credential=credential,
            api_version=config.AZURE_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        )
        self.client = AsyncAzureOpenAI(
            credential=credential,
            api_version=config.AZURE_API_VERSION,
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
        )

    async def query_code_async(self, messages: list[dict[str, str]]) -> str:
        chat_completion = await self.client.chat.completions.create(
            model=config.AZURE_LLM_MODEL_NAME, messages=messages
        )
        return chat_completion.choices[0].message.content

    async def close(self):
        await self.client.close()


class OllamaClient:
    def __init__(self):
        self.client = AsyncClient()

    async def query_code_async(self, messages: list[dict[str, str]]) -> str:
        chat_completion = await self.client.chat(
            model=config.LOCAL_LLM_MODEL_NAME, messages=messages
        )
        return chat_completion["message"]["content"]

    def list(self):
        return self.client.list()

    async def close(self):
        return  # Does nothing, no close on OllamaClient needed but matches AzureClient API
