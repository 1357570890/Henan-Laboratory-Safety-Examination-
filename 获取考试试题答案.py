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

# 创建一个列表存储所有question_info
question_info_list = []

for index, row in df.iterrows():
    question_id = row['questionId']
    correct_answer = row['questionAnswer']
    question_type = row['questionType']
    pool_id = row['poolId']

    # 获取题目信息
    question_info = get_question(question_id)

    # 如果成功获取到题目信息，将其添加到原始数据中
    if question_info:
        # 将question_info（字典格式）扁平化处理
        question_info_flat = pd.json_normalize(question_info.get('data', {}))

        # 如果获取到了题目信息，将其添加到列表中
        if not question_info_flat.empty:
            question_info_list.append(question_info_flat.iloc[0])

    # 添加适当的延时以避免请求过于频繁
    time.sleep(1)

# 将所有question_info转换为DataFrame
if question_info_list:
    question_info_df = pd.DataFrame(question_info_list)

    # 将原始DataFrame与新的question_info_df横向合并
    result_df = pd.concat([df, question_info_df], axis=1)

    # 保存到新的Excel文件
    result_df.to_excel('output.xlsx', index=False)



