import subprocess
import shlex
from langchain_core.tools import tool

ALLOWED_COMMANDS = ["ls", "cat", "grep", "head", "tail", "wc", "echo"]

@tool
def bash_tool(command: str) -> str:
    """Execute a safe bash command."""
    # 1. 解析命令和参数
    parts = shlex.split(command)
    if not parts:
        return "空命令"
    
    # 2. 白名单检查
    base_cmd = parts[0]
    if base_cmd not in ALLOWED_COMMANDS:
        return f"不允许的命令: {base_cmd}。允许的命令: {', '.join(ALLOWED_COMMANDS)}"
    
    # 3. 禁止重定向和管道
    dangerous_chars = ['|', '&', ';', '>', '<', '`', '$', '(', ')']
    if any(char in command for char in dangerous_chars):
        return f"检测到危险字符，命令被拒绝"
    
    # 4. 使用列表形式执行（shell=False）
    try:
        result = subprocess.run(
            parts,
            capture_output=True,
            text=True,
            timeout=30  # 增加超时保护
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return "命令执行超时（30秒）"
    except Exception as e:
        return f"执行失败: {str(e)}"