import boto3
import json
import zipfile
import argparse
import os


def analyze_code_with_claude(zip_path=None, code_snippet=None, analyze_dependencies=False, explain_logic=False):
    # Create a Bedrock Runtime client
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

    # Set the model ID for Claude 3 Sonnet
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    # Extract the contents of the zip file if provided
    zip_contents = {}
    if zip_path:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                with zip_ref.open(file_name) as file:
                    zip_contents[file_name] = file.read()

    # Prepare the prompt
    prompt = "Here's the contents of a zip file containing source code:\n\n"
    if zip_contents:
        for file_name, content in zip_contents.items():
            prompt += f"File: {file_name}\n```\n{content}\n```\n\n"

    if code_snippet:
        prompt += f"Code Snippet:\n```\n{code_snippet}\n```\n\n"

    if analyze_dependencies:
        prompt += "Please analyze the class dependencies in the provided code.\n"

    if explain_logic:
        prompt += "Please explain the logic behind this code.\n"

    prompt += "Please analyze this code and provide a summary of its functionality."
    print(prompt)
    # Prepare the request payload
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }

    try:
        '''Invoke the model
        # response = bedrock_runtime.invoke_model(
        #         #     modelId=model_id,
        #         #     contentType='application/json',
        #         #     accept='application/json',
        #         #     body=json.dumps(request_body)
        #         # )

        # Parse the response
        # response_body = json.loads(response['body'].read())
        # generated_text = response_body['content'][0]['text']
        #
       ''' # return generated_text
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Analyze source code using Claude 3 via AWS Bedrock")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-s", "--zip_file", help="Path to the zip file containing source code")
    group.add_argument("-c", "--code_snippet", help="Code snippet to analyze")

    parser.add_argument("-d", "--analyze_dependencies", action='store_true',
                        help="Analyze class dependencies in the code")
    parser.add_argument("-e", "--explain", action='store_true', help="Explain the logic behind the code")

    args = parser.parse_args()

    # Check if the provided zip file exists
    if args.zip_file and not os.path.exists(args.zip_file):
        print(f"Error: The file '{args.zip_file}' does not exist.")
        return

    print("Analyzing code...")
    analysis = analyze_code_with_claude(args.zip_file, args.code_snippet, args.analyze_dependencies, args.explain)
    print("\nAnalysis Result:")
    print(analysis)


if __name__ == "__main__":
    main()