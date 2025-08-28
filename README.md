# Hackathon Mission 1: The Empathetic Code Reviewer

This project is a solution for the "The Empathetic Code Reviewer" hackathon mission. It uses Google's Gemini AI to transform blunt, critical code review comments into supportive, constructive, and educational feedback, aiming to foster a positive growth environment for developers.

---

## 🚀 Features

This solution meets all the core requirements and implements all suggested "Stand Out" features to maximize the score.

* **Empathetic Rephrasing:** Converts terse feedback into positive, encouraging guidance.
* **Educational Explanations:** Clearly explains the "why" behind each suggestion, referencing core software engineering principles.
* **Actionable Code Suggestions:** Provides corrected code snippets for easy implementation.
* **🏆 [Stand Out] Contextual Awareness:** The AI's prompt encourages it to adjust its tone based on the severity of the feedback.
* **🏆 [Stand Out] Links to External Resources:** Each piece of feedback includes a link to high-quality documentation (e.g., PEP 8, official docs) for further learning.
* **🏆 [Stand Out] Holistic Summary:** After analyzing all comments, the program makes a second AI call to generate a final, encouraging summary to motivate the developer.
* **Robust & Clean Code:** The Python script is well-structured, commented, and includes error handling.
* **Secure API Key Handling:** Uses `.env` files for API key management, avoiding hardcoded secrets.

---

## 🛠️ Setup & Installation

Follow these steps to get the project running.

### 1. Prerequisites

* Python 3.8+
* A Google Gemini API Key. (You can get a free one from [Google AI Studio](https://aistudio.google.com/app/apikey)).

### 2. Clone the Repository

Clone the project from your GitHub repository.

```bash
git clone [https://github.com/nirbhay002/hackathon_mission_1.git](https://github.com/nirbhay002/hackathon_mission_1.git)
cd your-repo-name
```

### 3. Set Up a Virtual Environment

It's a best practice to use a virtual environment to manage dependencies.

**For Unix/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Install the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Configure Your API Key (Important!)

This application requires a Google Gemini API key to function. The project is configured to load this key securely from an environment file, which you must create.

1.  In the root of the project directory, create a new file named `.env`.
2.  Open the `.env` file and add your API key in the following format:

    ```
    # .env file
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```
3.  Replace `YOUR_GEMINI_API_KEY_HERE` with your actual, valid Gemini API Key. The `.gitignore` file is already configured to prevent this file from being committed to the repository.

---

## ▶️ How to Run

Once the setup is complete, you can run the program from your terminal.

1.  Make sure you are in the root directory of the project and your virtual environment is activated.
2.  The script requires one argument: the path to the input JSON file.

**Example Command:**
```bash
python main.py input.json
```

The script will print its progress to the console and, upon completion, will generate a Markdown report.

By default, the output is saved to `report.md`. You can specify a different output file name using the `-o` or `--output_file` flag:

```bash
python main.py input.json -o my_custom_report.md
