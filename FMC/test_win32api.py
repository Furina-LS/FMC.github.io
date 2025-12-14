# 测试win32api是否可用

# 方法1: 尝试导入win32api
try:
    import win32api
    import win32con
    print("✓ win32api可用")
    print(f"win32api版本: {win32api.VERSION}")
    
    # 测试点击功能
    print("\n测试鼠标点击...")
    # 获取当前鼠标位置
    x, y = win32api.GetCursorPos()
    print(f"当前鼠标位置: ({x}, {y})")
    
    # 执行一次点击
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print("✓ 鼠标点击成功")
    
except ImportError as e:
    print(f"✗ win32api不可用: {e}")
    print("正在尝试重新安装pywin32...")
    
    # 方法2: 尝试使用ctypes调用Windows API
    print("\n尝试使用ctypes调用Windows API...")
    try:
        import ctypes
        from ctypes import wintypes
        
        # 加载user32.dll
        user32 = ctypes.WinDLL('user32')
        
        # 定义鼠标事件常量
        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004
        MOUSEEVENTF_RIGHTDOWN = 0x0008
        MOUSEEVENTF_RIGHTUP = 0x0010
        
        # 定义mouse_event函数
        user32.mouse_event.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.ULONG_PTR]
        user32.mouse_event.restype = None
        
        print("✓ ctypes调用Windows API可用")
        
        # 执行一次点击
        print("测试鼠标点击...")
        user32.mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, 0, 0, 0, None)
        print("✓ 鼠标点击成功")
        
    except Exception as e:
        print(f"✗ ctypes调用Windows API失败: {e}")
        print("无法使用更底层的方法实现点击")

except Exception as e:
    print(f"✗ 测试win32api时发生错误: {e}")