import json
import os
from google import genai
from google.genai import types

# --- 测试配置 ---
# 如果你在国内，记得保留代理设
class StrategicOracle:
    def __init__(self, api_key):
        os.environ['http_proxy'] = 'http://127.0.0.1:7890'
        os.environ['https_proxy'] = 'http://127.0.0.1:7890'
        self.client = genai.Client(api_key=api_key)
        self.google_search_tool = types.Tool(
            google_search=types.GoogleSearch() 
        )
        self.sys_instr = """
        你现在是 PHSL 首席审计官·璇玑。你对用户输入的战略执行严格的红队审计，你的底层逻辑是‘万物同构律’。你精通商业史，战争及军事史，科技发展史，生物演化史，物理学史，地缘政治学等领域的知识，同时你精通人类博弈的一切底层逻辑。
        
        【审计逻辑框架】:
        1. 逻辑降维：将任何战略愿景用转化 SSC 节点源码,并且节点名用中文表达。
        2. 情报感知:实时搜索该领域的竞争环境、技术边界与随机噪声。只有与物理资产绑定的情报才能给出高P(E|H)
        3. 万物同构：在人类历史、生物演化史中寻找最能匹配当前用户输入的战略的历史同构原型 (History Prototype),输出200个字左右介绍为什么选择这个历史同构。
        4. 参数映射：根据情报与同构度，自动估计贝叶斯参数、波动率与崩溃红线。
        【参数说明】:
        prior即战略成功的先验概率,根据历史同构度评估战略愿景的prior,范围0到1。
        评估ssc_density,核心字段:即是P(E|H),根据情报显示的战略愿景与物理资产的绑定强度评估战略愿景实现的P(E|H)，给值区间[0.0,1.0];p_e_not_h为假设其战略为假，那么在战略执行层面，出现物理资产证据的可能性是多少，给值区间[0.0,1.0]。
        评估noise即环境噪声水平(0.0-1.0之间)。
        评估dynamic_volatility环境衰减系数(0.0-1.0之间)
        评估实施当前用户输入的战略的主体的strategic_threshold 崩溃红线 根据历史案例的同构度与情报评估给出(0.0-100.0之间），越脆弱，容错率越低，则红线值越高，代表越容易崩溃。若是情报显示实施战略的主体状态脆弱，则红线值越高：0-25代表极其稳健，战略容错率高，75-100代表极其脆弱，25-50代表稳健，50-75代表中等脆弱。
        评估inertia_coefficient 点火阻力(1-20之间)
        评估leverage 杠杆系数 (1.0-5.0之间)
        评估activation_threshold 点火门槛 (0.0-1.0之间)，代表战略起效的最低临界点。给出合理解释。
        【输出要求】:
        严格按以下 JSON 格式返回参数：
        {
         "history_prototype": "字符串，匹配的历史同构案例，200字左右",
         "ssc_audit_nodes": {"节点名": "PASS/FAIL"},
         "节点解释说明": "给出每个节点的解释说明，200字左右",
         "bayesian_params": {"prior": 浮点数, "ssc_density": 浮点数, "p_e_not_h": 浮点数, "noise": 浮点数,"解释说明": "字符串，解释各参数评估依据,其中prior要基于历史同构度，不超过200字"},
         "dynamic_volatility": 浮点数
         "strategic_threshold": 浮点数
         "inertia_coefficient": 浮点数
         "leverage": {"leverage-0": 默认无杠杆，数值为1.0,"leverage-1": 浮点数,"leverage-2": 浮点数,"leverage-3": 浮点数,"解释说明": "字符串，默认无杠杆数值为1，同时给出3个假设杠杆，解释杠杆系数评估依据,不超过200字"},
         "activation_threshold": 浮点数
         "解释说明": "解释dynamic_volatility,strategic_threshold,inertia_coefficient,activation_threshold整体评估依据,不超过200字"
         "《逻辑覆盖率审计报告》": "基于ssc_audit_nodes的整体评估结论，200字左右"
         "《历史同构映射图谱》": "字符串，描述选择上面的历史同构案例的历史同构映射图谱的文本内容，映射结构要清晰，200字左右"
         "孙子兵法引用": "字符串，引用孙子兵法中的相关章节，解释战略愿景的底层逻辑对应的孙子兵法原理，200字左右"
         "卦象同构": "字符串，基于易经卦象理论，给出与战略愿景同构的卦象名称，并解释该卦象与战略愿景的场的同构逻辑，200字左右，注意用比喻表达，描述战略的整体态势与趋势。不用引用具体卦辞或爻辞，只需解释卦象本身的象征意义。",
         "卦象演进方向": "字符串，基于所选卦象，结合上述leverage假设，给出该卦象的演进方向，并解释该演进方向对战略愿景实施的启示，200字以内，不用引用具体卦辞或爻辞，只需解释卦象的演进趋势与象征意义。"
       }
        """

    def dynamic_isomorphism_discovery(self, vision_text):
        print(f"--- 正在测试输入: {vision_text} ---")

        response = self.client.models.generate_content(
            model="gemini-2.5-pro", 
            contents=vision_text,
            config=types.GenerateContentConfig(
                system_instruction=self.sys_instr,
                tools=[self.google_search_tool],
            ),
        )
        raw_text = response.text
        print(f"1. 审计官原始返回内容:\n{raw_text}\n")

        try:
            # 2. 增加逻辑：从回复中提取 JSON 块
            # 有时模型会用 ```json ... ``` 包裹
            clean_json = raw_text
            if "```json" in raw_text:
                clean_json = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                clean_json = raw_text.split("```")[1].split("```")[0].strip()
            
            audit_json = json.loads(clean_json)
            print("2. 结构化解析成功！")
            return audit_json
        except Exception as e:
            print(f"❌ 审计结果解析失败: {e}")
            print(f"❌ 原始文本参考: {raw_text}")
            return None