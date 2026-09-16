# AI Text-to-SQL

AI Text-to-SQL is a Python-based project that demonstrates how natural language can be converted into SQL queries using Artificial Intelligence.

The project uses a sample e-commerce database with synthetic data and is designed to provide the foundation for querying the database using natural language.

## Project Overview

The purpose of this project is to explore how Artificial Intelligence can be used to make database querying easier.

Instead of requiring a user to write SQL manually, the system is intended to accept a natural language question such as:

```text
Show all products with a price greater than 5000.
```

and generate an SQL query based on the e-commerce database structure.

## Current Features

* Python project setup
* E-commerce sample database
* Synthetic e-commerce data generation using Faker
* Environment variable configuration
* OpenAI API configuration
* Database generation script
* Structured project directory for Text-to-SQL development

## Technologies Used

* Python
* GeminiAI API
* Faker
* Python-dotenv
* SQLite

## Project Structure

```text
txt-to-sql/
│
├── data/
│   └── e-commerce database
│
├── scripts/
│   └── generate_database.py
│
├── .env
├── requirements.txt
└── README.md
```

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

Create a `.env` file in the project root directory.

Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual API key.

Do not upload the `.env` file or API key to GitHub.

Add the following to `.gitignore`:

```text
.env
.venv/
__pycache__/
```

## Generate the E-Commerce Database

The project includes a database generation script:

```bash
python scripts/generate_database.py
```

The script uses Faker to generate synthetic e-commerce data for testing and development.

The generated database is stored in the `data/` directory.

## Example Natural Language Queries

The e-commerce database can be queried using questions such as:

```text
Show all products with a price greater than 5000.
```

```text
Show the top 10 most expensive products.
```

```text
How many customers are registered in the database?
```

```text
Show all orders placed by a specific customer.
```

```text
What is the total sales amount?
```

These questions are intended to be converted into SQL queries by the Text-to-SQL system.

## Project Objective

The objective of this project is to develop an AI-based Text-to-SQL system that understands natural language questions and converts them into SQL queries for an e-commerce database.

The project is being developed step by step, beginning with the creation of the e-commerce database and synthetic data.

## Future Development

The project can be extended to include:

* Natural language to SQL query generation
* OpenAI API integration
* E-commerce database schema understanding
* SQL query execution
* Query result display
* SQL query validation
* Query history
* Web-based user interface
* Support for additional database systems

## Author

**Sara Fazal**

GitHub: [SaraFazal-2004](https://github.com/SaraFazal-2004)

## License

This project is intended for educational and learning purposes.
