import re
import operator


class Parser:

    def __init__(self, path):
        self.file_data, self.num_of_req_data = self.reading(path)

    def reading(self, path):
        num_of_requests_dict = {}
        file_data_dict = []
        with open(path) as log:
            for i in log:
                try:
                    read_str = \
                    re.findall(r'(\d+.\d+.\d+.\d+) (\w+|\-) (\w+|\-) \[(.+)\] \"(.+)\" (\d+|\-) (\d+|\-) \"(.*)\" '
                               r'\"(.*)\"', i.strip())[0]

                    ###########################################################################

                    if len(read_str[4].split(' ')[0]) > 10:
                        raise Exception

                    ###########################################################################
                    file_data_dict.append({})
                    file_data_dict[-1]['ip'] = read_str[0]
                    file_data_dict[-1]['time'] = read_str[4]
                    file_data_dict[-1]['request_type'] = read_str[4].split(' ')[0]
                    file_data_dict[-1]['request_url'] = read_str[4].split(' ')[1]
                    file_data_dict[-1]['request_size'] = len(file_data_dict[-1]['request_url'])
                    file_data_dict[-1]['response_code'] = read_str[5]

                    if file_data_dict[-1]['request_url'] in num_of_requests_dict.keys():
                        num_of_requests_dict[f'{file_data_dict[-1]["request_url"]}'] += 1
                    else:
                        num_of_requests_dict[f'{file_data_dict[-1]["request_url"]}'] = 1
                except Exception:
                    pass
        return file_data_dict, num_of_requests_dict

    def collect_requests(self, file_data):
        return len(file_data)

    def collect_requests_by_type(self, file_data):
        result = {}

        for i in file_data:
            if i["request_type"] in result.keys():
                result[f'{i["request_type"]}'] += 1
            else:
                result[f'{i["request_type"]}'] = 1

        return result

    def get_most_frequent_requests(self, num_of_requests_dict, number):

        result = {}

        #  sorting
        num_of_requests_sorted_l = sorted(num_of_requests_dict.items(), key=operator.itemgetter(1), reverse=True)
        num_of_requests_sorted = dict(num_of_requests_sorted_l)

        #  N first elements
        num = 0
        for i in num_of_requests_sorted:
            result[i] = num_of_requests_sorted[i]
            num += 1
            if num >= number:
                break

        # return
        return result

    def get_requests_with_code(self, file_data, n):
        #  req with code N
        result = []
        for i in file_data:
            if int(i['response_code']) // 100 == (n // 100):
                result.append(i)
        return result

    def get_longest_requests(self, file_data, number):

        result = []
        for i in range(number):
            req_size = 0
            temp_list = {}
            for j in range(len(file_data)):
                if file_data[j]['request_size'] >= req_size:
                    flag = 0
                    for elem in result:
                        if elem['request_url'] == file_data[j]['request_url']:
                            flag += 1
                    if flag == 0:
                        temp_list = file_data[j]
                        req_size = file_data[j]['request_size']
            result.append(temp_list)
        return result

    def get_users_with_highest_number_of_req(self, file_data, n):

        users_req_list = {}
        for i in file_data:
            if i['ip'] in users_req_list.keys():
                users_req_list[f'{i["ip"]}'] += 1
            else:
                users_req_list[f'{i["ip"]}'] = 1

        #  sorting
        users_req_sorted = sorted(users_req_list.items(), key=operator.itemgetter(1), reverse=True)
        users_req_sorted = dict(users_req_sorted)
        num = 0

        #  N first elements
        result = {}

        for i in users_req_sorted:
            result[i] = users_req_sorted[i]
            num += 1
            if num >= n:
                break

        return result
