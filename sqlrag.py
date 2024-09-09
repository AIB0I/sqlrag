import os
import sqlite3
from dotenv import load_dotenv
from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import pandas as pd

# Load environment variables
load_dotenv()

# Get configurations from environment variables
DB = os.getenv('DB')
LLM_MODEL = os.getenv('LLM_MODEL')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')

def get_table_names(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

# Connect to the SQL database
db_url = f"sqlite:///{DB}"
sql_database = SQLDatabase.from_uri(db_url)

# Get table names automatically
tables = get_table_names(DB)

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

# Function to handle user queries
def process_query(user_query):
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
    print(f"\nFound tables: {', '.join(tables)}")
    
    while True:
        user_query = input("\nEnter your query: ").strip()
        
        if user_query.lower() == 'exit':
            print("\nThank you for using the sqlrag Query System. See you soon!\n")
            break
        
        print("\nProcessing query...")

        result = process_query(user_query)
        
        print("\nAnswer:")
        print(result['answer'])
        print("\nSQL Query:")
        print(result['sql_query'])
        print("\nData:")
        print(result['data'].to_string(index=False))

        print("\nQuery processed successfully!")

if __name__ == "__main__":
    main()