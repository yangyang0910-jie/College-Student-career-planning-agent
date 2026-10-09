from userprofile.dao import BaseInfoDao
from userprofile.entity.BaseInfoEntity import SaveEntity
from common.ResponseCommon import success
class InfoService:
    # 保存用户基础信息
    @staticmethod
    def save_info(saveinfoEntity: SaveEntity, user_id: int) -> dict:
        result = BaseInfoDao.info_save(saveinfoEntity, user_id)
        return result
    # 判断用户信息是否已存在
    @staticmethod
    def query_info(user_id: int) -> bool:
        result = BaseInfoDao.info_query(user_id)
        if result["code"]==200:
            return True
        return False
    # 查询用户信息
    @staticmethod
    def get_info(user_id: int) -> dict:
        result = BaseInfoDao.info_query(user_id)
        if result.get("code") != 200 or not result.get("data"):
            return {}
        data = result["data"]
        return {
            "name": data.get("name"),
            "education": data.get("education"),
            "major": data.get("major"),
            "school": data.get("school"),
            "graduation_date": data.get("graduation_date"),
            "city": data.get("city"),
            "job_direction": data.get("job_direction"),
        }
if __name__ == '__main__':
    re = InfoService.get_info(7)
    print(re)