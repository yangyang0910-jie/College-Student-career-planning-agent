from fastapi import UploadFile
from common.ResponseCommon import error, success
from userprofile.dao.ProfileDao import StudentProfileDao
from userprofile.util.ProfileModelUtil import profile_model
from userprofile.util.ProfileProcessorUtil import profileprocessor
from userprofile.util.ParsePDFUtil import parse_pdf
class ProfileService:
    # 用户自己输入介绍生成用户画像
    @staticmethod
    def ai_pro(raw_text:str,user_id:int)->dict:
        try:
            # 调用LLM分析
            data = profile_model(raw_text)
            result = profileprocessor(data)
            source="manual"
            res = StudentProfileDao.save(user_id,raw_text,result,source)
            return res
        except Exception as e:
            print("画像生成失败:", e)
            return error("画像生成失败")
    # 查询用户是否有用户画像---前端用于返回显示
    @staticmethod
    def query_pro(user_id:int)->dict:
        try:
            result = StudentProfileDao.query(user_id)
            return result
        except Exception as e:
            return error("画像查询失败")
    # 用户上传PDF简历生成用户画像
    @staticmethod
    def upload_pdf(file:UploadFile, user_id: int) -> dict:
            # 校验类型：是否是pdf
            if not file.filename.lower().endswith(".pdf"):
                return error("仅支持PDF格式简历")
            # 存临时文件
            import os, uuid
            tmp = f"tmp_{uuid.uuid4().hex}.pdf"
            with open(tmp, "wb") as f:
                f.write(file.file.read())
            try:
                # 解析文字
                raw_text = parse_pdf(tmp)
            finally:
                if tmp and os.path.exists(tmp):
                    os.remove(tmp)  # 用完即删
            # 当如果是扫描版或者图片型PDF提不出文字时
            if len(raw_text) < 50:
                return error("简历内容过少，可能是扫描版PDF，请改用手动录入")
            try:
                data = profile_model(raw_text)
                result = profileprocessor(data)
                source = "resume"
                res = StudentProfileDao.save(user_id, raw_text, result,source)
                return res
            except Exception as e:
                print("画像生成失败:", e)
                return error("画像生成失败")

if __name__ == '__main__':
    s=ProfileService.query_pro(7)
    print(s)