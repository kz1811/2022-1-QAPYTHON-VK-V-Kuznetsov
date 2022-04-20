from models.models import *
from script import Parser


class MysqlBuilder:
    def __init__(self, client):
        self.client = client
        self.parse = Parser("homework6/access.log")

    def create_table_requests_total(self):

        res = self.parse.collect_requests(self.parse.file_data)

        total = TotalRequestsModel(
            number_of_requests=res,
        )
        self.client.session.add(total)
        self.client.session.commit()

        return total

    def create_table_requests_by_type(self):

        by_type = None
        res = self.parse.collect_requests_by_type(self.parse.file_data)

        for i in res.keys():
            by_type = TotalRequestsByTypeModel(
                type=i,
                number_of_requests=res[i]
            )
            self.client.session.add(by_type)
        self.client.session.commit()

        return by_type

    def create_table_10_most_frequent_requests(self):

        most_freq = None
        res = self.parse.get_most_frequent_requests(self.parse.num_of_req_data, 10)

        for i in res.keys():

            most_freq = MostFrequentRequestsModel(
                url=i,
                number_of_requests=res[i],
            )
            self.client.session.add(most_freq)
        self.client.session.commit()

        return most_freq

    def create_table_5_longest_with_4XX(self):

        table_5_long_req = None
        res = self.parse.get_longest_requests(self.parse.get_requests_with_code(self.parse.file_data, 400), 5)

        for i in res:
            table_5_long_req = LongestRequestsModel(
                url=i['request_url'],
                status_code=i['response_code'],
                request_size=i['request_size'],
                ip=i['ip'],
            )
            self.client.session.add(table_5_long_req)
        self.client.session.commit()

        return table_5_long_req

    def create_table_5_users_with_highest_number_of_req_code_5XX(self):

        highest_num_of_req = None
        res = self.parse.get_users_with_highest_number_of_req(self.parse.get_requests_with_code(self.parse.file_data, 500), 5)

        for i in res.keys():
            highest_num_of_req = HighestNumberRequestsIpModel(
                ip=i,
                number_of_requests=res[i],
            )
            self.client.session.add(highest_num_of_req)

        self.client.session.commit()

        return highest_num_of_req
