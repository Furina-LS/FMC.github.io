import time
import pyautogui

# 测试点击速度的函数
def click_speed_test():
    print("开始点击速度测试...")
    
    # 设置pyautogui参数
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
    
    # 测试不同的点击方式
    test_methods = [
        ("单点击模式", lambda: pyautogui.click(button='left')),
        ("批量点击模式", lambda: [pyautogui.click(button='left') for _ in range(100)])
    ]
    
    for method_name, click_method in test_methods:
        print(f"\n--- {method_name} ---")
        
        # 预热测试
        print("预热测试...")
        for _ in range(1000):
            click_method()
        
        # 正式测试
        print("正式测试...")
        start_time = time.perf_counter()
        total_clicks = 0
        
        # 测试时长（秒）
        test_duration = 2
        
        if method_name == "批量点击模式":
            # 批量点击模式
            batches = 0
            while time.perf_counter() - start_time < test_duration:
                click_method()  # 100次点击
                batches += 1
                total_clicks += 100
        else:
            # 单点击模式
            while time.perf_counter() - start_time < test_duration:
                click_method()
                total_clicks += 1
        
        end_time = time.perf_counter()
        actual_duration = end_time - start_time
        actual_speed = total_clicks / actual_duration
        
        print(f"测试结果：")
        print(f"持续时间：{actual_duration:.4f}秒")
        print(f"总点击次数：{total_clicks}")
        print(f"实际点击速度：{actual_speed:.2f}次/秒")

# 测试pyautogui的实际性能限制
def pyautogui_performance_test():
    print("\n--- PyAutoGUI性能测试 ---")
    
    # 测试pyautogui.click()的最小延迟
    pyautogui.PAUSE = 0
    
    iterations = 10000
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        pyautogui.click(button='left')
    
    end_time = time.perf_counter()
    total_duration = end_time - start_time
    avg_time_per_click = total_duration / iterations
    max_theoretical_speed = 1 / avg_time_per_click
    
    print(f"执行{iterations}次点击的总时间：{total_duration:.4f}秒")
    print(f"每次点击的平均时间：{avg_time_per_click:.6f}秒")
    print(f"PyAutoGUI的理论最大点击速度：{max_theoretical_speed:.2f}次/秒")

# 主函数
if __name__ == "__main__":
    click_speed_test()
    pyautogui_performance_test()
    print("\n测试完成！")