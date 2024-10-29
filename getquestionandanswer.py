import json
import pandas as pd

# 提示用户输入原生JSON文本
print("请输入原生JSON文本，输入 'END' 结束输入:")

# 初始化一个空字符串来存储输入的JSON文本
data_json = ""
while True:
    line = input()
    if line.strip() == "END":  # 检查是否输入结束标记
        break
    data_json += line + "\n"  # 将每行添加到data_json中

try:
    # 尝试解析JSON数据
    data = json.loads(data_json)

    # 初始化列表来存储提取的数据
    filtered_records = []

    # 遍历records，提取符合条件的记录
    for record in data['data']['records']:
        for item in record['recordList']:
            # 检查poolId是否为指定值
            filtered_records.append({
                'poolId': item['poolId'],
                'questionAnswer': item['questionAnswer'],
                'questionId': item['questionId'],
                'questionType': item['questionType'],
                'userQueAnswernswer': item['userQueAnswernswer'],
                'userQueRes': item['userQueRes']
            })

    # 创建一个DataFrame
    df = pd.DataFrame(filtered_records)

    # 将DataFrame写入Excel文件
    output_file = 'input.xlsx'
    df.to_excel(output_file, index=False)

    print(f"数据已成功写入 {output_file}")

except json.JSONDecodeError as e:
    print(f"JSON解析失败: {e}")
