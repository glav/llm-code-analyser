import config
import prompt_templates
from ollama_client import LlmClient
from result_store import ResultStore
from solution_file_reader import SolutionFileReader


class CodeQueryEngine:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.ollama_client = LlmClient()
        self.solution_file_reader = SolutionFileReader(base_dir=base_dir)

    async def execute_async(self):
        files = await self.solution_file_reader.get_all_files_async()
        print(f"..First pass\n..Found {len(files)} files")
        results = []
        result_store = ResultStore(descriptive_suffix=config.LOCAL_LLM_MODEL_NAME)
        await result_store.add_result_to_store_async(
            f"Solution Path: {self.base_dir}\n"
        )
        for file in files:
            print(f"..Reading file: {file}")
            contents = await self.solution_file_reader.read_contents_async(file)

            ## need to chunk here
            content_to_submit = f"{contents}"

            print(f"..Querying code in file: {file}")
            # use a different prompt for code and markdown files
            prompt_type = prompt_templates.PROMPT_TYPE_CODE
            if file.endswith(".md") or file.endswith(".txt"):
                prompt_type = prompt_templates.PROMPT_TYPE_MARKDOWN

            response = await self.ollama_client.query_code_async(
                prompt_templates.SYSTEM_PROMPTS[prompt_type],
                prompt_templates.USER_PROMPTS[prompt_type],
                content_to_submit,
                True,
            )
            single_result = f"Filename:{file}\n{response}"
            await result_store.add_result_to_store_async(single_result)
            results.append(single_result)
        print(f"..Results stored in: {result_store.result_file_name}")

        # final summarisation pass
        first_pass_context = await result_store.get_results_from_store_async()

        ######TESTING ONLY
        # import aiofiles

        # async with aiofiles.open("./_results/test_results.txt", "r") as f:
        #     first_pass_context = await f.read()
        ######TESTING ONLY

        response = await self.ollama_client.query_code_async(
            prompt_templates.SYSTEM_PROMPTS[prompt_templates.PROMPT_TYPE_FINAL_SUMMARY],
            prompt_templates.USER_PROMPTS[prompt_templates.PROMPT_TYPE_FINAL_SUMMARY],
            first_pass_context,
            True,
        )
        final_summary = f"---- Final Summary ----\n{response}"
        await result_store.add_result_to_store_async(final_summary)
        print(
            f"..Updated final summarisation results stored in: {result_store.result_file_name}"
        )
