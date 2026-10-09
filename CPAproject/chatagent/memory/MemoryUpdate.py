from langchain_core.language_models.chat_models import BaseChatModel
from chatagent.memory.SimpleMemory import SimpleMemory

def update_memory(memory: SimpleMemory, model: BaseChatModel, question: str, answer: str) -> None:
    try:
        # LLM判断是否值得长期保存
        prompt = ("判断下面对话是否包含值得长期记住的信息"
                  f"（用户偏好/计划/技能/身份）。不值得只回答NONE，"
                  f"值得则只返回一句精炼记忆：\n用户：{question}\nAI：{answer[:200]}")
        result = model.invoke(prompt).content.strip()
        if result and result != "NONE":
            memory.add_long(result)
            print(f"[L3长期记忆] 已保存: {result}")

        # 窗口攒够4条未摘要的新增消息就增量摘要
        # 窗口只保留最近8条且会滑动，所以"还没摘要的条数" = 会话累计条数 - 已摘要条数，
        # 未摘要的消息在窗口尾部
        window = memory.load_window()
        done_count = memory.load_summarized_count()   # 累计已摘要到多少条
        total = memory.load_total_count()             # 会话累计消息条数
        unsummarized = total - done_count             # 还没摘要过的条数
        if unsummarized > 0:
            new_msgs = window[max(0, len(window) - unsummarized):]
            if len(new_msgs) >= 4:
                conv = "\n".join(f"{m['role']}：{m['content']}" for m in new_msgs)
                # 提取旧摘要与新的合并
                old_summary = memory.load_summary()
                sp = (f"历史摘要：{old_summary}\n新增对话：\n{conv}\n"
                      f"请合并生成新的摘要（300字内，第三人称）：")
                #新摘要
                summary = model.invoke(sp).content.strip()
                memory.save_summary(summary)
                memory.save_summarized_count(done_count + len(new_msgs))
                print(f"[摘要] 增量更新（新增{len(new_msgs)}条）")
    except Exception as e:
        print(f"记忆更新失败（不影响对话）: {e}")
