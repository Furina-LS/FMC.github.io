import time
import threading
import tkinter as tk
from tkinter import ttk
import win32api
import win32con

class ClickSpeedTester:
    def __init__(self, root):
        self.root = root
        self.root.title("点击速度测试工具")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 设置样式
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#87CEFA")
        self.style.configure("TLabel", background="#87CEFA", foreground="black")
        self.style.configure("TButton", background="#87CEFA", foreground="black", padding=5)
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建界面元素
        self.title_label = ttk.Label(self.main_frame, text="点击速度测试", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=10)
        
        self.instruction_label = ttk.Label(self.main_frame, text="点击开始按钮后，将鼠标移动到点击区域，程序将自动测量点击速度")
        self.instruction_label.pack(pady=10)
        
        self.status_label = ttk.Label(self.main_frame, text="就绪", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)
        
        self.result_label = ttk.Label(self.main_frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # 创建按钮
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(self.button_frame, text="开始测试", command=self.start_test)
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(self.button_frame, text="停止测试", command=self.stop_test, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        # 创建点击区域
        self.click_area = tk.Canvas(self.main_frame, width=200, height=100, bg="white", highlightthickness=2, highlightbackground="black")
        self.click_area.pack(pady=10)
        self.click_area.create_text(100, 50, text="点击区域", font=("Arial", 12))
        
        # 测试参数
        self.is_testing = False
        self.click_count = 0
        self.start_time = 0
        self.test_thread = None
    
    def start_test(self):
        self.is_testing = True
        self.click_count = 0
        self.start_time = time.time()
        
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="测试进行中...")
        self.result_label.config(text="")
        
        # 启动点击线程
        self.test_thread = threading.Thread(target=self.click_loop)
        self.test_thread.daemon = True
        self.test_thread.start()
        
        # 开始更新结果
        self.update_result()
    
    def stop_test(self):
        self.is_testing = False
        
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="测试已停止")
    
    def click_loop(self):
        while self.is_testing:
            # 使用win32api执行点击
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            self.click_count += 1
    
    def update_result(self):
        if self.is_testing:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            
            if elapsed_time > 0:
                click_speed = self.click_count / elapsed_time
                self.result_label.config(text=f"点击次数: {self.click_count}\n点击速度: {click_speed:.2f}次/秒")
            
            # 每秒更新一次
            self.root.after(1000, self.update_result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickSpeedTester(root)
    root.mainloop()