import os
from model.engine.db_engine import Storage

os.environ['DB_USER'] = 'echodat_db_manager'
os.environ['DB_PASSWORD'] = 'fe02ab2194a55a7d99c0d00b734193c57be6993a3045f17a8d818ca529d54ddec81fb15e6e3dd865c4ae'
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '3306'
os.environ['DB_NAME'] = 'echodat_db'

storage = Storage()
