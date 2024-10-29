import requests
import json
import time
import pandas as pd


# 定义获取题目的函数
def get_question(question_id):
    url = f"http://1.94.224.181:8897/api/biz/examPoolStudy/getQuestInfoById?id={question_id}"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Cookie": "tokenName=token; sidebarStatus=0; token=b153d0faab2244d186f405b232b4156e; tokenValue=b153d0faab2244d186f405b232b4156e",
        "Host": "1.94.224.181:8897",
        "Referer": "http://1.94.224.181:8897/learn/questions",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "token": "b153d0faab2244d186f405b232b4156e"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # 返回题目信息


# 读取输入文件
df = pd.read_excel('input.xlsx')

# 创建一个列表存储所有需要的数据
result_list = []

for index, row in df.iterrows():
    question_id = row['questionId']

    # 获取题目信息
    question_info = get_question(question_id)
    time.sleep(0.1)
    if question_info and 'data' in question_info:
        data = question_info['data']
        # 只保存需要的字段
        filtered_data = {
            'questionAnswer': row['questionAnswer'],  # 从原始Excel获取
            'questionContent': data.get('questionContent', ''),
            'optionContent': data.get('optionContent', ''),
            'questionExplain': data.get('questionExplain', ''),
            'questionType': row['questionType']  # 从原始Excel获取
        }
        result_list.append(filtered_data)


# 将所有数据转换为新的DataFrame
if result_list:
    result_df = pd.DataFrame(result_list)

    # 保存到新的Excel文件
    result_df.to_excel('output.xlsx', index=False)