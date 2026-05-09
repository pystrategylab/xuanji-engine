import json
import time
import asyncio
import random
import numpy as np
from google import genai
from google.genai import types

class StrategicArena:
    def __init__(self, api_key, max_rounds=2):
        """
        璇玑多智能体对抗沙盘 (异步并发 + 战报封存版)
        """
        self.client = genai.Client(api_key=api_key)
        self.max_rounds = max_rounds
    # 👇 新增：防熔断的安全调用包装器
    # 在参数里加上 model_name，默认使用 flash
    def _safe_api_call(self, prompt, is_json=False, max_retries=3, model_name="gemini-2.5-flash"):
        """带有指数退避、强制冷却和多发引擎切换的安全调用"""
        for attempt in range(max_retries):
            try:
                # 即使是 Flash，也保留极其微小（0.5秒）的错峰，保证绝对稳定
                time.sleep(random.uniform(0.1, 0.5)) 
                
                if is_json:
                    config = types.GenerateContentConfig(response_mime_type="application/json")
                    response = self.client.models.generate_content(
                        model=model_name, # 👈 使用传入的模型
                        contents=prompt,
                        config=config
                    )
                else:
                    response = self.client.models.generate_content(
                        model=model_name, # 👈 使用传入的模型
                        contents=prompt
                    )
                return response.text
                
            except Exception as e:
                print(f"⚠️ API 遭到拦截/断联 (尝试 {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    sleep_time = 2 ** (attempt + 1)
                    print(f"⏳ 正在冷却引擎，等待 {sleep_time} 秒后重试...")
                    time.sleep(sleep_time)
                else:
                    raise Exception(f"🚨 彻底熔断!API 连续 {max_retries} 次调用失败。")
    def red_agent_turn(self, strategy,round_num,current_stability,context,leverage_desc="无特殊杠杆"):
        prompt = f"""
        你现在是以下战略的【绝对主导者与执行方】（第一人称视角）：
        核心战略设定：【{strategy}】
        🛡️ 核心底牌与物理装甲：【{leverage_desc}】
        
        📊 【系统遥测仪表盘】：
        - 当前交锋回合：第 {round_num} 回合
        - 当前组织稳定性（总体生命值）：{current_stability:.1f}% 
        
        ⚠️ 请严格按照以下两步逻辑进行思考和输出（总字数控制在 150 字以内）：
        
        【第一步：三维体征自检】(存量、增量与调动通道)
        蓝方正在对你进行攻击，你必须根据蓝方的攻击，极其冷酷地盘点你真实的资源现状。必须明确评估以下三个维度：
        1. 🛡️ 【物理存量】：我方的老本（如：资金、库存）还剩多少？
        2. 🩸 【造血增量】：我方的未来血液（如：新订单、流水）是否已断裂？
        3. ⛓️ 【调动通道（节点）】：最关键的！蓝方是否切断了我的传输节点？我的存量资产是随时可用的，还是被冻结的“远水”？
        
        【第二步：基于三维自检的战术动作】(知行合一)
        - 若【通道被切断（有存量无法调动）】：你【绝对不能】直接使用被冻结的存量发起反击！你必须优先消耗其他资源去“打通节点”、“建立地下通道”或“寻找极其昂贵的替代物流”。
        - 若【双双重创】：无权反攻，只能极其凄惨地断尾求生。
        (你的动作必须符合严丝合缝的物理与后勤常识！)
        """
        return self._safe_api_call(prompt, is_json=False, model_name="gemini-3-flash-preview")

    # 🌟 修复：新增 round_num 和 max_rounds 参数，引入战争迷雾
    def blue_agent_turn(self, strategy, red_action, historical_prototype="无特定原型", round_num=1, max_rounds=2):
        
        # 🌪️ 动态烈度与随机性引擎
        if round_num == 1:
            attack_mode = "【盲盒摩擦（高度随机性）】：你现在处于战争迷雾中，不知道红方的致命弱点。请基于历史同构原型，制造一场【随机的、无差异的宏观波动或常规竞争摩擦】（例如：全行业原材料普涨、汇率波动、新规草案出台）。⚠️ 绝对不要进行极其精准的定向狙击！"
        elif round_num < max_rounds:
            attack_mode = "【战术试探（针对性增强）】：红方在上一轮的行动中不可避免地暴露了资源调动轨迹。请分析其刚刚的动作，寻找其防线的薄弱环节，发动一次中等烈度的【针对性商业阻击或围堵】。"
        else:
            attack_mode = "【终极绞杀（致命降维）】：扯下伪装！结合历史同构的深层规律，直接锁定红方在之前回合中暴露出的最致命断裂点（资金链、核心节点或技术底座），发动一次极其凶狠的【极端黑天鹅或结构性摧毁打击】！"

        prompt = f"""
        你是客观环境与竞争对手的无情集合体（蓝方）。
        面对红方战略：【{strategy}】
        红方刚刚应对的动作：【{red_action}】
        先知锁定的历史同构规律：【{historical_prototype}】
        
        🌪️ 【当前环境生成法则】：{attack_mode}
        
        ⚠️ 请严格按照以下两步逻辑进行思考和输出（总字数严格控制在 150 字以内）：
        【第一步：局势演化】用一句话客观描述当前市场/环境发生了什么变化。
        【第二步：物理施压】描述这次变化/攻击将如何具体消耗红方的资源、增加阻力或切断通道。
        """
   
        return self._safe_api_call(prompt, is_json=False, model_name="gemini-3-flash-preview")
    

    def referee_judge(self, strategy, red_action, blue_reaction, current_stability, leverage_desc=""):
        # 兼容无财报设定的前置说明
        fin_constraint = "🌪️【审计模式】：纯逻辑推演（无财报约束）。红方不受账面资金限制，但【绝对受限于】当前的稳定性（后勤调度能力）。"

        prompt = f"""
        你是璇玑(PHSL)系统的无情物理仲裁官。你处于一个【绝对双盲实验】中。

        【当前战局快照】
        - 核心战略逻辑：{strategy}
        - 🛡️ 红方物理装甲（杠杆）：{leverage_desc} 
        - 交锋前红方稳定性：{current_stability:.1f}%
        {fin_constraint}

        【本回合交锋记录】
        🔴 红方动作：{red_action}
        🔵 蓝方反扑：{blue_reaction}

        ⚖️ 【判决核心法则】：

        1. 🛡️【降噪透穿率测算（核心物理参数）】：
           请你深刻“意会”红方的【物理装甲】能否抵御蓝方的具体【攻击方式】。首先输出一个【降噪透穿率(noise_multiplier)】，取值范围 [0.0, 1.0]:
           - 透穿率 1.0:装甲完全失效/未产生降噪，蓝方攻击 100% 穿透。
           - 透穿率 0.0:装甲完美克制该攻击,实现完全降噪,0% 穿透。

        2. 🩸【预估原始伤害】：
           根据蓝方攻击的烈度和红方的失误,直接给出一个【原始伤害5-25%】。(注：你不需要计算最终净伤害，底层系统引擎会接管计算)。

        💀【物理猝死判定 (is_bankrupt)】：
           ⚠️ 你处于绝对双盲状态，无权知道系统的理论死亡红线。你只能根据当前的物理常识和装甲对抗逻辑，判定是否触发了以下“结构性猝死”（只要满足一条即刻判定 True):
           
           - 🛡️【基座坍塌（无视血量）】：蓝方摧毁了红方赖以生存的核心资产。但是！你必须深刻评估红方的【物理装甲(leverage)】是否能防御此攻击。如果红方的杠杆明确克制该攻击，则【绝对不能】判死；如果红方是 L-0 裸奔或装甲失效，则直接击穿，满血也直接判死。
           
           - 🩸【动作变形/后勤断裂（挂钩血量）】：评估红方的【反击动作】与其【当前剩余稳定性(血量)】是否匹配。如果在当前的血量状态下（哪怕是 60% 甚至 80%），红方的动作（如“全线反击”、“百亿狂砸”）明显超过了其剩余资源的支撑极限，这属于严重的【战术幻觉与后勤断裂】，必须立刻判死！
           
           - ⛓️【通道窒息】：造血增量被切断，且所有可调动的物理存量被完全锁死。
           

        请【严格以 JSON 格式】输出你的判决：
        ```json
        {{
            "noise_multiplier": (浮点数,0.0到1.0之间),
            "raw_damage_percentage": (浮点数，最终计算出的净扣血量),
            "referee_logic": "(120字以内。冷酷说明:为什么给出这个透穿率？净伤害如何算出？)",
            "is_bankrupt": (布尔值)
        }}
        ```
        """
        raw_text = self._safe_api_call(prompt, is_json=False, model_name="gemini-2.5-pro")
        raw_text = self._safe_api_call(prompt, is_json=False, model_name="gemini-2.5-pro")
        # ==========================================
        # 🛡️ 新增：装甲级 JSON 解析与清洗中心
        # ==========================================
        try:
            # 1. 防止交白卷
            if not raw_text or not raw_text.strip():
                raise ValueError("裁判官模型返回了空字符串 (可能触发了安全拦截)")
            
            clean_text = raw_text.strip()
            
            # 2. 物理切除大模型喜欢乱加的 Markdown 标记 (```json 和 ```)
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            elif clean_text.startswith("```"):
                clean_text = clean_text[3:]
                
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
                
            clean_text = clean_text.strip()
            
            # 3. 安全解析
            return json.loads(clean_text)
            
        except Exception as e:
            # 4. 终极防线：如果解析彻底失败，绝对不让系统崩溃！
            # 强制返回一个默认的“轻伤”判定，让沙盘推演能够继续活下去
            print(f"⚠️ JSON 解析防线触发！原始文本: {raw_text} | 错误: {e}")
            return {
                "noise_multiplier": 1.0,
                "raw_damage_percentage": 5.0,
                "referee_logic": "裁判官系统发生认知偏离或安全拦截，按系统强制协议判定为轻度磨损。",
                "is_bankrupt": False
            }

    # 【核心改造 1】：升级为异步方法
# 增加 noise_multiplier 参数，默认 1.0 (不降噪)
    async def run_single_simulation(self, strategy_vision, historical_prototype="无", leverage_val=1.0, leverage_desc="L-0 裸奔基准", noise_multiplier=1.0, log_output=False):
        await asyncio.sleep(random.uniform(1.0, 3.0))
        stability = 100.0
        context = "战略刚刚启动，各方势力处于观望状态。"
        battle_log = ""
        
        safe_leverage = max(leverage_val, 1.0) 
        
        for round_num in range(1, self.max_rounds + 1):
            await asyncio.sleep(2) 
            # 🌟 修复：严格对齐 red_agent_turn 的参数位置
            # 顺序: strategy, round_num, current_stability, context, leverage_desc
            red_action = await asyncio.to_thread(
                self.red_agent_turn, 
                strategy_vision, 
                round_num, 
                stability,       # 传入当前真实的浮点数血量
                context, 
                leverage_desc
            )
            await asyncio.sleep(2)
            blue_reaction = await asyncio.to_thread(self.blue_agent_turn, strategy_vision, red_action, historical_prototype)
            await asyncio.sleep(2)
            # 裁判官依然需要知道 leverage_val 和 desc 来进行综合评判
            judgement = await asyncio.to_thread(
                self.referee_judge, 
                strategy_vision, 
                red_action, 
                blue_reaction, 
                stability,       # 👈 关键修复：把红方真实的血量传给裁判官
                leverage_desc    # 裁判官靠阅读这一段装甲文字，就能自动意会出降噪透传率
            )
            
            #精准提取大模型给出的两个纯参数
            raw_damage = judgement.get('raw_damage_percentage', 5.0)
            is_collapsed = judgement.get('is_bankrupt', False)
            
            # ==============================================================
            # 🌟 核心物理机制终极进化：完全听从先知的动态降噪透传率！
            # 彻底废除 raw_damage / (safe_leverage ** 0.5) 的死板公式。
            # 如果是 L-0，noise_multiplier 为 1.0，全额承受真实伤害。
            actual_damage = raw_damage * noise_multiplier 
            # ============================================================
            stability -= actual_damage
            context = blue_reaction
            
            # 【核心改造 2】：将每次交锋录制为 Markdown 文本
            battle_log += f"#### ⚔️ 第 {round_num} 回合\n"
            battle_log += f"> **🔴 进攻方动作:** {red_action}\n>\n"
            battle_log += f"> **🔵 阻力方反扑:** {blue_reaction}\n>\n"
            
            # 🌟 修复点：彻底合并判词与损耗，消除冗余重复打印
            judgement_text = judgement.get('referee_logic', '无判定理由')
            
            if is_collapsed or stability <= 0:
                # 阵亡分支：判词 + 🚨 触发致死红线
                battle_log += f"> **⚖️ 裁判官仲裁:** {judgement_text} **💥 物理损耗: -{actual_damage}% | 🚨 触发致死红线: {stability:.1f}%**\n\n---\n"
                battle_log += f"🚨 **战略在第 {round_num} 回合发生物理学坍塌！(红线击穿)**\n"
                return max(0, stability), battle_log 
            else:
                # 存活分支：判词 + 🛡️ 剩余稳定性
                battle_log += f"> **⚖️ 裁判官仲裁:** {judgement_text} **💥 物理损耗: -{actual_damage}% | 🛡️ 剩余稳定性: {stability:.1f}%**\n\n---\n"
                
        battle_log += "✅ **战略韧性极佳，成功扛过所有压测回合！**\n"
        return max(0, stability), battle_log

class XuanjiValidator:
    def __init__(self, api_key):
        self.arena = StrategicArena(api_key)
        
    # 🌟 修复 1：在函数定义中，补齐前端传来的三个装甲参数！
    async def run_monte_carlo_validation(self, strategy_vision, oracle_bp, historical_prototype="无", iterations=2, leverage_val=1.0, leverage_desc="L-0 裸奔基准", noise_multiplier=1.0):
        print(f"\n{'='*70}")
        print(f"🔬 璇玑系统双盲验证启动 | 目标战略：{strategy_vision[:20]}...")
        print(f"⏳ 正在瞬间并发 {iterations} 次独立 ABM 沙盘推演...")
        
        tasks = []
        for i in range(iterations):
            # 🌟 修复 2：将这三个参数接力传递给底层的单次推演引擎！
            tasks.append(self.arena.run_single_simulation(
                strategy_vision=strategy_vision, 
                historical_prototype=historical_prototype, 
                leverage_val=leverage_val,          # 接力向下传
                leverage_desc=leverage_desc,        # 接力向下传
                noise_multiplier=noise_multiplier,  # 接力向下传
                log_output=False
            ))
            
        results = await asyncio.gather(*tasks)
        
        # 结果拆解：results 里是类似于 [(分1, 战报1), (分2, 战报2)] 的结构
        emergent_bps = [res[0] for res in results]
        battle_logs = [res[1] for res in results]
            
        # 统计学计算
        avg_emergent_bp = np.mean(emergent_bps)
        std_dev = np.std(emergent_bps)
        delta = abs(oracle_bp - avg_emergent_bp)
        
        print(f"\n📊 【双盲验证结算报告】")
        print(f"🔹 平均崩溃红线: {avg_emergent_bp:.2f}% | 波动: {std_dev:.2f} | 误差(Δ): {delta:.2f}%")
        
        # 将战报打包返回给前端
        return {
            "emergent_bps": emergent_bps,
            "avg_emergent_bp": avg_emergent_bp,
            "std_dev": std_dev,
            "delta": delta,
            "battle_logs": battle_logs 
        }