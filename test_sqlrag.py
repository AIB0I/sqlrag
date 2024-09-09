import unittest
import os
import pandas as pd
import logging
from sqlrag import process_query, initialize_engine
from dotenv import load_dotenv, set_key

# Remove all handlers associated with the root logger object
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Set up logging to write to both app.log file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TestSQLRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up TestSQLRAG class")
        # Set up paths for test data
        cls.sqlite_db = 'sample_data/sqlite/ecommerce.db'
        cls.csv_file = 'sample_data/csv/products.csv'
        cls.env_file = '.env'

    def update_env(self, db_type, db_connection):
        logger.info(f"Updating .env file for {db_type} test")
        set_key(self.env_file, 'DB_TYPE', db_type)
        set_key(self.env_file, 'DB_CONNECTION', db_connection)
        set_key(self.env_file, 'LLM_MODEL', 'llama3.1:8b')
        set_key(self.env_file, 'EMBEDDING_MODEL', 'nomic-embed-text:latest')
        load_dotenv(self.env_file, override=True)

    def test_sqlite_database(self):
        logger.info("Starting SQLite database test")
        self.update_env('sqlite', self.sqlite_db)

        # Assert environment variables
        self.assertEqual(os.getenv('DB_TYPE'), 'sqlite')
        self.assertEqual(os.getenv('DB_CONNECTION'), self.sqlite_db)
        self.assertEqual(os.getenv('LLM_MODEL'), 'llama3.1:8b')
        self.assertEqual(os.getenv('EMBEDDING_MODEL'), 'nomic-embed-text:latest')
        logger.info("Environment variables assertion passed for SQLite test")

        # Test initialize_engine
        logger.info("Testing initialize_engine for SQLite")
        sql_database, tables, query_engine = initialize_engine()
        self.assertIsNotNone(sql_database)
        self.assertIsNotNone(tables)
        self.assertIsNotNone(query_engine)
        logger.info("initialize_engine test passed")

        # Assert table names
        expected_tables = {'products', 'customers', 'orders'}
        self.assertEqual(set(tables), expected_tables, f"Expected tables {expected_tables}, but got {set(tables)}")
        logger.info("Table names assertion passed")

        # Test process_query
        logger.info("Testing process_query for SQLite")
        result = process_query(sql_database, query_engine, "Provide top 3 products by price")        
        logger.info("process_query test passed")
        logger.info(f"SQL Query: {result['sql_query']}")
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Data: {result['data']}")
        self.assertIn('answer', result)
        self.assertIn('sql_query', result)
        self.assertIn('data', result)
        self.assertIn('SELECT', result['sql_query'])


    def test_csv_database(self):
        logger.info("Starting CSV database test")
        self.update_env('csv', self.csv_file)

        # Assert environment variables
        self.assertEqual(os.getenv('DB_TYPE'), 'csv')
        self.assertEqual(os.getenv('DB_CONNECTION'), self.csv_file)
        self.assertEqual(os.getenv('LLM_MODEL'), 'llama3.1:8b')
        self.assertEqual(os.getenv('EMBEDDING_MODEL'), 'nomic-embed-text:latest')
        logger.info("Environment variables assertion passed for CSV test")

        # Test initialize_engine
        logger.info("Testing initialize_engine for CSV")
        sql_database, tables, query_engine = initialize_engine()
        self.assertIsNotNone(sql_database)
        self.assertIsNotNone(tables)
        self.assertIsNotNone(query_engine)
        logger.info("initialize_engine test passed")

        # Assert table names
        expected_tables = {'csv_data'}
        self.assertEqual(set(tables), expected_tables, f"Expected tables {expected_tables}, but got {set(tables)}")
        logger.info("Table names assertion passed")

        # Test process_query
        logger.info("Testing process_query for CSV")
        result = process_query(sql_database, query_engine, "Provide top 3 products by price")
        logger.info("process_query test passed")
        logger.info(f"SQL Query: {result['sql_query']}")
        logger.info(f"Answer: {result['answer']}")
        logger.info(f"Data: {result['data']}")
        self.assertIn('answer', result)
        self.assertIn('sql_query', result)
        self.assertIn('data', result)
        self.assertIn('SELECT', result['sql_query'])


if __name__ == '__main__':
    logger.info("Starting SQLRAG tests")
    unittest.main(verbosity=2)