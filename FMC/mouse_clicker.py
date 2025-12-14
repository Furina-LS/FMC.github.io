import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
import sys
import os
import webbrowser
# 导入更底层的win32api库以实现更高的点击速度
import win32api
import win32con
import win32gui
# 优化pyautogui设置以减少延迟
pyautogui.PAUSE = 0  # 设置pyautogui操作间的延迟为0
pyautogui.FAILSAFE = False  # 禁用安全模式
from PIL import Image
import pystray
from pystray import MenuItem as item
from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener
from pynput.mouse import Button, Listener as MouseListener

class MouseClicker:
    def __init__(self):
        self.is_running = False
        self.click_thread = None
        self.clicks_per_second = 10
        # 热键设置
        self.hotkey = Key.f9  # 默认热键为F9
        self.hotkey_type = "keyboard"  # 默认热键类型为键盘键
        self.hotkey_name = "F9"
        self.is_setting_hotkey = False
        self.is_setting_mouse_hotkey = False
        self.root = tk.Tk()
        self.root.title("芙芙鼠标连点器")
        self.root.geometry("450x500")
        self.root.resizable(False, False)
        
        # 创建点击类型变量（必须在root窗口之后创建）
        self.click_type = tk.StringVar(value="left")  # 默认左键点击
        
        # 设置天蓝色背景
        self.bg_color = "#87CEEB"
        self.root.configure(bg=self.bg_color)
        
        # 窗口居中
        self.root.update_idletasks()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 设置窗口图标
        self.root.iconbitmap('D:\\FMC\\FMC.ico')
        
        # 设置任务栏图标
        try:
            # 获取窗口句柄
            hwnd = win32gui.FindWindow(None, "芙芙鼠标连点器")
            if hwnd:
                # 加载图标
                icon_path = 'D:\\FMC\\FMC.ico'
                hicon = win32gui.LoadImage(
                    None,  # 模块句柄，None表示加载独立图标
                    icon_path,  # 图标路径
                    win32con.IMAGE_ICON,  # 资源类型
                    0, 0,  # 宽度和高度，0表示使用资源默认值
                    win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE  # 加载选项
                )
                if hicon:
                    # 设置窗口图标
                    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)  # 小图标
                    win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)  # 大图标
        except Exception as e:
            pass  # 如果设置任务栏图标失败，不影响程序运行
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, width=450, height=500, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # 初始化组件
        self.create_widgets()
        self.setup_system_tray()
        self.setup_global_key_listener()
        
        # 窗口事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # 使用wm_state来监听最小化事件，而不是替换内置的iconify方法
        self.root.bind("<Unmap>", lambda event: self.on_minimize() if self.root.state() == 'iconic' else None)
        
    # 移除了背景图片加载功能
    
    def create_widgets(self):
        """创建UI组件"""
        self.setup_styles()
        
        # 标题
        ttk.Label(self.canvas, text="芙芙鼠标连点器", font=('Microsoft YaHei', 20, 'bold')).place(x=100, y=30)
        
        # 状态显示
        status_frame = ttk.Frame(self.canvas)
        status_frame.place(x=35, y=80, width=380, height=80)
        self.status_label = ttk.Label(status_frame, text="状态: 已停止", font=('Microsoft YaHei', 15, 'bold'), foreground="#e74c3c")
        self.status_label.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 点击类型选择（放在状态显示和频率调制之间）
        click_type_frame = ttk.Frame(self.canvas)
        click_type_frame.place(x=35, y=160, width=380, height=40)
        ttk.Label(click_type_frame, text="点击类型: ", font=('Microsoft YaHei', 12)).pack(side="left", padx=(20, 10), pady=5)
        ttk.Radiobutton(click_type_frame, text="左键点击", variable=self.click_type, value="left").pack(side="left", padx=(0, 20), pady=5)
        ttk.Radiobutton(click_type_frame, text="右键点击", variable=self.click_type, value="right").pack(side="left", pady=5)
        
        # 热键设置
        hotkey_frame = ttk.Frame(self.canvas)
        hotkey_frame.place(x=35, y=200, width=380, height=40)
        ttk.Label(hotkey_frame, text="开始/停止热键: ", font=('Microsoft YaHei', 12)).pack(side="left", padx=(20, 10), pady=5)
        self.hotkey_label = ttk.Label(hotkey_frame, text="F9", font=('Microsoft YaHei', 12, 'bold'), foreground="#4a90e2")
        self.hotkey_label.pack(side="left", padx=(0, 10), pady=5)
        self.set_hotkey_button = ttk.Button(hotkey_frame, text="设置热键", command=self.set_hotkey)
        self.set_hotkey_button.pack(side="left")
        
        # 控制面板
        control_frame = ttk.Frame(self.canvas)
        control_frame.place(x=35, y=250, width=380, height=150)
        
        # 滑块控件
        ttk.Label(control_frame, text="点击频率调整: ", font=('Microsoft YaHei', 14)).pack(anchor="w", padx=20, pady=(10, 5))
        self.click_rate_slider = ttk.Scale(control_frame, from_=1, to=5000, orient="horizontal", command=self.on_slider_change, length=320)
        self.click_rate_slider.set(self.clicks_per_second)
        self.click_rate_slider.pack(anchor="center", padx=20, pady=5)
        
        # 输入区域
        input_frame = ttk.Frame(control_frame)
        input_frame.pack(fill="x", padx=20, pady=5)
        ttk.Label(input_frame, text="自定义速度: ", font=('Microsoft YaHei', 12)).pack(side="left", padx=(0, 10))
        self.click_rate_input = ttk.Entry(input_frame, width=6, font=('Microsoft YaHei', 12))
        self.click_rate_input.insert(0, str(self.clicks_per_second))
        self.click_rate_input.pack(side="left", padx=(0, 10))
        ttk.Button(input_frame, text="应用", command=self.apply_click_rate).pack(side="left", padx=(0, 20))
        self.rate_label = ttk.Label(input_frame, text=f"当前: {self.clicks_per_second} 次/秒", font=('Microsoft YaHei', 12, 'bold'), foreground="#4a90e2")
        self.rate_label.pack(side="right")
        
        # 主按钮
        self.toggle_button = ttk.Button(self.canvas, text="按F9键开始/停止", command=self.toggle_clicking)
        self.toggle_button.place(x=100, y=400, width=250, height=50)
        
        # 连点器信息按钮
        self.info_button = ttk.Button(self.canvas, text="连点器信息", command=self.show_clicker_info)
        self.info_button.place(x=150, y=450, width=150, height=40)
    
    def on_slider_change(self, value):
        """滑块值变化时的回调函数"""
        self.clicks_per_second = int(float(value))
        if hasattr(self, 'rate_label'):
            self.rate_label.config(text=f"当前: {self.clicks_per_second} 次/秒")
        if hasattr(self, 'click_rate_input'):
            self.click_rate_input.delete(0, tk.END)
            self.click_rate_input.insert(0, str(self.clicks_per_second))
    
    def apply_click_rate(self):
        """应用输入的点击速度（每秒点击次数，最高5000次/秒）"""
        if not hasattr(self, 'click_rate_input'):
            return
        input_text = self.click_rate_input.get().strip()
        try:
            new_rate = int(input_text)
            if new_rate > 0:
                # 限制最高点击速度为每秒5000次
                self.clicks_per_second = min(5000, new_rate)
                if hasattr(self, 'click_rate_slider'):
                    self.click_rate_slider.set(self.clicks_per_second)
                if hasattr(self, 'rate_label'):
                    self.rate_label.config(text=f"当前: {self.clicks_per_second} 次/秒")
                # 如果输入值超过5000，更新输入框显示实际应用的值
                if new_rate > 5000:
                    self.click_rate_input.delete(0, tk.END)
                    self.click_rate_input.insert(0, str(self.clicks_per_second))
                self.click_rate_input.focus()
            else:
                messagebox.showerror("输入错误", "点击速度必须大于0")
                self.click_rate_input.delete(0, tk.END)
                self.click_rate_input.insert(0, str(self.clicks_per_second))
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
            self.click_rate_input.delete(0, tk.END)
            self.click_rate_input.insert(0, str(self.clicks_per_second))
    
    def setup_system_tray(self):
        """设置系统托盘"""
        try:
            # 使用指定的ICO文件作为系统托盘图标
            icon_path = r'D:\FMC\FMC.ico'
            
            # 检查文件是否存在
            if os.path.exists(icon_path):
                try:
                    icon = Image.open(icon_path)
                except Exception:
                    # 如果ICO文件无法打开，使用默认图标
                    icon = Image.new('RGB', (64, 64), color="#4a90e2")
            else:
                # 如果文件不存在，使用默认图标
                icon = Image.new('RGB', (64, 64), color="#4a90e2")
            
            # 创建菜单
            menu = (item('显示窗口', self.show_window), item('退出程序', self.quit_program))
            
            # 创建系统托盘图标
            self.tray_icon = pystray.Icon("mouse_clicker", icon, "鼠标连点器", menu)
            
            # 启动系统托盘线程
            def run_tray_icon():
                try:
                    self.tray_icon.run()
                except Exception as e:
                    print(f"系统托盘错误: {e}")
            
            threading.Thread(target=run_tray_icon, daemon=True).start()
            
        except Exception as e:
            print(f"设置系统托盘时发生错误: {e}")
            pass
    
    def set_hotkey(self):
        """设置热键"""
        self.is_setting_hotkey = True
        self.is_setting_mouse_hotkey = True
        self.hotkey_label.config(text="等待按键...", foreground="#e74c3c")
        self.set_hotkey_button.config(text="取消设置", command=self.cancel_set_hotkey)
        
    def cancel_set_hotkey(self):
        """取消设置热键"""
        self.is_setting_hotkey = False
        self.is_setting_mouse_hotkey = False
        self.hotkey_label.config(text=self.hotkey_name, foreground="#4a90e2")
        self.set_hotkey_button.config(text="设置热键", command=self.set_hotkey)
    
    def update_hotkey_ui(self):
        """更新热键相关的UI元素"""
        self.hotkey_label.config(text=self.hotkey_name, foreground="#4a90e2")
        self.toggle_button.config(text=f"按{self.hotkey_name}键开始/停止")
        self.set_hotkey_button.config(text="设置热键", command=self.set_hotkey)
        self.is_setting_hotkey = False
        self.is_setting_mouse_hotkey = False
    
    def toggle_click_type(self):
        """切换点击类型（左键/右键）"""
        current_type = self.click_type.get()
        new_type = "right" if current_type == "left" else "left"
        self.click_type.set(new_type)
        
    def setup_global_key_listener(self):
        """设置全局键盘和鼠标监听"""
        def on_key_press(key):
            """键盘按下事件"""
            if self.is_setting_hotkey:
                # 设置新热键
                self.hotkey = key
                self.hotkey_type = "keyboard"
                # 转换键名格式
                try:
                    self.hotkey_name = key.char.upper() if hasattr(key, 'char') and key.char else str(key).replace('Key.', '').upper()
                except:
                    self.hotkey_name = str(key).replace('Key.', '').upper()
                self.update_hotkey_ui()
            elif self.hotkey_type == "keyboard" and key == self.hotkey:
                self.toggle_clicking()
            elif key == Key.alt_l:
                self.toggle_click_type()
        
        def on_mouse_press(x, y, button, pressed):
            """鼠标按下事件"""
            if pressed and self.is_setting_mouse_hotkey:
                # 设置新的鼠标热键
                self.hotkey = button
                self.hotkey_type = "mouse"
                # 转换键名格式
                if button == Button.left:
                    self.hotkey_name = "鼠标左键"
                elif button == Button.right:
                    self.hotkey_name = "鼠标右键"
                elif button == Button.middle:
                    self.hotkey_name = "鼠标中键"
                else:
                    self.hotkey_name = str(button).replace('Button.', '')
                self.update_hotkey_ui()
            elif pressed and self.hotkey_type == "mouse" and button == self.hotkey:
                self.toggle_clicking()
        
        # 启动全局键盘监听线程
        threading.Thread(target=lambda: Listener(on_press=on_key_press).start(), daemon=True).start()
        
        # 启动全局鼠标监听线程
        threading.Thread(target=lambda: MouseListener(on_click=on_mouse_press).start(), daemon=True).start()
    
    def toggle_clicking(self):
        """切换点击状态"""
        self.stop_clicking() if self.is_running else self.start_clicking()
    
    def start_clicking(self):
        """开始点击"""
        if self.is_running:
            return
        self.is_running = True
        self.status_label.config(text="状态: 运行中", foreground="green")
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()
    
    def click_loop(self):
        """点击循环，使用win32api实现更高的点击速度"""
        try:
            while self.is_running:
                # 获取当前设置的点击速度
                current_clicks_per_second = self.clicks_per_second
                
                # 确定使用的点击方法
                if self.click_type.get() == "left":
                    click_event = win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP
                else:
                    click_event = win32con.MOUSEEVENTF_RIGHTDOWN | win32con.MOUSEEVENTF_RIGHTUP
                
                # 如果速度较低，使用单点击模式
                if current_clicks_per_second <= 500:
                    interval = 1.0 / current_clicks_per_second
                    start_time = time.perf_counter()
                    
                    # 使用win32api执行点击
                    win32api.mouse_event(click_event, 0, 0, 0, 0)
                    
                    # 计算等待时间
                    click_duration = time.perf_counter() - start_time
                    sleep_time = interval - click_duration
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                # 如果速度较高，使用批量点击模式
                else:
                    # 每次处理500个点击，减少循环开销
                    batch_size = 500
                    batch_interval = batch_size / current_clicks_per_second
                    batch_start_time = time.perf_counter()
                    
                    for _ in range(batch_size):
                        if not self.is_running:
                            break
                        # 使用win32api执行点击
                        win32api.mouse_event(click_event, 0, 0, 0, 0)
                    
                    # 计算批量处理耗时
                    batch_duration = time.perf_counter() - batch_start_time
                    sleep_time = batch_interval - batch_duration
                    if sleep_time > 0:
                        time.sleep(sleep_time)
        except Exception as e:
            print(f"点击循环错误: {e}")
            self.is_running = False
            self.update_ui_status()
    
    def stop_clicking(self):
        """停止点击"""
        self.is_running = False
        self.update_ui_status()
    
    def setup_styles(self):
        """设置ttk样式"""
        style = ttk.Style()
        for widget in ["TFrame", "TLabel", "TButton", "TEntry", "TScale", "TRadiobutton"]:
            style.configure(widget, background=self.bg_color, foreground="black")
        style.configure("TButton", padding=5)
        style.map("TButton", background=[('active', '#4a90e2')], foreground=[('active', 'white')])
    
    def update_ui_status(self):
        """更新UI状态"""
        if self.is_running:
            self.status_label.config(text="状态: 运行中", foreground="#2ecc71")
        else:
            self.status_label.config(text="状态: 已停止", foreground="#e74c3c")
    
    def on_close(self):
        """窗口关闭事件"""
        self.stop_clicking()
        self.quit_program()
    
    def on_minimize(self):
        """窗口最小化"""
        self.root.withdraw()
    
    def show_window(self):
        """显示窗口"""
        self.root.deiconify()
        self.root.lift()
    
    def quit_program(self):
        """退出程序"""
        self.stop_clicking()
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.root.destroy()
        sys.exit()
    
    def show_clicker_info(self):
        """显示连点器信息，打开指定网页"""
        webbrowser.open("https://furina-ls.github.io/")
    
    def run(self):
        """运行程序"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MouseClicker()
    app.run()