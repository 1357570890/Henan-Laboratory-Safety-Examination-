import json
import pyperclip


def process_experiment_data(json_str):
    # 解析JSON字符串
    data = json.loads(json_str)

    # 获取experimentData中的reportDetails
    report_details = data['experimentData']['reportDetails']

    # 计算不同id的数量
    unique_ids = len(set(detail['id'] for detail in report_details))
    total_score = unique_ids * 5

    # 更新总分数
    data['score'] = total_score
    data['experimentData']['score'] = total_score

    # 更新每个reportDetail
    for detail in report_details:
        detail['useda'] = detail['bzda']  # 将useda设置为bzda的值
        detail['useScore'] = 5  # 将useScore设置为5
        detail['isSign'] = True  # 将isSign设置为true
        detail['solution'] = True  # 将solution设置为true

    # 返回处理后的JSON字符串
    return json.dumps(data, ensure_ascii=False)


try:
    # 从用户输入获取JSON字符串
    print("请输入JSON字符串：")
    input_json = input()

    # 处理数据
    result = process_experiment_data(input_json)

    # 将结果复制到剪贴板
    pyperclip.copy(result)
    print("\n处理完成！结果已复制到剪贴板。")

except json.JSONDecodeError:
    print("错误：输入的不是有效的JSON格式")
except Exception as e:
    print(f"发生错误：{str(e)}")



