import prompt_templates
from ollama_client import OllamaClient
from solution_file_reader import SolutionFileReader


class CodeQueryEngine:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self.ollama_client = OllamaClient()
        self.solution_file_reader = SolutionFileReader(base_dir=base_dir)

    async def execute_async(self) -> list:
        files = await self.solution_file_reader.get_all_files_async()
        print(f"..Found {len(files)} files")
        results = []
        for file in files:
            print(f"..Reading file: {file}")
            contents = await self.solution_file_reader.read_contents_async(file)

            ## need to chunk here

            print(f"..Querying code in file: {file}")
            # use a different prompt for code and markdown files
            prompt_type = "code"
            if file.endswith(".md") or file.endswith(".txt"):
                prompt_type = "markdown"

            response = await self.ollama_client.query_code_async(
                prompt_templates.SYSTEM_PROMPTS[prompt_type],
                prompt_templates.USER_PROMPTS[prompt_type],
                contents,
            )
            results.append(response["message"]["content"])
        return results
