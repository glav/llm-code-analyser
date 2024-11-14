# LLM Code Analyser
An experiment to see how effective an LLM can be in helping to classify and potentially migrate applications to a new platform.

This codebase is primarily targetting non PaaS or cloud hosted models to remove any security concerns of an organisations code (which may contains various secrets or IP) being shared with a public cloud hosted service.
This solution assumes you are using [Ollama](https://ollama.com/) and you have at least 1 model downloaded and able to run. Most of the testing has been performed using Llama3.1 model but it has not been comprehensively tested.

## Table of contents
- [LLM Code Analyser](#llm-code-analyser)
  - [Table of contents](#table-of-contents)
- [Pre-requisites](#pre-requisites)
  - [Ensuring Ollama is accessible](#ensuring-ollama-is-accessible)
    - [Configuring the solution](#configuring-the-solution)
    - [Running inside a devcontainer](#running-inside-a-devcontainer)
- [Running the code](#running-the-code)

# Pre-requisites
1. [Ollama](https://ollama.com/) installed and at least one model like 'Llama3.1' downloaded. Executing 
![Ollama list](./images/ollama-list.png)
2. VSCode installed with Python extension
  - However this is not strictly true, but all development has been performed within the devcontainer so many assumptions are already taken care of.
3. A solution to analyse. You can use the source code of this app or you can try something like [replatform-java-webapp-on-aws](https://github.com/aws-samples/replatform-java-webapp-on-aws) from the AWS Samples GitHub repository.
4. If you want to use cloud hosted models, you need to have deployed an Azure OpenAI model like gpt-4o (the default)

## Ensuring Ollama is accessible
Ollama can be typically accessed via http://localhost:11434 (default - but can be changed - see Ollama documentation). 

To ensure the Ollama is in fact accessible via HTTP, you can execute:
```bash
curl http://localhost:11434
```
If it is running, you should receive:
```
Ollama is running
```
*Note:* If you are executing the command from within the devcontainer, you may need to use the `host.docker.internal` hostname to access the Ollama service running on the host machine. For example:
```bash
curl http://host.docker.internal:11434
```
### Configuring the solution
Set the .env file within the `app` directory with the correct configuration values, use the `.env-sample` as a template. 
```
LOCAL_LLM_MODEL_NAME = "llama3.1"
LLM_MODE = "local"  # or 'azure'

# if using azure
AZURE_OPENAI_API_KEY = "<your-azure-openai-key"
AZURE_OPENAI_ENDPOINT = "https://{name}.openai.azure.com"
AZURE_API_VERSION = "2024-02-15-preview"
AZURE_LLM_MODEL_NAME = "gpt-4o"
AZURE_STORAGE_CONNECTION_STRING="<your-storage-acct-connection-string>"  # Only required if you are performing an image analysis using cloud models

```
### Running inside a devcontainer
For the solution to work inside a devcontainer, there is a configuration element in the `.devcontainer/devcontainer.json` file that sets the `OLLAMA_HOST` environment variable. This is used by the code to connect to the Ollama service on `localhost:11434`. If you are using a different host or port, you will need to update this value.
```
"containerEnv": {
    	"OLLAMA_HOST": "host.docker.internal:11434" // OLLAMA_HOST is the hostname of the OLLAMA server - this is to enable use of ollama package inside devcontainer
	},
```

# Running the code
There are multiple options to choose from, all of which do somewhat different functions but you cannot use all at once. Only the `--ref-image-path` and `--target-image-path` can be used together.
The usage is:
```python
cd app
python app.py {options{...}}
```
where options can be: 
- `--solution-path SOLUTION_PATH`: Path to the solution files
- `--ref-image-path REF_IMAGE_PATH`: The reference architecture image to compare with
- `--target-image-path TARGET_IMAGE_PATH`: The target architecture image to compare against the reference architecture image
- `--solution-plan-path SOLUTION_PLAN_PATH`: Path to the solution files for which to create a migration plan
- `--solution-plan-path-result-file SOLUTION_PLAN_PATH_RESULT_FILE`: Path to the result file from the `--solution-plan-path` argument from which to process, by passing the generation of the result file and simply creating the plan summary from.
- `--solution-app-env-extract-path SOLUTION_APP_ENV_EXTRACT_PATH`: Path to the solution files for which to extract the environment information.


To run the analysis on a solution (prefer Java or python), execute the following:
```bash
cd app
python app.py --solutionpath SOLUTIONPATH
```
or
```
python app.py --ref-image-path REF_IMAGE_PATH --target-image-path TARGET_IMAGE_PATH
```
Where:
- `SOLUTIONPATH` is the path to the solution you want to analyse. For example:
```bash
python app.py --solutionpath ..
```
and
- `ref-image-path`: The reference architecture image to compare with
- `target-image-path`: The target architecture image to compare against the reference architecture image
This will analyse the solution in the parent directory of the app directory for this solution.
```bash
python app.py --ref-image-path ../.local/ref_arch.png --target-image-path ../.local/test_arch.png
```

**Important Note:** If you are not using a device with a suitable GPU, this process can take quite some time and consume a lot of CPU.

