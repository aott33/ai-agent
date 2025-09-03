import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def main():
	try:
		verbose = False

		if len(sys.argv) <= 1:
			print("ERROR: No prompt argument provided")
			sys.exit(1)

		if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
			verbose = True
		
		model_name = 'gemini-2.0-flash-001'
		user_prompt = sys.argv[1]
		
		system_prompt = """
		You are a helpful AI coding agent.

		When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

		- List files and directories
		- Read file contents
		- Execute Python files with optional arguments
		- Write or overwrite files

		All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
		"""

		available_functions = types.Tool(
			function_declarations=[
				schema_get_files_info,
				schema_get_file_content,
				schema_run_python_file,
				schema_write_file,
			]
		)

		messages = [
			types.Content(role="user", parts=[types.Part(text=user_prompt)]),
		]

		load_dotenv()
		api_key = os.environ.get("GEMINI_API_KEY")
		
		client = genai.Client(api_key = api_key)

		for i in range(0,20):
			response = client.models.generate_content(
				model=model_name,
				contents=messages,
				config=types.GenerateContentConfig(
					tools=[available_functions], system_instruction=system_prompt
				),
			)

			prompt_token_count = response.usage_metadata.prompt_token_count
			candidates_token_count = response.usage_metadata.candidates_token_count
			
			for candidate in response.candidates:
				messages.append(candidate.content)

			if response.function_calls:
				for function_call_part in response.function_calls:
					function_call_result = call_function(function_call_part, verbose)

					if not hasattr(function_call_result.parts[0], 'function_response'):
						raise Exception("Function call result does not have expected structure")

					if verbose:
						print(f"-> {function_call_result.parts[0].function_response.response}")
					
					messages.append(types.Content(role="user", parts=[function_call_result.parts[0]]))
			else:
				print('Final Response:')
				print(response.text)
				if verbose:
					print(f"User prompt: {user_prompt}")
					print(f"Prompt tokens: {prompt_token_count}")
					print(f"Response tokens: {candidates_token_count}")
				break

	except Exception as e:
		print(f"Error: {str(e)}")

def call_function(function_call_part, verbose=False):
	if verbose:
		print(f"Calling function: {function_call_part.name}({function_call_part.args})")
	else:
		print(f" - Calling function: {function_call_part.name}")

	function_name = function_call_part.name
	function_args = function_call_part.args.copy()

	function_map = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python_file": run_python_file,
		"write_file": write_file
	}

	if function_name not in function_map:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Unknown function: {function_name}"},
				)
			],
		)
	
	function_args["working_directory"] = "./calculator"

	function_result = function_map[function_name](**function_args)

	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=function_name,
				response={"result": function_result},
			)
		],
	) 

if __name__ == "__main__":
	main()
