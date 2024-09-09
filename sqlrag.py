import os
import sqlite3
import logging
from dotenv import load_dotenv
from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import pandas as pd

# Get configurations from environment variables
DB_TYPE = None
DB_CONNECTION = None
LLM_MODEL = None
EMBEDDING_MODEL = None

# Set up logging to write to both app.log file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def csv_to_sqlite(csv_file, sqlite_file):
    logger.info(f"Converting CSV file '{csv_file}' to SQLite database '{sqlite_file}'")
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(sqlite_file)
    df.to_sql('csv_data', conn, if_exists='replace', index=False)
    conn.close()

def get_sql_database():
    logger.info(f"Getting SQL database for type: {DB_TYPE}")
    if DB_TYPE == 'sqlite':
        db_url = f"sqlite:///{DB_CONNECTION}"
    elif DB_TYPE == 'csv':
        sqlite_file = 'temp_csv_database.db'
        csv_to_sqlite(DB_CONNECTION, sqlite_file)
        db_url = f"sqlite:///{sqlite_file}"
    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}")
    
    return SQLDatabase.from_uri(db_url)

def initialize_engine():
    # Load environment variables
    load_dotenv(".env", override=True)

    global DB_TYPE, DB_CONNECTION, LLM_MODEL, EMBEDDING_MODEL
    DB_TYPE = os.getenv("DB_TYPE")
    DB_CONNECTION = os.getenv("DB_CONNECTION")
    LLM_MODEL = os.getenv("LLM_MODEL")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

    # Get the SQL database
    sql_database = get_sql_database()

    # Get table names automatically
    tables = sql_database.get_usable_table_names()

    # Set up Ollama LLM
    llm = Ollama(model=LLM_MODEL)

    # Set up embedding model
    embed_model = OllamaEmbedding(model_name=EMBEDDING_MODEL)

    # Update global settings
    Settings.llm = llm
    Settings.embed_model = embed_model

    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=tables, llm=llm
    )

    return sql_database, tables, query_engine

# Function to handle user queries
def process_query(sql_database, query_engine, user_query):
    logger.info(f"Processing query: {user_query}")
    response = query_engine.query(user_query)
    
    # Extract the SQL query
    sql_query = response.metadata['sql_query']
    
    # Execute the SQL query and get the results as a pandas DataFrame
    df = pd.read_sql_query(sql_query, sql_database.engine)
    
    return {
        'answer': str(response),
        'sql_query': sql_query,
        'data': df
    }

def main():

    # Get the SQL database
    sql_database, tables, query_engine = initialize_engine()

    logger.info("Starting sqlrag Query System")
    welcome_message = """
    ╔═════════════════════════════════════════════════╗
    ║                                                 ║
    ║   Welcome to the sqlrag Query System!           ║
    ║                                                 ║
    ║   Enter your queries or type 'exit' to quit.    ║
    ║                                                 ║
    ╚═════════════════════════════════════════════════╝
    """
    print(welcome_message)
    logger.info(f"Found tables: {', '.join(tables)}")
    print(f"\nFound tables: {', '.join(tables)}")

    while True:
        user_query = input("\nEnter your query: ").strip()
        
        if user_query.lower() == 'exit':
            logger.info("User requested to exit the system")
            print("\nThank you for using the sqlrag Query System. See you soon!\n")
            break
        
        logger.info(f"Received user query: {user_query}")
        print("\nProcessing query...")

        try:
            result = process_query(sql_database, query_engine, user_query)
            
            print("\nAnswer:")
            print(result['answer'])
            print("\nSQL Query:")
            print(result['sql_query'])
            print("\nData:")
            print(result['data'].to_string(index=False))

            logger.info("Query processed successfully")
            print("\nQuery processed successfully!")
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            print(f"\nAn error occurred while processing the query: {str(e)}")

if __name__ == "__main__":
    main()