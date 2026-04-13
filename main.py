#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Steam Depot Downloader GUI
使用 ttkbootstrap 创建的桌面应用程序，用于通过 DepotDownloader 下载 Steam 游戏
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip
import subprocess
import threading
import json
import re
import sys
import os
from pathlib import Path
import webbrowser
import update_checker  # 导入更新检查模块
local_version = "2026.4.13.1"  # 当前程序版本号
tool_name = "SteamDepotDownloader"   # 单个客户端版本的api接口信息,自己打包的版本，可以配置自动更新

class SteamDepotDownloaderGUI:
    def __init__(self):
        # 创建主窗口
        self.root = ttkb.Window(themename="superhero")
        self.root.title("Steam Depot Downloader GUI             B站.怀沙2049")
        self.root.geometry("1000x670")
        
        # 锁定窗口大小，不可调整
        self.root.resizable(False, False)
        
        # 设置窗口居中显示
        self.center_window()
        
        # 设置窗口图标（如果有）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # 显示版本号（仅用于 UI 展示）
        self.display_version = "1.0.0"
        self.version_url = "https://github.com/huaisha1224"
        
        # DepotDownloader 路径
        self.depotdownloader_path = self.find_depotdownloader()
        
        # 创建变量
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.app_id_var = tk.StringVar()
        self.depot_id_var = tk.StringVar()
        self.manifest_id_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.no_mobile_auth_var = tk.BooleanVar(value=False)
        
        # 进程管理
        self.process = None
        self.is_running = False
        
        # 创建 UI
        self.create_ui()
        
        # 绑定事件
        self.bind_events()
        
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def find_depotdownloader(self):
        """查找 DepotDownloader 可执行文件"""
        # 可能的路径
        possible_paths = [
            Path(__file__).parent / "src" / "DepotDownloader.exe",  # src 目录
            Path(__file__).parent / "DepotDownloader" / "DepotDownloader.exe",
            Path(__file__).parent / "src-tauri" / "resources" / "DepotDownloader" / "windows-x64" / "DepotDownloader.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "SteamDepotDownloaderGUI" / "DepotDownloader.exe",
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # 如果都找不到，返回默认值
        return "DepotDownloader.exe"
    
    def create_ui(self):
        """创建用户界面"""
        # 主框架
        main_frame = ttkb.Frame(self.root, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)
        
        # 标题
        title_label = ttkb.Label(
            main_frame,
            text="Steam游戏 历史版本下载器",
            font=("Arial", 24, "bold"),
            bootstyle=PRIMARY
        )
        title_label.pack(pady=(0, 20))
        
        # 副标题说明
        subtitle_label = ttkb.Label(
            main_frame,
            text="通过 DepotDownloader 下载 Steam 游戏的指定历史版本（Manifest）",
            font=("Arial", 10),
            bootstyle=INFO
        )
        subtitle_label.pack(pady=(0, 10))
        
        # 创建左右分栏框架
        content_frame = ttkb.Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=YES)
        
        # 左侧输入区域
        left_frame = ttkb.Frame(content_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))
        
        # 右侧输出区域
        right_frame = ttkb.Frame(content_frame)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        # 创建输入框架（左侧）
        self.create_input_frame(left_frame)
        
        # 创建输出框架（右侧）
        self.create_output_frame(right_frame)
        
        # 创建按钮框架
        self.create_button_frame(main_frame)
        
    def create_input_frame(self, parent):
        """创建输入框架"""
        input_frame = ttkb.LabelFrame(parent, text="下载配置", padding=15)
        input_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))
        
        # Steam 账号
        username_frame = ttkb.Frame(input_frame)
        username_frame.pack(fill=X, pady=3)
        ttkb.Label(username_frame, text="Steam 账号:", width=15).pack(anchor=W)
        username_entry = ttkb.Entry(
            username_frame,
            textvariable=self.username_var,
            width=50,
            bootstyle=PRIMARY
        )
        username_entry.pack(fill=X, pady=(2, 0))
        
        # Steam 密码
        password_frame = ttkb.Frame(input_frame)
        password_frame.pack(fill=X, pady=3)
        ttkb.Label(password_frame, text="Steam 密码:", width=15).pack(anchor=W)
        password_entry = ttkb.Entry(
            password_frame,
            textvariable=self.password_var,
            width=50,
            show="*",
            bootstyle=PRIMARY
        )
        password_entry.pack(fill=X, pady=(2, 0))
        
        # App ID
        app_frame = ttkb.Frame(input_frame)
        app_frame.pack(fill=X, pady=3)
        ttkb.Label(app_frame, text="App ID *:", width=15).pack(anchor=W)
        app_entry = ttkb.Entry(app_frame, textvariable=self.app_id_var, width=50, bootstyle=PRIMARY)
        app_entry.pack(fill=X, pady=(2, 0))
        
        # Depot ID
        depot_frame = ttkb.Frame(input_frame)
        depot_frame.pack(fill=X, pady=3)
        ttkb.Label(depot_frame, text="Depot ID *:", width=15).pack(anchor=W)
        depot_entry = ttkb.Entry(depot_frame, textvariable=self.depot_id_var, width=50, bootstyle=PRIMARY)
        depot_entry.pack(fill=X, pady=(2, 0))
        
        # Manifest ID
        manifest_frame = ttkb.Frame(input_frame)
        manifest_frame.pack(fill=X, pady=3)
        ttkb.Label(manifest_frame, text="Manifest ID *:", width=15).pack(anchor=W)
        manifest_entry = ttkb.Entry(manifest_frame, textvariable=self.manifest_id_var, width=50, bootstyle=PRIMARY)
        manifest_entry.pack(fill=X, pady=(2, 0))
        
        # 输出目录
        output_frame = ttkb.Frame(input_frame)
        output_frame.pack(fill=X, pady=3)
        ttkb.Label(output_frame, text="下载路径 *:", width=15).pack(anchor=W)
        output_entry = ttkb.Entry(
            output_frame,
            textvariable=self.output_path_var,
            width=50,
            bootstyle=PRIMARY,
            state='readonly'  # 设置为只读，只能通过按钮选择
        )
        output_entry.pack(fill=X, pady=(2, 0))
        
        # 目录操作按钮
        button_frame = ttkb.Frame(input_frame)
        button_frame.pack(fill=X, pady=3)
        
        choose_btn = ttkb.Button(
            button_frame,
            text="📁 选择目录",
            command=self.choose_output_directory,
            bootstyle=SUCCESS,
            width=15
        )
        choose_btn.pack(side=LEFT, padx=(0, 10))
        
        preview_btn = ttkb.Button(
            button_frame,
            text="👁️ 打开目录",
            command=self.preview_output,
            bootstyle=INFO,
            width=12
        )
        preview_btn.pack(side=LEFT)
        
        # 高级选项
        advanced_frame = ttkb.Frame(input_frame)
        advanced_frame.pack(fill=X, pady=5)
        
        no_mobile_check = ttkb.Checkbutton(
            advanced_frame,
            text="不使用手机验证",
            variable=self.no_mobile_auth_var,
            bootstyle=WARNING
        )
        no_mobile_check.pack(side=LEFT)
        
    def create_output_frame(self, parent):
        """创建输出框架"""
        output_frame = ttkb.LabelFrame(parent, text="下载输出", padding=15)
        output_frame.pack(fill=BOTH, expand=YES, pady=(0, 10))
        
        # 创建文本框和滚动条
        text_frame = ttkb.Frame(output_frame)
        text_frame.pack(fill=BOTH, expand=YES)
        
        scrollbar = ttkb.Scrollbar(text_frame, bootstyle=SUCCESS)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.output_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg="#1e1e1e",
            fg="#d4d4d4",
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            height=15  # 设置固定行数，避免过度扩展
        )
        self.output_text.pack(fill=BOTH, expand=YES)
        scrollbar.config(command=self.output_text.yview)
        
        # 清空按钮
        clear_btn = ttkb.Button(
            output_frame,
            text="清空",
            command=self.clear_output,
            bootstyle=DANGER,
            width=10
        )
        clear_btn.pack(anchor=E, pady=(5, 0))
    
    def open_version_link(self):
        """打开版本号链接"""
        import webbrowser
        webbrowser.open(self.version_url)
    
    def create_button_frame(self, parent):
        """创建按钮框架"""
        button_frame = ttkb.Frame(parent)
        button_frame.pack(fill=X, pady=10)
        
        # 下载按钮
        self.download_btn = ttkb.Button(
            button_frame,
            text="⬇️ 开始下载",
            command=self.start_download,
            bootstyle=WARNING,  # 橙色按钮
            width=20
        )
        self.download_btn.pack(side=LEFT, padx=(0, 10))
        
        # 使用帮助按钮
        help_btn = ttkb.Button(
            button_frame,
            text="📖 使用帮助",
            command=self.show_help,
            bootstyle=INFO,
            width=15
        )
        help_btn.pack(side=LEFT, padx=(0, 10))
        
        # 关于按钮
        about_btn = ttkb.Button(
            button_frame,
            text="ℹ️ 关于",
            command=self.show_about,
            bootstyle=INFO,
            width=15
        )
        about_btn.pack(side=LEFT)
        
        # 版本号标签（右下角）
        version_label = ttkb.Label(
            button_frame,
            text=f"v{self.display_version}",
            font=("Arial", 12, "bold"),
            bootstyle="info"
        )
        version_label.pack(side=RIGHT, padx=10, pady=5)
        
        # 添加鼠标点击事件
        version_label.bind("<Button-1>", lambda e: self.open_version_link())
        # 添加鼠标悬停效果
        version_label.bind("<Enter>", lambda e: version_label.config(cursor="hand2"))
    
    def show_help(self):
        """显示使用帮助"""
        import webbrowser
        webbrowser.open("https://www.bilibili.com/video/BV1zvQbBkEFL/")
    
    def bind_events(self):
        """绑定事件"""
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def show_about(self):
        """显示关于对话框"""
        about_window = ttkb.Toplevel(self.root)
        about_window.title("关于")
        about_window.geometry("500x400")
        about_window.resizable(False, False)
        
        # 居中显示
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (about_window.winfo_screenheight() // 2) - (400 // 2)
        about_window.geometry(f"500x400+{x}+{y}")
        
        frame = ttkb.Frame(about_window, padding=30)
        frame.pack(fill=BOTH, expand=YES)
        
        # 标题
        ttkb.Label(
            frame,
            text="Steam 游戏历史版本下载器",
            font=("Arial", 20, "bold"),
            bootstyle=PRIMARY
        ).pack(pady=(0, 20))
        
        # 版本信息
        ttkb.Label(
            frame,
            text=f"版本：{self.display_version}",
            font=("Arial", 12)
        ).pack(pady=5)
        
        # 描述
        description = """这是一个用于下载 Steam 游戏历史版本的工具。
通过DepotDownloader实现，可以下载指定版本的游戏文件。"""
        
        ttkb.Label(
            frame,
            text=description,
            font=("Arial", 10),
            wraplength=400,
            justify="center"
        ).pack(pady=20)
        
        # 分隔线
        ttkb.Separator(frame, orient="horizontal", bootstyle="info").pack(fill=X, pady=20)
        
        # 技术栈
        ttkb.Label(
            frame,
            text="作者：怀沙2049",
            font=("Arial", 10)
        ).pack(pady=5)
        
        # 相关链接
        ttkb.Label(
            frame,
            text="相关链接:",
            font=("Arial", 10, "bold")
        ).pack(pady=(20, 5))
        
        links_frame = ttkb.Frame(frame)
        links_frame.pack()
        
        links = [
            ("DepotDownloader", "https://github.com/SteamRE/DepotDownloader"),
            ("SteamDB", "https://steamdb.info"),
            ("GitHub主页", "https://github.com/huaisha1224"),
            ("B站主页", "https://space.bilibili.com/37443749")
        ]
        
        for text, url in links:
            btn = ttkb.Button(
                links_frame,
                text=text,
                command=lambda u=url: webbrowser.open(u),
                bootstyle="info-outline",
                width=12  # 减小宽度，让按钮更紧凑
            )
            btn.pack(side=LEFT, padx=3, pady=5)  # 减小间距
        
        # 关闭按钮
        ttkb.Button(
            frame,
            text="关闭",
            command=about_window.destroy,
            bootstyle=SUCCESS,
            width=20
        ).pack(pady=(30, 0))
    
    def choose_output_directory(self):
        """选择输出目录"""
        directory = filedialog.askdirectory(title="选择下载目录")
        if directory:
            self.output_path_var.set(directory)
    
    def preview_output(self):
        """预览输出目录"""
        path = self.output_path_var.get()
        if not path:
            messagebox.showwarning("警告", "请先选择输出目录")
            return
        
        if os.path.exists(path):
            os.startfile(path)
        else:
            if messagebox.askyesno("目录不存在", "目录不存在，是否创建？"):
                os.makedirs(path)
                os.startfile(path)
    
    
    def clear_output(self):
        """清空输出"""
        self.output_text.delete(1.0, END)
    
    def start_download(self):
        """开始下载"""
        
        # 验证输入
        if not self.validate_inputs():
            return
        
        # 检查 DepotDownloader
        if not os.path.exists(self.depotdownloader_path):
            messagebox.showerror(
                "错误",
                f"找不到 DepotDownloader\n路径：{self.depotdownloader_path}\n\n请先下载 DepotDownloader"
            )
            return
        
        # 禁用下载按钮 - 更明显的状态提示
        self.download_btn.config(
            state=DISABLED, 
            text="⏳ 正在下载中...",
            bootstyle=WARNING  # 变为橙色，更醒目
        )
        
        # 清空输出
        self.clear_output()
        
        # 在用户选择的路径中创建 Manifest ID 文件夹
        manifest_id = self.manifest_id_var.get()
        base_path = self.output_path_var.get()
        download_path = os.path.join(base_path, manifest_id)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            self.output_text.insert(END, f"✓ 已创建下载目录：{download_path}\n")
        except Exception as e:
            self.output_text.insert(END, f"✗ 创建目录失败：{e}\n")
            messagebox.showerror("错误", f"无法创建下载目录：{e}")
            self.download_btn.config(
                state=NORMAL, 
                text="⬇️ 开始下载",
                bootstyle=WARNING  # 恢复橙色
            )
            self.is_running = False
            return
        
        # 构建命令
        cmd = [
            self.depotdownloader_path,
            "download_depot",
            "-username", self.username_var.get(),
            "-password", self.password_var.get(),
            "-app", self.app_id_var.get(),
            "-depot", self.depot_id_var.get(),
            "-manifest", self.manifest_id_var.get(),
            "-dir", download_path
        ]
        
        if self.no_mobile_auth_var.get():
            cmd.append("-no-mobile")
        
        # 显示命令（隐藏密码）
        safe_cmd = cmd.copy()
        # 找到 -password 参数的位置，将其值替换为 ****
        try:
            password_index = safe_cmd.index("-password")
            if password_index + 1 < len(safe_cmd):
                safe_cmd[password_index + 1] = "****"
        except (ValueError, IndexError):
            pass
        
        self.output_text.insert(END, f"执行命令：{' '.join(safe_cmd)}\n")
        self.output_text.insert(END, "=" * 80 + "\n\n")
        
        # 启动进程
        def run_process():
            try:
                # 创建启动信息，隐藏控制台窗口
                startupinfo = None
                if sys.platform == 'win32':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    startupinfo=startupinfo
                )
                
                # 读取输出
                for line in self.process.stdout:
                    if self.output_text:
                        self.root.after(0, lambda l=line: self.output_text.insert(END, l))
                    self.root.after(0, lambda: self.output_text.see(END))
                
                # 等待完成
                self.process.wait()
                
                # 更新 UI
                self.root.after(0, self.on_download_complete)
                
            except Exception as e:
                self.root.after(0, lambda: self.on_download_error(str(e)))
        
        # 在新线程中运行
        thread = threading.Thread(target=run_process, daemon=True)
        thread.start()
    
    def validate_inputs(self):
        """验证输入"""
        if not self.username_var.get():
            messagebox.showerror("错误", "请输入用户名")
            return False
        
        if not self.password_var.get():
            messagebox.showerror("错误", "请输入密码")
            return False
        
        if not self.app_id_var.get():
            messagebox.showerror("错误", "请输入 App ID")
            return False
        
        if not self.depot_id_var.get():
            messagebox.showerror("错误", "请输入 Depot ID")
            return False
        
        if not self.manifest_id_var.get():
            messagebox.showerror("错误", "请输入 Manifest ID")
            return False
        
        if not self.output_path_var.get():
            messagebox.showerror("错误", "请选择输出目录")
            return False
        
        return True
    
    def on_download_complete(self):
        """下载完成"""
        # 恢复下载按钮
        self.download_btn.config(
            state=NORMAL, 
            text="⬇️ 开始下载",
            bootstyle=WARNING  # 恢复橙色
        )
        self.is_running = False
        
        if self.process and self.process.returncode == 0:
            self.output_text.insert(END, "\n" + "=" * 80 + "\n")
            self.output_text.insert(END, "✓ 下载完成！\n", "success")
            messagebox.showinfo("成功", "下载完成！")
        else:
            self.output_text.insert(END, "\n" + "=" * 80 + "\n")
            self.output_text.insert(END, f"✗ 下载失败，退出码：{self.process.returncode if self.process else '未知'}\n", "error")
            messagebox.showwarning("警告", f"下载失败，退出码：{self.process.returncode if self.process else '未知'}")
    
    def on_download_error(self, error):
        """下载错误"""
        # 恢复下载按钮
        self.download_btn.config(
            state=NORMAL, 
            text="⬇️ 开始下载",
            bootstyle=WARNING  # 恢复橙色
        )
        self.is_running = False
        self.output_text.insert(END, f"\n错误：{error}\n", "error")
        messagebox.showerror("错误", f"下载失败：{error}")
    
    def show_settings(self):
        """显示设置"""
        settings_window = ttkb.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("500x400")
        
        frame = ttkb.Frame(settings_window, padding=20)
        frame.pack(fill=BOTH, expand=YES)
        
        ttkb.Label(frame, text="设置", font=("Arial", 16, "bold")).pack(pady=10)
        
        # DepotDownloader 路径
        path_frame = ttkb.Frame(frame)
        path_frame.pack(fill=X, pady=10)
        
        ttkb.Label(path_frame, text="DepotDownloader 路径:").pack(anchor=W)
        path_entry = ttkb.Entry(path_frame, width=60)
        path_entry.pack(fill=X, pady=5)
        path_entry.insert(0, self.depotdownloader_path)
        
        def save_path():
            self.depotdownloader_path = path_entry.get()
            settings_window.destroy()
        
        ttkb.Button(
            path_frame,
            text="保存",
            command=save_path,
            bootstyle=PRIMARY
        ).pack(pady=10)
    
    def on_closing(self):
        """窗口关闭事件"""
        if self.is_running:
            if messagebox.askokcancel("确认", "下载正在进行中，确定要退出吗？"):
                if self.process:
                    self.process.terminate()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """运行程序"""
        
        # 检查更新（在独立线程中执行，避免阻塞UI）
        try:
            threading.Thread(target=lambda: update_checker.check_updates(tool_name, local_version), daemon=True).start()
        except Exception as e:
            print(f"启动更新检查线程失败: {e}")

        
        self.root.mainloop()


if __name__ == "__main__":
    app = SteamDepotDownloaderGUI()
    app.run()
