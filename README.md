# AI Text-to-SQL

An AI-powered application that converts natural language questions into SQL queries. The project allows users to interact with a database using simple English instructions instead of writing SQL manually.

## Project Overview

AI Text-to-SQL is designed to make database querying easier by translating natural language input into SQL statements using Artificial Intelligence.

For example, instead of writing:

```sql
SELECT * FROM employees WHERE salary > 50000;
```

A user can simply ask:

> Show all employees with a salary greater than 50,000.

The application processes the user's request and generates the appropriate SQL query.

## Features

* Convert natural language text into SQL queries
* AI-powered SQL generation
* Connect with a database
* Execute generated SQL queries
* Display query results
* Support for common SQL operations such as:

  * SELECT
  * WHERE
  * ORDER BY
  * GROUP BY
  * JOIN
  * COUNT
  * SUM
  * AVG
* Environment variable support for API keys
* Sample database generation for testing

## Technologies Used

* Python
* OpenAI API
* SQL / SQLite
* Faker
* Python-dotenv

## Project Structure

```text
txt-to-sql/
│
├── data/
│   └── database files and sample data
│
├── scripts/
│   └── generate_database.py
│
├── .env
├── requirements.txt
├── README.md
└── main.py
```

> Note: The project structure may change as additional features are developed.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SaraFazal-2004/ai-text-to-sql.git
```

### 2. Navigate to the Project Folder

```bash
cd ai-text-to-sql
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install Required Packages

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a file named `.env` in the project root directory.

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.

**Important:** Never upload your `.env` file or API key to GitHub.

You should add the following to your `.gitignore` file:

```text
.env
.venv/
__pycache__/
```

## Generate the Sample Database

Run the database generation script:

```bash
python scripts/generate_database.py
```

This will create and populate a sample database that can be used to test natural language queries.

## Example Usage

A user can enter a question such as:

```text
Show all customers from Islamabad.
```

The AI may generate:

```sql
SELECT *
FROM customers
WHERE city = 'Islamabad';
```

Another example:

```text
Show the top 5 highest-paid employees.
```

Generated SQL:

```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 5;
```

## Security Considerations

Generated SQL should be validated before execution, especially when working with production databases.

Recommended practices include:

* Use read-only database access where possible.
* Restrict dangerous SQL commands such as:

  * DROP
  * DELETE
  * UPDATE
  * ALTER
* Validate AI-generated SQL before execution.
* Never expose API keys in source code.
* Use environment variables to store sensitive credentials.

## Project Goal

The goal of this project is to demonstrate how Artificial Intelligence and Large Language Models can simplify database interaction by allowing users to communicate with databases using natural language.

This project can be further expanded to support:

* Multiple database systems
* SQL Server
* MySQL
* PostgreSQL
* SQLite
* Web-based user interface
* Chat-based database interaction
* Query history
* Database schema visualization
* SQL query explanation
* Role-based database access

## Future Improvements

*  Support SQL Server
*  Support multiple databases
*  Add database schema detection
*  Validate generated SQL
*  Add SQL query explanations
*  Add query history
*  Improve error handling
*  Add automated tests

## Author

**Sara Fazal**

GitHub: [SaraFazal-2004](https://github.com/SaraFazal-2004?utm_source=chatgpt.com)

## License

This project is currently intended for educational and learning purposes.

---

If you find this project useful, consider giving the repository a star.
