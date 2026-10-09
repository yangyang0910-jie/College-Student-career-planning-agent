import json
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import GraphRecursionError
from agent.state.CareerState import CareerState
from agent.nodes.LoadBaseNode import load_base_node
from agent.nodes.LoadStudentNode import load_student_node
from agent.nodes.LoadJobNode import load_job_node
from agent.nodes.JobMapNode import load_job_map_node
from agent.nodes.MatchNode import match_node
from agent.nodes.RagNode import rag_node
from agent.nodes.ReportNode import get_report_node


def build_career_graph():
    builder = StateGraph(CareerState)
    builder.add_node("load_base", load_base_node)
    builder.add_node("load_student", load_student_node)
    builder.add_node("load_job", load_job_node)
    builder.add_node("load_job_map", load_job_map_node)
    builder.add_node("match", match_node)
    builder.add_node("rag", rag_node)
    builder.add_node("gen_report", get_report_node)

    builder.add_edge(START, "load_base")
    builder.add_edge("load_base", "load_student")
    builder.add_edge("load_student", "load_job")
    builder.add_edge("load_job", "load_job_map")
    builder.add_edge("load_job_map", "match")
    builder.add_edge("match", "rag")
    builder.add_edge("rag", "gen_report")
    builder.add_edge("gen_report", END)
    return builder.compile(checkpointer=MemorySaver())
async def stream_career_graph(user_id: int, target_position: str = None) :
    graph = build_career_graph()
    config = {
        "configurable": {"thread_id": f"career_{user_id}"},
        "recursion_limit": 25, #防止图无限循环
    }
    init = {"user_id": user_id}
    if target_position:
        init["target_position"] = target_position
    full= []
    try:
        async for mode, chunk in graph.astream(init, config, stream_mode=["messages"]):
            if mode == "messages":
                msg, _ = chunk
                piece = msg.content or ""
                if piece:
                    full.append(piece)
                    yield f"data: {json.dumps({'delta': piece}, ensure_ascii=False)}\n\n"
    except GraphRecursionError:
        yield f"data: {json.dumps({'error': '流程步数超限，请重试'}, ensure_ascii=False)}\n\n"
        return
    except Exception as e:
        print(f"流式生成异常: {e}")
        yield f"data: {json.dumps({'error': f'生成失败:{e}'}, ensure_ascii=False)}\n\n"
        return
    report = "".join(full).strip()
    if not report:
        yield f"data: {json.dumps({'error': '报告生成为空，请重试'}, ensure_ascii=False)}\n\n"
        return
    # 结束标识
    yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"

def draw():
    graph = build_career_graph()
    data = graph.get_graph().draw_mermaid_png()
    with open("111.png", "wb") as f:
        f.write(data)

if __name__ == '__main__':
    draw()