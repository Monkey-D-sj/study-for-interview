# 第一阶段：依赖安装（利用缓存）
FROM python:3.13-slim as builder

WORKDIR /app

# 复制依赖文件
COPY backend/requirements.txt .

# 安装依赖到临时目录
RUN pip install --user --no-cache-dir -r requirements.txt

# 第二阶段：运行环境
FROM python:3.13-slim

WORKDIR /app

# 从 builder 复制已安装的依赖到全局位置
COPY --from=builder /root/.local /usr/local

# 复制应用代码
COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY data/ ./data/

# 创建数据目录并设置权限
RUN mkdir -p /app/data/db && \
    chmod -R 755 /app/data && \
    chmod +x /app/scripts/*.py

# 确保 PATH 包含全局安装的包
ENV PATH=/usr/local/bin:$PATH

# 暴露端口
EXPOSE 8000

# 健康检查
#HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]