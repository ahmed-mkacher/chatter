import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


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

    return f"""User prompt: {content}
Prompt tokens: {result.usage_metadata.prompt_token_count}
Response tokens: {result.usage_metadata.candidates_token_count}"""


def main():
    client = load_api_key()

    parser = argparse.ArgumentParser(description="chatter")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    content = args.user_prompt

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=content)])
    ]

    result = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
    )

    if args.verbose:
        print(verbose(content, result))
    print(f"Response:\n{result.text}")


if __name__ == "__main__":
    main()
