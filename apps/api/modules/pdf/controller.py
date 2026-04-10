from fastapi import APIRouter, UploadFile, File, Depends

from apps.api.db.pg_client import pg_client
from .schema import PDFReadResponse, ResumeParseResponse
from .service import PDFService

pdf_router = APIRouter(
    prefix="/resume",
    tags=["resume"]
)


@pdf_router.post("/upload", response_model=ResumeParseResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    上传 PDF 文件并解析简历内容

    Args:
        file: PDF 文件

    Returns:
        ResumeParseResponse: 包含解析后的简历信息或错误信息
    """
    # 验证文件类型
    if not file.filename.lower().endswith('.pdf'):
        return ResumeParseResponse(
            success=False,
            error="请上传 PDF 文件"
        )

    # 读取文件内容
    file_bytes = await file.read()

    # 使用服务处理 PDF
    result = PDFService.read_pdf(file_bytes)

    if not result["success"]:
        return ResumeParseResponse(
            success=False,
            error=f"PDF 读取失败: {result['error']}"
        )

    # 解析简历并保存到数据库
    async with await pg_client.get_session() as session:
        parse_result = await PDFService.parse_and_save_resume(
            resume_content=result["content"],
            session=session
        )

    if not parse_result["success"]:
        return ResumeParseResponse(
            success=False,
            error=f"简历解析失败: {parse_result['error']}"
        )

    return ResumeParseResponse(
        success=True,
        data=parse_result["data"],
        resume_id=parse_result["resume_id"]
    )
