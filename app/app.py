import asyncio
from argparse import ArgumentParser

from app_env_extract_engine import AppEnvExtractEngine
from code_plan_engine import CodePlanEngine
from code_query_engine import CodeQueryEngine
from config import show_config
from image_comparison_engine import ImageComparisonEngine


async def main(args):
    if args.solution_path:
        engine = CodeQueryEngine(args.solution_path)
        await engine.execute_async()
    elif args.solution_plan_path or args.solution_plan_path_result_file:
        engine = CodePlanEngine(
            args.solution_plan_path, args.solution_plan_path_result_file
        )
        await engine.execute_async()
    elif args.solution_app_env_extract_path:
        engine = AppEnvExtractEngine(args.solution_app_env_extract_path)
        await engine.execute_async()
    else:
        engine = ImageComparisonEngine(args.ref_image_path, args.target_image_path)
        await engine.execute_async()


if __name__ == "__main__":
    parser = ArgumentParser(description="Process solution path")
    parser.add_argument(
        "--solution-path", type=str, required=False, help="Path to the solution files"
    )
    parser.add_argument(
        "--ref-image-path",
        type=str,
        required=False,
        help="The reference architecture image to compare with",
    )
    parser.add_argument(
        "--target-image-path",
        type=str,
        required=False,
        help="The target architecture image to compare against the reference architecture image",
    )

    parser.add_argument(
        "--solution-plan-path",
        type=str,
        required=False,
        help="Path to the solution files for which to create a migration plan",
    )

    parser.add_argument(
        "--solution-plan-path-result-file",
        type=str,
        required=False,
        help="Path to the result file from the -solution-plan-path argument from which to process, by passing the generation of the result file and simply creating the plan summary from.",
    )

    parser.add_argument(
        "--solution-app-env-extract-path",
        type=str,
        required=False,
        help="Path to the solution files for which to extract the environment information",
    )

    args = parser.parse_args()
    if (
        not args.solution_path
        and not args.solution_plan_path
        and not args.solution_plan_path_result_file
        and not args.solution_app_env_extract_path
        and not (args.ref_image_path and args.target_image_path)
    ):
        parser.print_help()
        exit(1)
    if (
        args.solution_path
        or args.solution_plan_path
        and (args.ref_image_path or args.target_image_path)
    ):
        parser.print_help()
        exit(1)

    show_config(args)

    asyncio.run(main(args))
