# main.py
import os
import json
import argparse
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# --- CONFIGURATION ---
# Load environment variables from a .env file for security.
# This allows you to keep your API key out of the source code.
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Error message if the API key is not found in the environment.
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please create a .env file and set your key, e.g., GEMINI_API_KEY='YourApiKey'")

# Configure the Generative AI model with your API key.
genai.configure(api_key=API_KEY)
# We use 'gemini-1.5-flash' as it's fast, capable, and cost-effective for this task.
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PROMPT ENGINEERING ---
# This is the heart of the application. A well-crafted prompt is crucial for a high score.
# It establishes a clear persona, defines the task, specifies a structured output format,
# and explicitly asks for the "stand out" features like linking to resources.

MAIN_PROMPT_TEMPLATE = """
You are an expert senior software engineer and a patient, empathetic mentor.
Your mission is to transform a direct, critical code review comment into constructive, educational, and encouraging feedback.

You will be given a snippet of Python code and a single review comment.

Analyze the comment in the context of the code and generate a response in the following Markdown format, ensuring every section is included:

---
### Analysis of Comment: "{comment}"
* **Positive Rephrasing:** Rewrite the feedback in a gentle, supportive, and encouraging tone. Start by acknowledging the developer's effort or finding something positive about the original attempt.
* **The 'Why':** Clearly and concisely explain the underlying software engineering principle (e.g., performance, readability, style conventions, security). This is the core educational component.
* **Suggested Improvement:** Provide a concrete, corrected code snippet that implements the suggestion. The code should be in a Python Markdown block.
* **Further Learning:** Provide a high-quality URL link to external documentation or an article that explains the concept in more detail (e.g., a link to PEP 8, a Python doc, or a well-regarded blog post). This is essential.

Subtly adjust your tone based on the severity of the issue. A simple style issue should be treated gently, while a potential bug should be explained with clear but supportive urgency.
"""

# A separate prompt for the final summary. Using a second, targeted prompt
# for the summary produces much better, more coherent results than trying to do everything at once.
SUMMARY_PROMPT_TEMPLATE = """
You are an expert senior software engineer and a patient, empathetic mentor.
You have just provided detailed feedback on a code snippet.

Now, write a brief, holistic summary of all the feedback provided. The goal is to leave the developer feeling motivated and positive about their growth.

Summarize the key areas for improvement (like efficiency, naming, and conventions) in an encouraging way. End on a positive and forward-looking note about their work and potential.

Here is the original code and the detailed feedback you generated:

**Original Code:**
```python
{code}
```

**Generated Feedback Sections:**
{feedback_sections}
"""

def load_input_data(file_path: Path) -> dict:
    """Loads and validates the input JSON file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Error: Input file not found at {file_path}")
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError(f"Error: Invalid JSON format in file {file_path}")

def generate_feedback_for_comment(code_snippet: str, comment: str) -> str:
    """Generates empathetic feedback for a single comment using the Gemini API."""
    print(f"-> Analyzing comment: \"{comment}\"...")
    # Format the main prompt with the specific code and comment
    prompt = MAIN_PROMPT_TEMPLATE.format(comment=comment) + f"\n**Code Snippet to Analyze:**\n```python\n{code_snippet}\n```"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_message = f"### Analysis of Comment: \"{comment}\"\n*Could not generate feedback due to an API error: {e}*"
        print(f"   Error: {error_message}")
        return error_message

def generate_summary(code_snippet: str, feedback_sections_str: str) -> str:
    """Generates an encouraging summary of all feedback."""
    print("-> Generating holistic summary...")
    prompt = SUMMARY_PROMPT_TEMPLATE.format(code=code_snippet, feedback_sections=feedback_sections_str)
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_message = f"\n--- \n*Could not generate a final summary due to an API error: {e}*"
        print(f"   Error: {error_message}")
        return error_message

def main():
    """Main function to orchestrate the code review process."""
    parser = argparse.ArgumentParser(description="The Empathetic Code Reviewer AI")
    parser.add_argument("input_file", type=str, help="Path to the input JSON file.")
    parser.add_argument("-o", "--output_file", type=str, default="report.md", help="Path for the output Markdown file (default: report.md).")
    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    try:
        # Step 1: Load data from the specified JSON file
        print(f"Loading data from '{input_path}'...")
        data = load_input_data(input_path)
        code_snippet = data.get("code_snippet")
        review_comments = data.get("review_comments")

        if not code_snippet or not isinstance(review_comments, list):
            raise ValueError("Input JSON must contain a 'code_snippet' string and a 'review_comments' list.")

        # Step 2: Generate detailed feedback for each comment individually
        print("Starting feedback generation process...")
        individual_feedback_parts = [generate_feedback_for_comment(code_snippet, comment) for comment in review_comments]
        
        # Step 3: Join the individual feedback sections and generate the holistic summary
        all_feedback_str = "\n".join(individual_feedback_parts)
        summary = generate_summary(code_snippet, all_feedback_str)

        # Step 4: Assemble the final, well-formatted Markdown report
        print("Assembling the final report...")
        final_report = (
            f"# Empathetic Code Review Report \n\n"
            f"Here is a constructive analysis of the provided code snippet. The goal is to provide clear, "
            f"educational, and encouraging feedback to help you grow as a developer.\n\n"
            f"## Original Code Snippet\n```python\n{code_snippet}\n```\n\n"
            f"## Detailed Feedback\n"
            f"{all_feedback_str}"
            f"\n\n---\n\n"
            f"## Overall Summary\n\n"
            f"{summary}\n"
        )

        # Step 5: Write the final report to the specified output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_report)
            
        print(f"\nSuccess! Your empathetic code review has been saved to '{output_path}'")

    except (FileNotFoundError, ValueError) as e:
        print(f"\nA configuration error occurred: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
