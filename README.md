# LLM Code Analyser
An experiment to see how effective an LLM can be in helping to classify and potentially migrate applications to a new platform.

This codebase is primarily targetting non PaaS or cloud hosted models to remove any security concerns of an organisations code (which may contains various secrets or IP) being shared with a public cloud hosted service.
This solution assumes you are using [Ollama](https://ollama.com/) and you have at least 1 model downloaded and able to run. Most of the testing has been performed using Llama3.1 model but it has not been comprehensively tested.

## Table of contents
- [LLM Code Analyser](#llm-code-analyser)
  - [Table of contents](#table-of-contents)
- [Pre-requisites](#pre-requisites)
  - [Ensuring Ollama is accessible](#ensuring-ollama-is-accessible)
- [Running the code](#running-the-code)

# Pre-requisites
1. [Ollama](https://ollama.com/) installed and at least one model like 'Llama3.1' downloaded. Executing 
![Ollama list](./images/ollama-list.png)
2. VSCode installed with Python extension
  - However this is not strictly true, but all development has been performed within the devcontainer so many assumptions are already taken care of.

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

# Running the code
To run the analysis on a solution (prefer Java or python), execute the following:
```bash
cd app
python app.py --solutionpath SOLUTIONPATH
```
Where `SOLUTIONPATH` is the path to the solution you want to analyse. For example:
```bash
python app.py --solutionpath ..
```
This will analyse the solution in the parent directory of the app directory for this solution.
