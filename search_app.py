# search_app.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sys
import os
from pathlib import Path


def resource_path(relative_path):
    """ 获取资源的绝对路径，用于处理打包后的资源文件路径 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("题目搜索工具")
        self.root.geometry("800x600")

        # 尝试设置窗口图标
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except:
            pass  # 如果没有图标文件，就使用默认图标

        # 加载Excel数据
        try:
            excel_path = resource_path('tiku.xlsx')
            self.df = pd.read_excel(excel_path)
            # 确保数据框包含必要的列
            if 'questionContent' not in self.df.columns or 'questionAnswer' not in self.df.columns:
                raise ValueError("Excel文件格式不正确，需要包含'questionContent'和'questionAnswer'列")
        except Exception as e:
            messagebox.showerror("错误", f"无法加载Excel文件：{str(e)}\n\n请确保'merged_output.xlsx'文件存在且格式正确。")
            self.root.destroy()
            return

        # 创建主框架
        main_frame = ttk.Frame(root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # 创建搜索框和按钮
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill='x', pady=5)

        ttk.Label(search_frame, text="请输入搜索内容：").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side='left', padx=5)

        search_button = ttk.Button(search_frame, text="搜索", command=self.search)
        search_button.pack(side='left', padx=5)

        # 创建工具栏
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill='x', pady=5)

        ttk.Button(toolbar, text="复制选中", command=self.copy_selected).pack(side='left', padx=5)
        ttk.Button(toolbar, text="导出结果", command=self.export_results).pack(side='left', padx=5)

        # 创建结果显示表格
        self.create_treeview(main_frame)

        # 绑定快捷键
        self.root.bind('<Return>', lambda e: self.search())
        self.root.bind('<Control-c>', lambda e: self.copy_selected())

        # 设置焦点到搜索框
        self.search_entry.focus()

    def create_treeview(self, parent):
        # 创建表格框架
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill='both', expand=True)

        # 创建表格和滚动条
        columns = ('题目内容', '答案')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

        # 设置列标题和宽度
        self.tree.heading('题目内容', text='题目内容')
        self.tree.heading('答案', text='答案')
        self.tree.column('题目内容', width=500)
        self.tree.column('答案', width=200)

        # 添加滚动条
        y_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # 放置表格和滚动条
        self.tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        # 配置grid权重
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def search(self):
        search_text = self.search_var.get().strip()
        if not search_text:
            messagebox.showwarning("提示", "请输入搜索内容！")
            return

        # 清空现有结果
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            mask = self.df['questionContent'].str.contains(search_text, case=False, na=False)
            results = self.df[mask]

            if len(results) == 0:
                messagebox.showinfo("提示", "未找到匹配的结果！")
                return

            for _, row in results.iterrows():
                self.tree.insert('', 'end', values=(
                    row['questionContent'],
                    row['questionAnswer']
                ))

        except Exception as e:
            messagebox.showerror("错误", f"搜索出错：{str(e)}")

    def copy_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("提示", "请先选择要复制的内容！")
            return

        item = self.tree.item(selected[0])
        content = f"题目：{item['values'][0]}\n答案：{item['values'][1]}"
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("成功", "已复制到剪贴板！")

    def export_results(self):
        if len(self.tree.get_children()) == 0:
            messagebox.showinfo("提示", "没有可导出的结果！")
            return

        try:
            results = []
            for item in self.tree.get_children():
                results.append(self.tree.item(item)['values'])

            result_df = pd.DataFrame(results, columns=['题目内容', '答案'])
            result_df.to_excel('搜索结果.xlsx', index=False)
            messagebox.showinfo("成功", "结果已导出到'搜索结果.xlsx'")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{str(e)}")


def main():
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()