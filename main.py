import argparse
import os
import pprint

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def load_api_key():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable value is not set. Check issue and try again"
        )

    return genai.Client(api_key=api_key)


def verbose(content, result):
    if not result.usage_metadata:
        raise RuntimeError(
            "No usage metadata found in the response. API request most likely failed, try again."
        )

    return f"""User prompt: {content}\nPrompt tokens: {result.usage_metadata.prompt_token_count}\nResponse tokens: {result.usage_metadata.candidates_token_count}"""


def generate(client, config, messages, args):
    result = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
        config=config,
    )

    if result.candidates:
        map(lambda candidate: messages.append(candidate.content), result.candidates)

    if result.function_calls:
        verbosity = False
        function_call_result = types.Content()

        if args.verbose:
            verbosity = True

        for call in result.function_calls:
            function_call_result = call_function(call, verbosity)

        if not function_call_result.parts:
            raise Exception("Parts array is empty.")

        if not function_call_result.parts[0].function_response:
            raise Exception("No function response was returned.")

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Response is empty")

        messages.append(types.Content(role="user", parts=function_call_result.parts))
        pprint.pprint(f"-> {function_call_result.parts[0].function_response.response}")

    return result

def main():
    client = load_api_key()
    result = types.GenerateContentResponse()
    parser = argparse.ArgumentParser(description="chatter")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    content: str = args.user_prompt

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=content)])
    ]

    for _ in range(20):
        result = generate(client, config, messages, args)
        if result.text:
            break

    if not result.text:
        exit("Loop did not end.")

    if args.verbose:
        print(verbose(content, result))

    print(f"Response:\n{result.text}")


if __name__ == "__main__":
    main()
