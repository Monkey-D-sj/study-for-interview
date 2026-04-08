"""
测试 base_ask_node 节点
"""

from unittest.mock import patch, MagicMock
from packages.agents.interview.sub_graphs.base_inspect.nodes.base_ask import base_ask_node
from packages.agents.interview.sub_graphs.base_inspect.state import BaseInspectState


def test_base_ask_node():
    print("=" * 60)
    print("测试 base_ask_node 节点")
    print("=" * 60)

    # Mock stream writer - 需要patch在导入位置
    with patch('packages.agents.interview.sub_graphs.base_inspect.nodes.base_ask.get_stream_writer') as mock_writer:
        mock_writer.return_value = lambda x: None

        # 测试场景1: 前端初级
        print("\n【测试1】前端初级岗位")
        print("-" * 60)
        state: BaseInspectState = {
            "position": "frontend",
            "level": "junior",
            "results": [],
            "passed_question_count": 0,
            "used_question_ids": [],
            "is_passed": False,
        }
        result = base_ask_node(state)
        print(f"返回结果: {result}")
        print(f"问题ID: {result['results'][0]['id']}")
        print(f"问题内容: {result['results'][0]['question']}")
        print(f"标准答案: {result['results'][0]['standard_answer']}")
        print(f"已出题ID: {result['used_question_ids']}")

        # 测试场景2: 后端初级
        print("\n【测试2】后端初级岗位")
        print("-" * 60)
        state: BaseInspectState = {
            "position": "backend",
            "level": "junior",
            "results": [],
            "passed_question_count": 0,
            "used_question_ids": [],
            "is_passed": False,
        }
        result = base_ask_node(state)
        print(f"返回结果: {result}")
        print(f"问题ID: {result['results'][0]['id']}")
        print(f"问题内容: {result['results'][0]['question']}")
        print(f"标准答案: {result['results'][0]['standard_answer']}")
        print(f"已出题ID: {result['used_question_ids']}")

        # 测试场景3: 测试去重功能
        print("\n【测试3】测试去重功能")
        print("-" * 60)
        first_question_id = None

        # 第一次抽取
        state: BaseInspectState = {
            "position": "frontend",
            "level": "junior",
            "results": [],
            "passed_question_count": 0,
            "used_question_ids": [],
            "is_passed": False,
        }
        result1 = base_ask_node(state)
        first_question_id = result1['results'][0]['id']
        print(f"第一题ID: {first_question_id}")

        # 第二次抽取（排除第一题）
        state: BaseInspectState = {
            "position": "frontend",
            "level": "junior",
            "results": [],
            "passed_question_count": 0,
            "used_question_ids": [first_question_id],
            "is_passed": False,
        }
        result2 = base_ask_node(state)
        second_question_id = result2['results'][0]['id']
        print(f"第二题ID: {second_question_id}")

        if first_question_id != second_question_id:
            print("[PASS] 去重功能正常")
        else:
            print("[FAIL] 去重功能异常")

        # 测试场景4: 高级职级
        print("\n【测试4】前端高级岗位")
        print("-" * 60)
        state: BaseInspectState = {
            "position": "frontend",
            "level": "senior",
            "results": [],
            "passed_question_count": 0,
            "used_question_ids": [],
            "is_passed": False,
        }
        result = base_ask_node(state)
        print(f"返回结果: {result}")
        print(f"问题ID: {result['results'][0]['id']}")
        print(f"问题内容: {result['results'][0]['question']}")
        print(f"标准答案: {result['results'][0]['standard_answer']}")

        # 测试场景5: 中文职级映射
        print("\n【测试5】中文职级映射（中级）")
        print("-" * 60)
        state: BaseInspectState = {
            "position": "前端",
            "level": "中级",
            "results": [],
            "passed_question_count": 0,
            "used_question_ids": [],
            "is_passed": False,
        }
        result = base_ask_node(state)
        print(f"返回结果: {result}")
        print(f"问题ID: {result['results'][0]['id']}")
        print(f"问题内容: {result['results'][0]['question']}")

    print("\n" + "=" * 60)
    print("所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_base_ask_node()
