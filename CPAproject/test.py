# # 清理岗位数据
# import pandas as pd
# # =========================
# # 1. 读取数据
# # =========================
# path = r"D:\workspace\CPAproject\岗位数据.xls"
# df = pd.read_excel(path)
# print("原始数据量：", len(df))
# # =========================
# # 2. 第一次去重
# # 完全相同的记录去重
# # =========================
# df = df.drop_duplicates()
# print("完全去重后：", len(df))
# # =========================
# # 3. 第二次去重
# # 岗位名称 + 岗位详情相同的数据去重
# # =========================
# df = df.drop_duplicates(
#     subset=["岗位名称", "岗位详情"]
# )
# print("岗位名称+岗位详情去重后：", len(df))
# # =========================
# # 4. 检查关键字段是否为空
# # =========================
# print("\n岗位名称为空：", df["岗位名称"].isna().sum())
# print("岗位详情为空：", df["岗位详情"].isna().sum())
# # =========================
# # 5. 去掉岗位详情为空的数据
# # 用于后面的岗位画像分析
# # =========================
# profile_df = df.dropna(
#     subset=["岗位详情"]
# ).copy()
#
# print("\n用于岗位画像分析的数据量：", len(profile_df))
# # =========================
# # 6. 统计每个岗位的数量
# # =========================
# job_count = profile_df["岗位名称"].value_counts()
# # =========================
# # 7. 输出岗位种类数量
# # =========================
# print("\n岗位种类数量：", len(job_count))
# # =========================
# # 8. 输出每个岗位的数量
# # =========================
# print("\n每个岗位剩余数量：")
# print(job_count)
# # =========================
# # 9. 输出前10个岗位
# # =========================
# print("\n岗位数量前10：")
# print(job_count.head(10))


# from rag.service.RetrieveService import RagService
# def main():
#     question = "Java开发工程师需要掌握哪些技能？"
#     docs = RagService.retrieve(
#         question=question,
#         candidate_k=10,
#         top_k=5
#     )
#     print("\n================ 最终返回结果 ================\n")
#     if not docs:
#         print("没有检索到结果")
#         return
#     for index, doc in enumerate(docs, start=1):
#         print(f"【结果 {index}】")
#         print("岗位：", doc.metadata.get("job"))
#         print("来源：", doc.metadata.get("title"))
#         print("内容：")
#         print(doc.page_content)
#         print("-" * 80)
# if __name__ == "__main__":
#     main()

# from rag.tool.QueryTool import career_rag_search
# def main() -> None:
#     result = career_rag_search.invoke({
#         "question": "Java开发工程师需要掌握哪些技能？"
#     })
#
#     print(result)
#
#
# if __name__ == "__main__":
#     main()


from common.ModelCommon import LLM
model = LLM.load_model()
resp = model.invoke("你好")
print(resp)