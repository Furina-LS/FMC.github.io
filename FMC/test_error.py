import subprocess
import sys

# 运行鼠标连点器程序并捕获输出
try:
    result = subprocess.run(
        [sys.executable, "mouse_clicker.py"],
        capture_output=True,
        text=True,
        timeout=5  # 设置5秒超时
    )
    
    print("=== 标准输出 ===")
    print(result.stdout)
    
    print("\n=== 错误输出 ===")
    print(result.stderr)
    
    print(f"\n=== 退出码 ===")
    print(result.returncode)
    
except subprocess.TimeoutExpired:
    print("程序运行超时")
except Exception as e:
    print(f"捕获到异常: {e}")