import time
import pyautogui

# 设置pyautogui参数
pyautogui.PAUSE = 0  # 移除点击之间的延迟
pyautogui.FAILSAFE = False  # 禁用安全模式

print("PyAutoGUI 点击速度测试")
print("设置: PAUSE = 0, FAILSAFE = False")
print("=" * 40)

# 测试1: 单次点击延迟
print("\n1. 单次点击延迟测试:")
total_time = 0
iterations = 1000

for i in range(iterations):
    start = time.perf_counter()
    pyautogui.click(button='left')
    end = time.perf_counter()
    total_time += (end - start)

avg_time = total_time / iterations
max_theoretical = 1 / avg_time if avg_time > 0 else float('inf')

print(f"   执行 {iterations} 次点击")
print(f"   总耗时: {total_time:.4f} 秒")
print(f"   平均每次点击耗时: {avg_time:.6f} 秒")
print(f"   理论最大点击速度: {max_theoretical:.2f} 次/秒")

# 测试2: 连续点击速度
print("\n2. 连续点击速度测试:")
start_time = time.perf_counter()
click_count = 0
test_duration = 3  # 测试3秒

while time.perf_counter() - start_time < test_duration:
    pyautogui.click(button='left')
    click_count += 1

end_time = time.perf_counter()
actual_duration = end_time - start_time
actual_speed = click_count / actual_duration

print(f"   测试时长: {actual_duration:.4f} 秒")
print(f"   点击次数: {click_count}")
print(f"   实际点击速度: {actual_speed:.2f} 次/秒")

print("\n测试完成！")