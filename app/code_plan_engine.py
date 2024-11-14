import config
import prompt_templates
from code_plan_summary import CodePlanSummary
from llm_client import LlmClient
from result_store import ResultStore
from solution_file_reader import SolutionFileReader


class CodePlanEngine:
    def __init__(self, base_dir: str, result_file: str):
        self.base_dir = base_dir
        self.llm_client = LlmClient()
        self.result_file = result_file
        self.solution_file_reader = SolutionFileReader(base_dir=base_dir)

    async def execute_async(self):
        if not self.result_file:
            files = await self.solution_file_reader.get_all_files_async()
            print(f"..First pass\n..Found {len(files)} files")
            results = []
            result_store = ResultStore(
                descriptive_suffix=f"{config.LOCAL_LLM_MODEL_NAME}_plan"
                if config.LLM_MODE == "local"
                else f"{config.LLM_MODE}_{config.AZURE_LLM_MODEL_NAME}_plan",
                results_file_extension="json",
            )
            await result_store.add_result_to_store_async(
                '{ "SolutionPath":"' + self.base_dir + '", "Details":[\n'
            )
            cnt = 1
            for file in files:
                print(f"..Reading file: {file}")
                contents = await self.solution_file_reader.read_contents_async(file)

                ## need to chunk here
                content_to_submit = f"Filename: [{file}]\n{contents}"

                print(f"..Querying code in file: {file}")
                if (
                    file.endswith(".md")
                    or file.endswith(".txt")
                    or file.endswith("LICENCE")
                    or file.endswith("LICENSE")
                    or file.endswith(".")
                ):
                    continue

                response = await self.llm_client.query_code_async(
                    prompt_templates.SYSTEM_PROMPTS[prompt_templates.PROMPT_TYPE_PLAN],
                    prompt_templates.USER_PROMPTS[prompt_templates.PROMPT_TYPE_PLAN],
                    content_to_submit,
                    True,
                )
                single_result = f"{',' if cnt != 1 else ''}{response}\n"
                cnt += 1
                await result_store.add_result_to_store_async(single_result)
                results.append(single_result)
            await result_store.add_result_to_store_async("]}")  # close the json object

            print(f"..Results stored in: {result_store.result_file_name}")
            self.result_file = result_store.result_file_name

        summary = CodePlanSummary(self.result_file)
        # summary = CodePlanSummary(
        #     "./_results/results_azure_gpt-4o_plan_2024-11-13-03-14-44.json"
        # )  # debug
        dependencies, changes = await summary.aggregate_dependency_actions()

        summary_store = ResultStore(
            descriptive_suffix=f"{config.LOCAL_LLM_MODEL_NAME}_plansummary"
            if config.LLM_MODE == "local"
            else f"{config.LLM_MODE}_{config.AZURE_LLM_MODEL_NAME}_plansummary",
            results_file_extension="txt",
        )
        await summary_store.add_result_to_store_async(
            f"SolutionPath: [{self.base_dir}]"
        )
        await summary_store.add_result_to_store_async("\nDependencies:")
        for dep in dependencies:
            await summary_store.add_result_to_store_async(f"\t{dep}")

        await summary_store.add_result_to_store_async("\nRecommended changes:")
        for chg in changes:
            await summary_store.add_result_to_store_async(
                f"\t{chg["Dependency"]}: {chg['Action']}"
            )
        print(f"..Final Results stored in: {summary_store.result_file_name}")

        ######TESTING ONLY
        # import aiofiles

        # async with aiofiles.open("./_results/test_results.txt", "r") as f:
        #     first_pass_context = await f.read()
        ######TESTING ONLY

        # response = await self.llm_client.query_code_async(
        #     prompt_templates.SYSTEM_PROMPTS[prompt_templates.PROMPT_TYPE_FINAL_SUMMARY],
        #     prompt_templates.USER_PROMPTS[prompt_templates.PROMPT_TYPE_FINAL_SUMMARY],
        #     first_pass_context,
        #     True,
        # )
        # final_summary = f"---- Final Summary ----\n{response}"
        # await result_store.add_result_to_store_async(final_summary)
        # print(
        #     f"..Updated final summarisation results stored in: {result_store.result_file_name}"
        # )
        await self.llm_client.close()
