import re
import pdfplumber
def clean_text(text: str) -> str:
    #清除PDF私有区符号和控制字符，避免GBK编码报错
    return re.sub(r'[\uE000-\uF8FF\u0000-\u0008\u000b-\u001f]', '', text or '')

def parse_pdf(file_path: str) -> str:
    #提取PDF全部文字
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"
    return clean_text(text.strip())