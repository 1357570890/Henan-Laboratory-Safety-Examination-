# build_exe.py
import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'search_app.py',  # 主程序文件
    '--name=题目搜索工具',  # 生成的exe名称
    '--onefile',  # 打包成单个文件
    '--windowed',  # 使用Windows子系统
    '--icon=icon.ico',  # 程序图标
    '--add-data=tiku.xlsx;.',  # 添加Excel文件
    '--add-data=icon.ico;.',  # 添加图标文件
    '--noconfirm',  # 不确认覆盖
    '--clean',  # 清理临时文件
    f'--distpath={os.path.join(current_dir, "dist")}',  # 输出目录
    f'--workpath={os.path.join(current_dir, "build")}',  # 工作目录
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
])