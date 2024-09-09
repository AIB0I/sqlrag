# sqlrag

sqlrag helps users to query SQL databases using natural language. It leverages LLM and embeddings to interpret user queries and generate appropriate SQL statements.

## Features

- Natural language interface for SQL queries
- Returns both query results and the generated SQL statement
- Supports SQLite database and CSV files
- Uses Ollama for language model and embeddings

*Note: This project is currently under development.*

## Setup and Running

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sqlrag.git
   cd sqlrag
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure `.env` file:
   ```
   DB_TYPE = <sqlite or csv>
   DB_CONNECTION = <path_to_sqlite_db_or_csv_file>
   LLM_MODEL = <ollama_model_name>
   EMBEDDING_MODEL = <ollama_embedding_model_name>
   ```

4. Run the script:
   ```
   python sqlrag.py
   ```

## Install Ollama

You can follow the instructions on the [Ollama](https://github.com/ollama/ollama) GitHub repository to install and run Ollama on your system.

## Sample Data

Sample data for both SQLite and CSV is available in the `sample_data` folder.

## TODO

- [x] Add support for SQLite database
- [x] Add support for CSV file
- [ ] Add support for PostgreSQL database
- [ ] Add support for MySQL database
- [ ] Implement basic web interface
- [ ] Integrate basic data visualization
- [ ] Add query history tracking
- [ ] Add basic authentication
- [ ] Data validation for CSV files
- [ ] Multiple CSV files support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.