import asyncio
from argparse import ArgumentParser

from code_query_engine import CodeQueryEngine
from config import show_config


async def main(solution_path):
    engine = CodeQueryEngine(solution_path)
    results = await engine.execute_async()
    print(results)
    # reader = SolutionFileReader(solution_path)
    # files = await reader.get_all_files()
    # for file in files:
    #     print(f"Reading file: {file}")
    #     contents = await reader.read_contents_async(file)


if __name__ == "__main__":
    parser = ArgumentParser(description="Process solution path")
    parser.add_argument(
        "--solutionpath", type=str, required=True, help="Path to the solution files"
    )
    args = parser.parse_args()
    show_config(args)

    asyncio.run(main(args.solutionpath))
