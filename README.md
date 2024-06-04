# Llama 3 Word Problem Solver

Llama 3 Word Problem Solver is a natural language math solver that:

- Uses Llama 3 via the koboldcpp api to parse an expression from a word problem
- Solves that expression
- Returns the final answer with the units


This program was written to leverage LLMs to parse word problems, but to leave the calculation part to functions that can do math without "hallucinations".

It is currently limited to single-operator (addition, subtraction, multiplication, division) expressions with operands ranging from 0-999. It may struggle to return the correct units with division problems in some cases.

## Installation

You'll need Python 3.11, pip, koboldcpp, and the llama3 weights in GGUF format, and the code in this repo.

First, clone the repository and install the needed packages:
- `git clone https://github.com/joelewing/llama3-word-problem-solver`
- `cd llama3-word-problem-solver`
- `pip install requirements.txt`

Second, install koboldcpp from [LostRuins/koboldcpp](https://github.com/LostRuins/koboldcpp): 
- Select the executable for your platform
- Run the executable

You will be greeted with an options window. Refer to the [documentation on the koboldcpp repo](https://github.com/LostRuins/koboldcpp/wiki) to know if you should change any of the options.

One of these options is to select a model file. The model will need to be in the GGUF format. 

Models that use the [Llama 3 Instruct prompt format](https://llama.meta.com/docs/model-cards-and-prompt-formats/meta-llama-3/) should generally be compatible with the prompts in this program, but Meta Llama 3 Instruct 70B is recommended for best results. 

You can grab the GGUF file here: [https://huggingface.co/bartowski/Meta-Llama-3-70B-Instruct-GGUF/tree/main](https://huggingface.co/bartowski/Meta-Llama-3-70B-Instruct-GGUF/tree/main). 

I used the [Q3_K_S](https://huggingface.co/bartowski/Meta-Llama-3-70B-Instruct-GGUF/blob/main/Meta-Llama-3-70B-Instruct-Q3_K_S.gguf) quant during my testing. 

Alternatively, if you do not have the RAM / VRAM capacity to run that model, a quant of the less capable Meta Llama 3 8B Instruct is also a good option.

After koboldcpp has been launched, and the model has loaded into your system's RAM / VRAM, you should have a koboldcpp server listening on [http://localhost:5001](http://localhost:5001)

## Usage

At this point, you are ready to run the program.
- `python word_problem_solver.py`

Give it a simple word problem and watch it solve!



