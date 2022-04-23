import re
import operator
from optparse import OptionParser
import json

parser = OptionParser()

parser.add_option('-j', '--json', dest='json', action='store_true', default=False)

methods_list = ['POST', 'GET', 'HEAD', 'PUT', 'DELETE']

num_of_requests = {}
file_list = []
with open("access.log") as log:
    answer_1 = 0
    for i in log:
        try:
            answer_1 += 1
            read_str = re.findall(r'(\d+.\d+.\d+.\d+) (\w+|\-) (\w+|\-) \[(.+)\] \"(.+)\" (\d+|\-) (\d+|\-) \"(.*)\" '
                                  r'\"(.*)\"', i.strip())[0]

            if read_str[4].split(' ')[0] not in methods_list:
                raise Exception

            file_list.append({})
            file_list[-1]['ip'] = read_str[0]
            file_list[-1]['time'] = read_str[4]
            file_list[-1]['request_type'] = read_str[4].split(' ')[0]
            file_list[-1]['request_url'] = read_str[4].split(' ')[1]
            file_list[-1]['request_size'] = len(file_list[-1]['request_url'])
            file_list[-1]['response_code'] = read_str[5]

            if file_list[-1]['request_url'] in num_of_requests.keys():
                num_of_requests[f'{file_list[-1]["request_url"]}'] += 1
            else:
                num_of_requests[f'{file_list[-1]["request_url"]}'] = 1

        except Exception:
            pass

#  Creating json with collected data
options, args = parser.parse_args()
if options.json:
    with open('access.json', 'w') as file:
        jsonstr = json.dumps(file_list)
        file.write(jsonstr)

#  2

answer_2 = {}

for i in file_list:
    if i["request_type"] in answer_2.keys():
        answer_2[f'{i["request_type"]}'] += 1
    else:
        answer_2[f'{i["request_type"]}'] = 1

#  3

answer_3 = {}

#  sorting
num_of_requests_sorted_l = sorted(num_of_requests.items(), key=operator.itemgetter(1), reverse = True)
num_of_requests_sorted = dict(num_of_requests_sorted_l)

#  5 first elements
num = 0
for i in num_of_requests_sorted:
    answer_3[i] = num_of_requests_sorted[i]
    num+=1
    if num >=10:
        break

#  4

#  req with code 4XX
requ_respcode_400 = []
for i in file_list:
    if int(i['response_code'])//100 == 4:
        requ_respcode_400.append(i)

#  list creating
answer_4 = []
for i in range(5):
    req_size = 0
    temp_list = {}
    for j in range(len(requ_respcode_400)):
        if requ_respcode_400[j]['request_size'] >= req_size:
            flag = 0
            for elem in answer_4:
                if elem['request_url'] == requ_respcode_400[j]['request_url']:
                    flag += 1
            if flag == 0:
                temp_list = requ_respcode_400[j]
                req_size = requ_respcode_400[j]['request_size']
    answer_4.append(temp_list)

#  5

#  req with code 5XX
requests_with_respcode_500 = []
for i in file_list:
    if int(i['response_code'])//100 == 5:
        requests_with_respcode_500.append(i)

#  creating dict {ip: number_of_requests}
users_req_list = {}
for i in requests_with_respcode_500:
    if i['ip'] in users_req_list.keys():
        users_req_list[f'{i["ip"]}'] += 1
    else:
        users_req_list[f'{i["ip"]}'] = 1

#  sorting
users_req_sorted = sorted(users_req_list.items(), key=operator.itemgetter(1), reverse=True)
users_req_sorted = dict(users_req_sorted)
num = 0

#  5 first elements
answer_5 = {}
for i in users_req_sorted:
    answer_5[i] = users_req_sorted[i]
    num += 1
    if num >= 5:
        break


#  add data to file
with open('results.txt', 'w') as file:

    #  1
    file.write('Number of requests:\n\n')
    file.write(str(answer_1) + '\n')

    #  2
    file.write('\n\nNumber of requests by type: \n\n')
    for i in answer_2.keys():
        file.write(i + ': ' + str(answer_2[i]) + '\n')

    #  3
    file.write('\n\nMost 10 often requests: \n\n')
    for i in answer_3.keys():
        file.write('url:' + i + '; number of requests: ' + str(answer_3[i]) + '\n')

    #  4
    file.write('\n\nMost 5 longest requests with response code 4XX:\n\n')
    for i in answer_4:
        file.write(
            'url: ' + str(i['request_url']) + '; status code: ' + str(i['response_code']) + '; request size: ' + str(
                i['request_size']) + '; ip: ' + str(i['ip']) + '\n')

    #  5
    file.write('\n\n5 users with the most requests with response code 5XX:\n\n')
    for i in answer_5.keys():
        file.write('ip:' + i + '; number of requests: ' + str(answer_5[i]) + '\n')
