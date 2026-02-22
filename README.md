# Query Wizard 3.0

Enterprises struggle with complex, location bound database access and multilingual barriers. So an automated AI-driven platform is required for real-time, natural language interaction with databases accessible anytime, anywhere, by anyone. In database management, many individuals, such as beginners and nontechnical users, often struggle with writing SQL queries. This challenge motivated my team to create Query Wizard to ease writing queries. **Query Wizard 3.0** is an AI-powered Database handling platform that allows users to interact with real-time databases using NLP through text and voice input, from any location on the globe with multilingual support.

![Query Wizard Logo](logo.png)

---

## 🚀 Features

- **Natural Language to SQL**: Convert plain English (or other supported languages) into accurate SQL queries using AI.
- **Voice Input Support**: Speak your queries—ideal for accessibility and hands-free environments.
- **Live SQL Execution**: Run generated queries directly on your **MySQL** database and view results instantly.
- **Schema Preview**: Visualize database tables and column structures for better context.
- **Multi-Language Support**: Interact in various languages, breaking down language barriers in data querying.
- **User Authentication**: Secure login system to manage user access.
- **Modular Architecture**: Easily extendable components for future enhancements.
- **Explanation Box**: View simplified explanations of the generated SQL queries to understand their function.
- **History Audits**: Track and view past queries, responses, and user activity for transparency and learning.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) – Interactive UI for seamless user experience.
- **Backend**:
  - **AI Model**: Google Gemini AI for natural language processing.
  - **Database**: **MySQL** for managing and executing SQL queries.
  - **Voice Recognition**: [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library for converting speech to text.
  - **Language Translation**: [Deep Translator](https://pypi.org/project/deep-translator/) for multi-language support.

---

## 📂 System Architecture
1. High-Level Design
   ![diagram-export-5-12-2025-3_23_46-PM](https://github.com/user-attachments/assets/0a1f1e45-bc77-4a08-9ffa-3dde5a253ffe)

2. Low-Level Design
   ![diagram-export-5-12-2025-5_51_26-PM](https://github.com/user-attachments/assets/597390d0-02df-4151-83ef-973eb337cebe)

---

## 📂 Project Structure

```
Query_Wizard_3.0/
├── __pycache__/              # Compiled bytecode files
├── ai_generator.py           # Handles AI-based SQL generation
├── db_config.py              # Database configuration settings
├── db_handler.py             # Functions for database connections and query execution
├── login.py                  # User authentication logic
├── logo.png                  # Application logo
├── main.py                   # Main application script
├── mysql_schema.json         # Sample MySQL schema for reference
├── prompt.py                 # Prompt templates for AI model
├── query_parser.py           # Parses and validates generated SQL queries
├── requirements.txt          # Python dependencies
├── schema_handler.py         # Manages database schema retrieval and display
└── README.md                 # Project documentation
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Rishivarshney100/Query_Wizard_3.0.git
   cd Query_Wizard_3.0
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   streamlit run main.py
   ```

---

## 🔐 Configuration

- **Database Settings**: Update `db_config.py` with your MySQL credentials and connection details.
- **AI Model API Key**: Ensure you have access to the Google Gemini AI API and set the necessary keys in `ai_generator.py`.
- **Language Support**: Modify `deep_translator` settings in `main.py` to add or change supported languages.

---

## 🧪 Usage

1. **Login**: Start the application and log in with your credentials.
2. **Select Database**: Choose the MySQL database you want to interact with.
3. **Input Query**:
   - **Text**: Type your query in natural language.
   - **Voice**: Click on the microphone icon and speak your query.
4. **Generate SQL**: The AI model will convert your input into an SQL query.
5. **Explanation Box**: Review the simplified explanation of what your SQL query does.
6. **Execute Query**: Run the generated SQL and view the results directly in the app.
7. **History Audits**: Navigate the history section to revisit previous queries and executions.

---

## 🛠️ Future Enhancements

- Support for cloud databases (e.g., PostgreSQL, MongoDB, AWS RDS)
- OAuth 2.0 authentication for enterprise-level security
- Query version control and rollback
- Enhanced data visualization and BI dashboard integrations
- Exportable query logs for enterprise audit compliance

---

## 🚀 UI
![Screenshot 2025-05-12 160303](https://github.com/user-attachments/assets/4a2c7c1c-957c-4374-a7de-8cba7befd8f2)

---

## 🚀 Sample TestCase
![Screenshot 2025-05-12 160648](https://github.com/user-attachments/assets/fd148490-1af0-4662-8d73-6ce7cd162102)
![Screenshot 2025-05-12 160736](https://github.com/user-attachments/assets/599b42bd-b208-4428-989c-7f8a3a60653c)
![Screenshot 2025-05-12 160907](https://github.com/user-attachments/assets/8bee0649-8c22-4477-a478-f6e49439b221)

---

## 👤 Authors

- **Rishi Varshney**  
  [LinkedIn](https://www.linkedin.com/in/rishi-varshney100/) | [LeetCode](https://leetcode.com/u/Rishi_varshney/)  
  Email: rishi.varshney100@gmail.com

- **Tushar Ranjan**  
  [LinkedIn](https://www.linkedin.com/in/tushar-ranjan-4186a8179/) | [LeetCode](https://leetcode.com/u/tushar_ranjan/)  
  Email: tusharranjan151@gmail.com

---

## 📊 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Special thanks to the mentors and contributors at G. L. Bajaj Institute of Technology and Management for supporting this initiative.

---

> 📄 *Query Wizard 3.0 is built to make data interaction as natural as a conversation.*
