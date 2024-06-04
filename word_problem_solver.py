import requests
import json

# Define the URL to post the JSON data to, here we are calling the koboldcpp api hosted locally
url = "http://localhost:5001/api/v1/generate"

# Llama 3 expects this tag before the user's prompt
llama3_opening_prompt = "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
# Llama 3 expects this tag after the user's prompt
llama3_closing_prompt = "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

# Function to create the JSON payload for the koboldcpp API (https://lite.koboldai.net/koboldcpp_api)
def create_json_payload (custom_max_length, custom_prompt, grammar):
    json_payload = {
        "max_context_length": 512,
        "max_length": custom_max_length,
        "prompt": custom_prompt,
        "rep_pen": 1.07,
        "rep_pen_range": 256,
        "temperature": 0.1,
        "grammar": grammar,
        "grammar_retrain_state": "false",
        "tfs": 1,
        "top_a": 0,
        "top_k": 100,
        "top_p": 1,
        "typical": 1
    }
    return json_payload

# Function to send the JSON to the API, and recieve the response
def send_and_recieve_json(post_this_json):
    # Send the POST request with the JSON data to koboldcpp API
    send_kobold_data = requests.post(url, json=post_this_json)
    # Check if request was successful
    try:
        send_kobold_data.status_code == 200
        # Get the JSON response
        json_response = send_kobold_data.json()
        # Extract the answer from the JSON response
        text_response = json_response["results"][0]["text"]
        return text_response
    # Return error code if request is not successful
    except Exception as e:
        return(f"Koboldcpp did not return a response, posted error code: {e}")

# Function to convert the word problem to an expression using the LLM
def convert_word_problem_to_expression(word_problem):
    # Prompt to LLM to convert word problem to expression
    # The prompt contains an example of how to change a word problem to an expression
    # It's a 1-shot prompt, a larger n-shot prompt might deliver better results. 
    expression_prompt = (llama3_opening_prompt + 
    'Write the following word problem as an expression: '+
    '"Gage went shopping and bought 9 cupcakes and 7 glazed donuts. How many items did he buy altogether?"' + 
    llama3_closing_prompt + 
    '9+7' + 
    llama3_opening_prompt + 
    'Write the following word problem as an expression: ' + 
    word_problem + 
    llama3_closing_prompt)
    # Defining pattern for LLM to return using GBNF grammar 
    # (https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md). 
    # We want it to only return a number one more times, followed by an operator, followed by a number one or more times. 
    # In the next step we only generate 3 tokens, and numbers larger than 999 count as more than one token in Llama 3 models. 
    # Thus, the answer will follow the pattern of [0-999][-+*/][0-999]. 
    # Will look at expanding this to larger numbers and more operators in future versions of this code.
    expression_output_grammar = ('root  ::= [0-9]*[-+*/][0-9]*\n')
    # Define the JSON data to be posted
    expression_json = create_json_payload(3,expression_prompt,expression_output_grammar)
    # Send the JSON to the API and recieve the response
    expression_response = (send_and_recieve_json(expression_json))

    return expression_response

# Function to retrieve the unit from the problem using the LLM
def retrieve_unit_from_problem(word_problem,answer):
    # Prompt to have LLM return the correct unit from the original word problem
    # The prompt contains an example of how to get the unit from the original question
    # Because we are feeding the model the answer from the earlier eval in the prompt, it just returns the unit
    unit_prompt = (llama3_opening_prompt + 
    'Express the correct answer and unit for the following word problem:' +
    'Gage went shopping and bought 9 cupcakes and 7 glazed donuts. How many items did he buy altogether?"' + 
    llama3_closing_prompt + 
    '16 items' + 
    llama3_opening_prompt + 
    'Express the correct answer and unit for the following word problem:' + 
    word_problem + 
    llama3_closing_prompt + 
    str(answer))
    # Create the JSON payload with the prompt to get the unit
    unit_json = create_json_payload(7,unit_prompt,"")
    # Send the JSON to the API and recieve the response
    unit_response = send_and_recieve_json(unit_json)

    return unit_response
    

def solve_word_problem (word_problem):
    # Convert the word problem to an expression
    expression = convert_word_problem_to_expression(word_problem)

    # Evaluate the mathematical expression
    try:
        answer = eval(expression)
    except Exception as e:
        return(f"Error evaluating expression: {e}")

    # Retrieve the correct unit from the original problem
    unit = retrieve_unit_from_problem(word_problem,answer)
    # Return final answer, combining the numerical answer with the unit
    return("\033[1m" + str(answer) + unit + "\033[0m")


def main():
    input_problem = input("Please input a word problem:\n")
    final_answer = (solve_word_problem(input_problem))
    print(final_answer)

if __name__ == "__main__":
    main()
