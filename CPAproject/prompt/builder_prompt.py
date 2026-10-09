import os
import textwrap
import yaml
class BuilderPromptYaml:
    @staticmethod
    def get_prompt(file_name: str) -> str:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, file_name)   # yaml和本文件同目录就保持这样
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                config: dict = yaml.safe_load(f)
        except FileNotFoundError:
            raise RuntimeError(f"提示词文件不存在: {file_path}")

        try:
            task_text = "\n".join(str(i) for i in config["task"])
            rule_text = "\n".join(str(i) for i in config["rule"])
            output_text = "\n".join(str(i) for i in config["output"])
            example_text = "\n".join(str(i) for i in config["example"])
        except KeyError as e:
            raise RuntimeError(f"提示词文件 {file_name} 缺少字段: {e}")

        return textwrap.dedent(f"""\
            一 角色：{config['role']}
            二 任务：
            {task_text}
            三 规则：
            {rule_text}
            四 输出：
            {output_text}
            五 示例：
            {example_text}
        """).strip()