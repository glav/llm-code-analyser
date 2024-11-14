import config
import prompt_templates
from llm_client import LlmClient
from result_store import ResultStore


class ImageComparisonEngine:
    def __init__(self, reference_image_path: str, test_image_path: str):
        self.reference_image_path = reference_image_path
        self.test_image_path = test_image_path
        self.llm_client = LlmClient()

    async def execute_async(self) -> None:
        result_store = ResultStore(
            descriptive_suffix=config.LOCAL_LLM_MODEL_NAME
            if config.LLM_MODE == "local"
            else f"{config.LLM_MODE}_{config.AZURE_LLM_MODEL_NAME}"
        )

        await result_store.add_result_to_store_async(
            f"Reference Architecture Image Path: [{self.reference_image_path}]\nTest Architecture Image Path: [{self.test_image_path}]\n\n"
        )

        response = await self.llm_client.query_code_async(
            prompt_templates.SYSTEM_PROMPTS[
                prompt_templates.PROMPT_TYPE_IMAGE_COMPARISON
            ],
            prompt_templates.USER_PROMPTS[
                prompt_templates.PROMPT_TYPE_IMAGE_COMPARISON
            ],
            "",
            set_context_in_user_prompt=True,
            ref_image_path=self.reference_image_path,
            test_image_path=self.test_image_path,
        )

        await result_store.add_result_to_store_async(response)
        await self.llm_client.close()
        return
