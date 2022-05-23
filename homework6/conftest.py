import pytest
from mysql.client import MysqlClient


def pytest_configure(config):
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_table('Total')
        mysql_client.create_table('Total_by_type')
        mysql_client.create_table('Top_frequent_requests')
        mysql_client.create_table('Top_long_requests_with_code_4XX')
        mysql_client.create_table('Top_IPs_with_highest_number_of_req_code_5XX')

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()
