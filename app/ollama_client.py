import asyncio

import config
from ollama import AsyncClient


class OllamaClient:
    def __init__(self):
        self.client = AsyncClient()

    async def query_code_async(
        self, system_prompt, user_prompt, context, set_context_in_user_prompt=False
    ) -> str:
        # Found the below setup (context in system) not as effective as putting the context in the user prompt
        # when performing a summary of summaries and other scenarios.
        # The context in the system prompt was effective when analysing code though
        # which is why the flag here is available
        if set_context_in_user_prompt:
            user_prompt = f"{user_prompt} ```\nContext:\n" + context + "\n```"
        else:
            system_prompt = f"{system_prompt} ```\nContext:\n" + context + "\n```"
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]
        return await self.client.chat(
            model=config.LOCAL_LLM_MODEL_NAME, messages=messages
        )

    def list(self):
        return self.client.list()


## Just for testing
async def chat():
    message = {"role": "user", "content": "Tell me a dad joke"}
    response = await AsyncClient().chat(
        model=config.LOCAL_LLM_MODEL_NAME, messages=[message]
    )
    print(response["message"]["content"])


if __name__ == "__main__":
    asyncio.run(chat())

# response = ollama.chat(
#     model="llama3.1:latest",
#     messages=[
#         {
#             "role": "user",
#             "content": "Why is grass green?",
#         },
#     ],
# )

# print(response)
# print(response["message"]["content"])

# x = ollama.list()
# print(x)
