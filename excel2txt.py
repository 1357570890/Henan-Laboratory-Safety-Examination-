import pandas as pd


def excel_to_txt_simple(excel_file, txt_file):
    # 读取Excel文件
    df = pd.read_excel(excel_file)

    # 只选择需要的列
    selected_df = df[['questionAnswer', 'questionContent']]

    # 将数据框转换为CSV格式的字符串
    text_content = selected_df.to_csv(index=False)

    # 将内容写入txt文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(text_content)


excel_to_txt_simple("题库.xlsx", '题库.txt')