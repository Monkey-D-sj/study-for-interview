from io import BytesIO
import fitz  # pymupdf

from packages.agents.resume.resume_agent import parse_resume
from apps.api.repositories.resume_repository import ResumeRepository


class PDFService:
    """PDF 处理服务"""

    @staticmethod
    def read_pdf(file_bytes: bytes) -> dict:
        """
        读取 PDF 文件内容

        Args:
            file_bytes: PDF 文件的字节内容

        Returns:
            dict: 包含 success, content, page_count, error 的字典
        """
        try:
            pdf_stream = BytesIO(file_bytes)
            doc = fitz.open(stream=pdf_stream, filetype="pdf")

            all_text = []
            for page in doc:
                text = page.get_text()
                if text.strip():
                    all_text.append(text)

            content = "\n\n".join(all_text)
            page_count = len(doc)
            doc.close()

            return {
                "success": True,
                "content": content,
                "page_count": page_count,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "content": None,
                "page_count": None,
                "error": str(e)
            }

    @staticmethod
    async def parse_and_save_resume(resume_content: str, session) -> dict:
        """
        解析并保存简历内容

        Args:
            resume_content: 简历文本内容
            session: 数据库会话

        Returns:
            dict: 包含 success, data, error 的字典
        """
        try:
            # 解析简历
            parsed_data = parse_resume(resume_content)

            # 保存到数据库
            resume = await ResumeRepository.save_resume(session, parsed_data)

            return {
                "success": True,
                "data": parsed_data,
                "resume_id": resume.id,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "resume_id": None,
                "error": str(e)
            }
