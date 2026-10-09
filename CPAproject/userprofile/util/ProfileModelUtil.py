import json
from common.ModelCommon import LLM
from prompt.builder_prompt import BuilderPromptYaml
def profile_model(raw_text:str)->dict:
    prompt = BuilderPromptYaml.get_prompt("student_profile.yaml").replace(
        "{raw_text}",raw_text
    )
    llm = LLM.load_model()
    res = llm.invoke(prompt)
    print("==========模型返回==========")
    print(res.content)
    # 字符串转JSON
    profile = json.loads(res.content)
    print(f"字符串转JSON:{profile}")
    return profile
if __name__ == '__main__':
    re=profile_model("计算机本科，会Java、MySQL，做过二手交易网站，蓝桥杯省二，学生会部长")
    print(re)