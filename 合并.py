import pandas as pd
import os

# 创建一个空列表来存储所有的DataFrame
all_dfs = []

# 遍历1到13的文件名（跳过9）
for i in range(1, 14):
    if i == 9:  # 跳过9.xlsx
        continue

    filename = f"{i}.xlsx"
    if os.path.exists(filename):  # 检查文件是否存在
        try:
            # 读取Excel文件
            df = pd.read_excel(filename)
            # 添加一个来源列，标识数据来自哪个文件
            df['source_file'] = f"{i}.xlsx"
            # 将DataFrame添加到列表中
            all_dfs.append(df)
            print(f"成功读取 {filename}")
        except Exception as e:
            print(f"读取 {filename} 时出错: {str(e)}")

# 合并所有DataFrame
if all_dfs:
    # 使用concat合并所有DataFrame，保持所有列
    merged_df = pd.concat(all_dfs, ignore_index=True)

    # 删除可能的重复列
    merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

    # 保存合并后的文件
    merged_df.to_excel('merged_output.xlsx', index=False)
    print(f"\n合并完成！总行数: {len(merged_df)}")
    print(f"列名: {list(merged_df.columns)}")
else:
    print("没有找到可以合并的文件！")