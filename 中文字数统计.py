import tkinter as tk
from tkinter import messagebox

def count_chinese_characters(text):
    count = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
    return count

def on_count():
    text = text_entry.get("1.0", tk.END)
    chinese_count = count_chinese_characters(text)
    messagebox.showinfo("结果", f"中文字符数量: {chinese_count}")

# 创建主窗口
root = tk.Tk()
root.title("中文字符统计工具")

# 创建文本框
text_entry = tk.Text(root, height=10, width=50)
text_entry.pack(pady=10)

# 创建按钮
count_button = tk.Button(root, text="统计中文字符", command=on_count)
count_button.pack(pady=5)

# 运行主循环
root.mainloop()
