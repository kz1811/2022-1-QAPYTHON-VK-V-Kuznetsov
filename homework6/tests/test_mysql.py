import pytest
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder
from models.models import *


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)

        self.prepare()

    def table_requests_total(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TotalRequestsModel).filter_by(**filters)
        return res.all()

    def get_table_requests_by_type(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(TotalRequestsByTypeModel).filter_by(**filters)
        return res.all()

    def get_table_10_most_frequent_requests(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(MostFrequentRequestsModel).filter_by(**filters)
        return res.all()

    def get_table_5_longest_with_4XX(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(LongestRequestsModel).filter_by(**filters)
        return res.all()

    def get_table_5_users_with_highest_number_of_req_code_5XX(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(HighestNumberRequestsIpModel).filter_by(**filters)
        return res.all()


class TestSqlOrm(MyTest):

    table = None

    def prepare(self):
        self.builder.create_table_requests_total()
        self.builder.create_table_requests_by_type()
        self.builder.create_table_10_most_frequent_requests()
        self.builder.create_table_5_longest_with_4XX()
        self.builder.create_table_5_users_with_highest_number_of_req_code_5XX()

    def test_get_tables(self):
        count = self.table_requests_total()
        assert len(count) == 1

        count = self.get_table_requests_by_type()
        assert len(count) == 4

        count = self.get_table_10_most_frequent_requests()
        assert len(count) == 10

        count = self.get_table_5_longest_with_4XX()
        assert len(count) == 5

        count = self.get_table_5_users_with_highest_number_of_req_code_5XX()
        assert len(count) == 5
