import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from models.models import Base

class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = 3306
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):

        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def create_table(self, name):
        if not inspect(self.engine).has_table(name):
            Base.metadata.tables[name].create(self.engine)

    def create_table_Total(self):
        if not inspect(self.engine).has_table('Total'):
            Base.metadata.tables['Total'].create(self.engine)

    def create_table_Total_by_type(self):
        if not inspect(self.engine).has_table('Total_by_type'):
            Base.metadata.tables['Total_by_type'].create(self.engine)

    def create_table_Top_frequent_requests(self):
        if not inspect(self.engine).has_table('Top_frequent_requests'):
            Base.metadata.tables['Top_frequent_requests'].create(self.engine)

    def create_table_Top_5_freq_requests_with_code_4XX(self):
        if not inspect(self.engine).has_table('Top_5_freq_requests_with_code_4XX'):
            Base.metadata.tables['Top_5_long_requests_with_code_4XX'].create(self.engine)

    def create_table_Top_5_IPs_with_highest_number_with_req_code_5XX(self):
        if not inspect(self.engine).has_table('Top_5_IPs_with_highest_number_with_req_code_5XX'):
            Base.metadata.tables['Top_5_IPs_with_highest_number_of_req_code_5XX'].create(self.engine)

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

