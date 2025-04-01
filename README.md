# Query Wizard

Query Wizard is a Streamlit-based web application that allows users to generate and execute SQL queries using AI, voice input, and a user-friendly interface.

## Features
- **Database Selection**: Users can enter their credentials and select the database they want to use.
- **AI-Powered Query Generation**: Automatically generates SQL queries from natural language prompts.
- **Voice Input**: Users can speak their queries instead of typing.
- **Schema Preview**: Displays table structures and column details.
- **SQL Execution**: Users can run generated queries and view results.

## Installation
### Prerequisites
Ensure you have Python 3.8+ installed.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Tushar00012/Query-Wizard.git
   cd query-wizard
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run main.py
   ```
## Demo Video
[Watch Demo](https://drive.google.com/file/d/1XmURMvdSwhj4Nuz8l5pGDFjM4C_9qTeM/view?usp=sharing)

## Usage
1. Open the application in your browser.
2. Select a database and table.
3. Enter a prompt or use voice input to generate SQL queries.
4. Execute the query and view the results.

## Dependencies
- Streamlit
- SpeechRecognition
- Deep Translator
- Gemini API (for AI-based query generation)
- MySQL

## Contributing
Feel free to fork the repository and submit pull requests for improvements!



