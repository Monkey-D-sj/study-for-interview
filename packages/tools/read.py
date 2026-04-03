import os
from pathlib import Path
from langchain_core.tools import tool

# 配置允许读取的目录（根据你的项目调整）
ALLOWED_PATHS = [
    Path.cwd(),  # 当前工作目录
    Path.home() / "Documents" / "resumes",  # 指定简历目录
    Path("/tmp"),  # 临时文件目录
]

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'.txt', '.md', '.json', '.pdf', '.docx'}

@tool
def read_file(file_path: str) -> str:
    """
    Read content from a file safely.
    
    Args:
        file_path: Path to the file (relative or absolute)
    
    Returns:
        File content or error message
    """
    try:
        # 1. 规范化路径（解析..和符号链接）
        target = Path(file_path).resolve()
        
        # 2. 检查是否在允许的目录内
        is_allowed = any(
            target.is_relative_to(allowed_path.resolve())
            for allowed_path in ALLOWED_PATHS
        )
        
        if not is_allowed:
            return f"错误：无权访问 {file_path}。允许的目录: {', '.join(str(p) for p in ALLOWED_PATHS)}"
        
        # 3. 检查文件是否存在
        if not target.exists():
            return f"错误：文件不存在 {file_path}"
        
        # 4. 检查是否为文件（而非目录）
        if not target.is_file():
            return f"错误：{file_path} 是一个目录"
        
        # 5. 检查扩展名（可选）
        if target.suffix.lower() not in ALLOWED_EXTENSIONS:
            return f"警告：文件类型 {target.suffix} 可能无法以纯文本形式读取"
        
        # 6. 检查文件大小（防止读取过大文件）
        file_size = target.stat().st_size
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            return f"错误：文件过大 ({file_size / 1024 / 1024:.1f}MB)，最大支持 {max_size / 1024 / 1024}MB"
        
        # 7. 尝试以不同编码读取
        encodings = ['utf-8', 'gbk', 'latin-1']
        for encoding in encodings:
            try:
                content = target.read_text(encoding=encoding)
                return content
            except UnicodeDecodeError:
                continue
        
        return "错误：无法解码文件，请确保是文本文件"
        
    except Exception as e:
        return f"读取失败: {str(e)}"