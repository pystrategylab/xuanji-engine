import streamlit as st
import matplotlib.pyplot as plt
from google import genai
import asyncio
import pandas as pd
from phsl import StrategicOracle, XuanjiEngine, XuanjiController, PHSLVisualizer
from phsl.arena import XuanjiValidator 

# --- 页面配置 ---
st.set_page_config(
    page_title="璇玑定量化战略审计终端原型机",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 自定义样式 ---
st.markdown("""
    <style>
    .report-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin-bottom: 20px;
    }
    /* 指标容器背景 */
    [data-testid="stMetric"] {
        background-color: #0e1117;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    /* 强制指标数值变白 */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    /* 强制指标标签（标题）变浅灰 */
    [data-testid="stMetricLabel"] {
        color: #d1d1d1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 初始化系统与状态记忆 (State Machine)
# ==========================================
def init_system(api_key):
    oracle = StrategicOracle(api_key)
    engine = XuanjiEngine()
    controller = XuanjiController(oracle, engine)
    viz = PHSLVisualizer(theme='dark')
    return controller, viz

# 记忆中枢：控制当前显示哪个页面，以及存储跑出来的数据
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'  # 可选: 'home', 'audit', 'scout'
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = None
if 'scout_results' not in st.session_state:
    st.session_state.scout_results = None

# ==========================================
# 侧边栏：控制台 UI
# ==========================================
st.sidebar.image(
    "https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,fit=crop,q=95/1evUiS818YahKfZE/pythonlogo2-AfiMET3ydIQjjfId.png", 
    width="stretch"
)
st.sidebar.title("Python历史战略实验室")
st.sidebar.caption("PHSL | 璇玑定量化战略审计中枢 |www.pystrategylab.com")
st.sidebar.divider()

st.sidebar.title("🛠️ 璇玑指挥控制台")
api_key = st.sidebar.text_input("API KEY", type="password")
vision_text = st.sidebar.text_area("输入战略愿景描述", height=150, 
                                 placeholder="例如：一带一路倡议对全球供应链的重构推演...")

with st.sidebar.expander("⚖️ 战略推演物理公理", expanded=True):
    st.latex(r"E = \frac{P \cdot (ssc\_d \cdot L)}{(I \cdot (1 + vol)) + P}")
    st.markdown(r"""
    **量纲说明：**
    * $E$: **战略效能** (Strategic Effectiveness)
    * $P$: **资源压强** (Resource Pressure)
    * $ssc\_d$: **逻辑密度** (SSC Density)
    * $L$: **战略杠杆** (Leverage)
    * $I$: **惯性阻力** (Inertia)
    * $vol$: **波动摩擦** (Volatility)
    """)

# 在 st.sidebar.button("⚡ 启动全领域审计") 之前插入
st.sidebar.markdown("#### 📑 报告输出设置")
include_sources_in_pdf = st.sidebar.checkbox("附录：《环境情报溯源清单》", value=True, help="附带底层搜索引擎抓取的权威数据源。")

run_audit = st.sidebar.button("⚡ 启动全领域审计", width='stretch')


# ==========================================
# 动作触发器：执行大模型计算并存入记忆
# ==========================================
# 触发 1：全领域审计
if run_audit:
    if not api_key or not vision_text:
        st.sidebar.warning("🚨 请输入 API Key 并填写战略愿景。")
    else:
        st.session_state.current_view = 'audit'  # 切换视图
        
        # 🌟 修复点：在启动新战略审计时，强制清空旧的风洞战报记忆
        if 'v_res' in st.session_state:
            del st.session_state['v_res']
        if 'pure_red_strategy' in st.session_state:
            del st.session_state['pure_red_strategy']    
        if 'v_results_history' in st.session_state:  # 👈 新增：彻底清空旧战略的所有杠杆测试记录！
            del st.session_state['v_results_history']
        with st.spinner("🚀 [璇玑] 系统全频率点火，正在检索历史同构并执行多杠杆物理推演..."):
            try:
                controller, viz = init_system(api_key)
                results = controller.execute_full_audit(vision_text)
                if results:
                    st.session_state.audit_results = results
                else:
                    st.error("🚨 审计链路中断，先知模块(Oracle)返回异常。")
            except Exception as e:
                st.error(f"❌ 系统崩溃: {str(e)}")
# ==========================================
# 主界面渲染：根据 current_view 分流
# ==========================================
st.title("🛡️ 璇玑定量化战略审计终端原型机 - 终端界面")
st.latex(r"E = \frac{P \cdot (ssc\_d \cdot L)}{(I \cdot (1 + vol)) + P}")
st.caption("计算战略第四定律 | 同构即守恒")

# (辅助组件) 参数渲染模块
def display_parameter_audit_module(report, physics):
    with st.container():
        st.markdown("#### 🔍 逻辑与先验审计")
        col1, col2 = st.columns(2)
        bp_params = report.get('bayesian_params', {})
        
        with col1:
            st.info(f"**逻辑密度 (ssc_density): {bp_params.get('ssc_density', 0.5)}**")
            st.caption("物理意义：战略逻辑与物理资产的绑定强度。")
        with col2:
            st.info(f"**先验胜率 (Prior): {bp_params.get('prior', 0.5)}**")
            st.caption("物理意义：基于历史同构案例计算的初始成功概率。")
        st.write(f"**审计依据：** {bp_params.get('解释说明', '暂无详细逻辑存证。')}")
        
        st.markdown("#### 🌪️ 环境对冲审计")
        c1, c2, c3 = st.columns(3)
        
        # 提取出红线数值备用
        bp_val = physics.get('applied_threshold', 0.0)
        
        with c1:
            st.warning(f"**波动率 (vol): {physics.get('volatility', 0.0)}**")
        with c2:
            st.warning(f"**阻力系数 (I): {report.get('inertia_coefficient', 10.0)}**")
        with c3:
            # 🛠️ 修复 1：在前端警告框中硬编码加上 % 外衣
            st.warning(f"**崩溃红线 (BP): {bp_val}%**")
            
        # 🛠️ 修复 2：对大模型输出的长文本进行动态拦截与替换
        import re
        explanation = report.get('解释说明', '环境数据已由 Oracle 模块实时校准。')
        
        # 🎯 滤网：无情抹除环境评估依据里的角标 (如 [4])
        explanation = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', explanation)
    
        if bp_val:
            explanation = explanation.replace(f"({bp_val})", f"({bp_val}%)")
            
        st.write(f"**环境评估依据：** {explanation}")
        
        st.markdown("#### 🚀 攻势杠杆审计")
        st.success(f"**起效门槛 (Activation Threshold): {physics.get('ai_threshold', 0.5)}**")
        
        import re
        lev_info = report.get('leverage', {})
        raw_lev_desc = lev_info.get('解释说明', '杠杆参数已根据技术代差/资源集中度修正。')
        # 🎯 滤网：抹除杠杆解释中的角标
        clean_lev_desc = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', raw_lev_desc)
        
        st.write(f"**杠杆评估依据：** {clean_lev_desc}")

# ----------------------------------------
# 视图 A：待机主页
# ----------------------------------------
if st.session_state.current_view == 'home':
    st.info("💡 请在左侧输入指令，点击‘启动全领域审计’或‘启动战略巡察’以唤醒璇玑。")
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col2:
        st.image("https://assets.zyrosite.com/1evUiS818YahKfZE/cc-jbS5206kEeW4ygoV.png", width='stretch')

# ----------------------------------------
# 视图 B：全领域审计报告页
# ----------------------------------------
elif st.session_state.current_view == 'audit' and st.session_state.audit_results:
    results = st.session_state.audit_results
    report = results['audit_report']
    physics = results['physics_results']
    controller, viz = init_system(api_key) 
# ==========================================
    # 🌟 终极微创手术：全局文本净化滤网
    # 在数据流向下游 UI 之前，在这里一次性把所有 % 号加上！
    # ==========================================
    import re
    
    # 1. 净化全局杠杆总结论 (应用于第一板块、第三板块)
    if 'leverage_desc' in physics:
        raw_desc = physics['leverage_desc']
        clean_desc = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', raw_desc) # 抹除角标
        # 给中括号里的第二个数字穿上 % 号防弹衣
        physics['leverage_desc'] = re.sub(r'\[([0-9.]+),\s*([0-9.]+),\s*([0-9.]+)\]', r'[\1, \2%, \3]', clean_desc)

    # 2. 净化每一个独立杠杆的描述 (应用于 PDF 表格、风洞装甲菜单)
    if 'leverage' in report:
        for k, v in report['leverage'].items():
            if isinstance(v, str):
                clean_v = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', v)
                report['leverage'][k] = re.sub(r'\[([0-9.]+),\s*([0-9.]+),\s*([0-9.]+)\]', r'[\1, \2%, \3]', clean_v)
    # ==========================================
    # 第一板块：战略背景与同构
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("🏛️ 首席审计官简报")
        st.info(f"**核心同构原型：** {report.get('history_prototype', '未知')}")
        st.markdown(f"> {physics.get('leverage_desc', '无数据')}")

    with col2:
        st.subheader("🚀 物理量纲监控")
        m1, m2, m3 = st.columns(3)
        vol_val = physics.get('volatility', 0.00)
        ine_val = report.get('inertia_coefficient', 10.0) 
        bp_val = physics.get('applied_threshold', 0.0)
        
        with m1:
            st.metric("环境波动 (vol)", f"{vol_val:.2f}", 
                      help="物理意义:外部环境的随机噪声与摩擦率。极度稳定为0,极度混乱为1。")
            # 使用 HTML 注入更贴合的辅助文本，调整 margin 向上靠拢数字
            st.markdown("<div style='color: #666; font-size: 0.8rem; margin-top: -10px;'>取值区间: [0.0, 1.0]</div>", unsafe_allow_html=True)
            
        with m2:
            st.metric("惯性阻力 (I)", f"{ine_val}", 
                      help="物理意义:推进该战略所需对抗的系统惯性。最低为1(零阻尼),极限标定为20。")
            st.markdown("<div style='color: #666; font-size: 0.8rem; margin-top: -10px;'>取值区间: [1.0, 20.0]</div>", unsafe_allow_html=True)
            
        with m3:
            st.metric("崩溃红线 (BP)", f"{bp_val:.2f}%", 
                      help="物理意义:系统发生不可逆坍塌的百分比临界值。")
            st.markdown("<div style='color: #666; font-size: 0.8rem; margin-top: -10px;'>取值区间: [0, 100]%</div>", unsafe_allow_html=True)
    st.divider()

    # 第二板块：逻辑与历史
    c_left, c_right = st.columns(2)
    with c_left:
        st.markdown('<div class="report-card">', unsafe_allow_html=True)
        st.subheader("📜 《逻辑覆盖率审计报告》")
        
        import re  # 确保引入正则处理库
        
        # 🎯 滤网 1：净化主报告文本，抹除形如 [6, 21] 的角标
        raw_report_text = report.get("《逻辑覆盖率审计报告》", "暂无数据")
        clean_report_text = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', raw_report_text)
        st.write(clean_report_text)
        
        nodes = report.get('ssc_audit_nodes', {})
        
        # 🎯 滤网 2：净化底部的节点解释说明文本
        raw_explanation = report.get('节点解释说明', '暂无节点解释说明。')
        clean_explanation = re.sub(r'\s*\[\d+(?:,\s*\d+)*\]', '', raw_explanation)
        st.caption(f"节点解释：{clean_explanation}")
        
        st.json(nodes)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_right:
        st.markdown('<div class="report-card" style="border-left-color: #00FFCC;">', unsafe_allow_html=True)
        st.subheader("🗺️ 《历史同构映射图谱》")
        st.write(report.get("《历史同构映射图谱》", "暂无数据"))
        st.caption("基于物理资产绑定强度与结构一致性计算")
        st.markdown(report.get("孙子兵法引用", "暂无孙子兵法引用内容。"))
        st.markdown(report.get("卦象同构", "暂无卦象同构内容。"))
        st.markdown(report.get("卦象演进方向", "暂无卦象演进方向内容。"))
        st.markdown('</div>', unsafe_allow_html=True)

    # 第三板块：系统脆性压测报告
    st.divider()
    st.subheader("🌋 《系统脆性压测报告》")
    
    fig_sip = viz.plot_sip_audit(physics, title_prefix="当前审计预案")
    st.pyplot(fig_sip, width='stretch')
    st.info(f"💡 AI 战略建议:\n\n{physics.get('leverage_desc')}")
    
    
    fig_res = viz.plot_resilience_audit(physics)
    st.pyplot(fig_res, width='stretch')
            
    with st.expander("查看压测细节数据"):
        lever_df = pd.DataFrame({
            "杠杆预案": ["L1", "L2", "L3", "L-0 基准"],
            "系数": physics.get('leverage_options', [1.0, 1.0, 1.0, 1.0]),
            "点火压强 (AP)": [f"{p:.2f}" if p else "战略死区" for p in physics.get('all_activation_aps', [])]
        })
        st.table(lever_df)

    # 第四板块：贝叶斯认知更新
    st.subheader("🔮 《贝叶斯认知更新与后验胜率图谱》")
    mean_val = physics.get('mean', 0.5)
    samples_val = physics.get('samples', [])
            
    if len(samples_val) > 0:
        fig_truth = viz.plot_truth_curve(mean_val, samples_val)
        st.pyplot(fig_truth, width='stretch')
            
    st.success(f"🎯 最终审计结论：后验平均胜率（真理值）为 **{mean_val:.2%}**")

    # 参数解释模块
    display_parameter_audit_module(report, physics)
    # 新增：实时情报流展示面板 ===
    st.markdown("#### 📡 贝叶斯推断环境情报源 (Environmental Intelligence Anchors)")
    sources = report.get('environmental_sources', [])
    
    if sources:
        with st.expander(f"👁️ 查看底层检索情报源 ({len(sources)} 条权威锚点)"):
            for src in sources:
                st.markdown(f"* {src.get('polarity', '⚪')} **{src.get('source', '未知信源')}**: {src.get('fact', '...')} `{src.get('impact', '')}`")
    else:
        st.caption("本次审计未强制提取底层搜索链接。")
    # ==========================================
    # 多智能体沙盘验证 (计算部分)
    # ==========================================
    st.divider()
    st.subheader("🔬 数字风洞|动态沙盘：多智能体双盲验证")
    st.caption("通过红蓝双盲对抗，在数字风洞中压测 Oracle 先知预估红线的真实性，计算认知偏差 Δ。")
    
    st.markdown("#### ⚙️ 压测参数配置")
    num_universes = st.slider(
        "🌌 选择平行宇宙推演次数 (风洞并发数)", 
        min_value=1, max_value=10, value=3, step=1
    )
    # 🌟 新增：推演深度（最大交锋回合数）滑动条
    max_rounds_input = st.slider(
        "⚔️ 选择推演深度 (每宇宙最大交锋回合数)", 
        min_value=1, max_value=10, value=2, step=1,
        help="测试深度。回合数越多，环境的连续打击越严苛。增加此值可有效挤出‘伪韧性’水分，测出战略真实的绝对崩溃底线。"
    )
    # ==============================================================
    # 🌟 修复：新增防线选择器 (利用正则从大文本中萃取物理装甲)
    # ==============================================================
    lev_dict = report.get('leverage', {})
    thr = report.get('strategic_threshold', 38.2)

    # 重新构建 3维矩阵，确保物理参数坚如磐石
    levers_data = [
        lev_dict.get('leverage-1', [1.0, thr, 1.0]),
        lev_dict.get('leverage-2', [1.0, thr, 1.0]),
        lev_dict.get('leverage-3', [1.0, thr, 1.0]),
        lev_dict.get('leverage-0', [1.0, thr, 1.0])
    ]

    shield_options = {}
    desc_raw = physics.get('leverage_desc', '')
    import re

    # 我们需要遍历的 4 个默认键，严格对应 levers_data 的顺序 [L1, L2, L3, L0]
    levers_keys = ['leverage-1', 'leverage-2', 'leverage-3', 'leverage-0']

    for idx, key in enumerate(levers_keys):
        # 如果这个杠杆在物理字典里存在
        if key in lev_dict:
            l_val, _, n_mult = levers_data[idx]
            
            # 🎯 物理透视黑科技：利用正则从大文本中精准抓取该杠杆的【名称】与具体描述
            # 它的逻辑是：寻找 "leverage-1: 【名字】 描述正文..." 直到遇到下一个 leverage 或文本结束
            pattern = rf'{key}[^:\uFF1A]*[:\uFF1A]\s*(?:【(.*?)】)?(.*?)?(?=leverage-\d|$)'
            match = re.search(pattern, desc_raw, re.IGNORECASE | re.DOTALL)
            
            if match:
                # 如果抓到了【】里的名字，就用它；否则给个默认编号
                k_name = match.group(1).strip() if match.group(1) else f"战略装甲 {key.upper()}"
                v_desc = match.group(2).strip() if match.group(2) else "无描述"
            else:
                k_name = f"战略装甲 {key.upper()}"
                v_desc = "未找到详细描述"
                
            # 完美组装前端显示的炫酷 UI 字符串
            display_name = f"🛡️ {k_name} (点火: {l_val:.2f} | 透传: {n_mult:.2f})"
            shield_options[display_name] = {"val": l_val, "noise": n_mult, "desc": v_desc}

    # 终极防线：如果大模型彻底发疯解析失败，给一个保底的裸奔选项
    if not shield_options:
        shield_options["🛡️ L-0 基准裸奔 (点火: 1.00 | 透传: 1.00)"] = {"val": 1.0, "noise": 1.0, "desc": "无战略杠杆，直面环境波动。"}

    selected_shield_name = st.selectbox(
        "🔰 选择本次风洞压测的物理装甲 (战略杠杆)", 
        options=list(shield_options.keys()),
        help="选择不同的杠杆装甲带入风洞。降噪透传率越低，抵御能力越强，裁判官扣除的物理损耗越低。"
    )
    
    # 提取选中的装甲参数，准备喂给风洞
    chosen_leverage_val = shield_options[selected_shield_name]["val"]
    chosen_noise_mult = shield_options[selected_shield_name]["noise"]
    chosen_leverage_desc = shield_options[selected_shield_name]["desc"]
    # ==============================================================

    # 【改动点 1】：这个按钮里只负责“运算”和“存入记忆”，不再负责展示界面
    if st.button("⚔️ 启动数字风洞：验证先知预估红线", width='stretch'):
        with st.status("🔬数字风洞全功率运转中：正在压测先知红线...", expanded=True) as status:
            try:
                validator = XuanjiValidator(api_key=api_key)
                # 🌟 关键穿透：利用 Python 动态特性，直接覆盖底层沙盘的最大回合数设定
                validator.arena.max_rounds = max_rounds_input
                
                oracle_bp = physics.get('applied_threshold', 0.0)
                # 🚀 新增模块：全自动战略提纯桥接层 (Context Bridge)
                # ==========================================
                st.write("⚙️ 正在从 Oracle 静态审计结果中提取第一人称防御阵型...")
                
                # 调取上一轮分析的核心逻辑
                oracle_context = f"""
                逻辑覆盖率审计：{report.get('《逻辑覆盖率审计报告》', '')}
                逻辑节点分析：{report.get('ssc_audit_nodes', {})}
                逻辑节点解释：{report.get('节点解释说明', '')}
                历史同构分析：{physics.get('historical_prototype', '')}
                
                """
                extraction_prompt = f"""
                你是一个极其冷酷的战略提纯引擎。
                用户的初始模糊意图是：【{vision_text}】
                先知模块得出的战略逻辑评估是：【{oracle_context}】
                
                请结合以上信息，为该战略写一段 100 字以内的【第一人称实体宣告（思想钢印）】。
                
                ⚠️ 绝对服从以下铁律：
                1. 格式锚定：必须以“我方”或“我方[企业/组织名]”开头。（若未提及具体名称，直接使用“我方”）。
                2. 战略剥离：明确指出我们要调动什么【真实的物理资产、资金或核心资源】，去【对冲什么死局 / 达成什么终局目标】。
                3. 越权禁止：绝对不要提及具体的“战略杠杆等级”或“免伤护甲”（底层引擎会另行分配）。
                4. 指挥官语态：语气必须是决战前的最高统帅下达的死命令。绝对禁止出现“分析表明”、“基于上述评估”等旁观者废话。
                5. 纯净输出：直接、立刻输出宣告文本本身！绝对不准包含任何类似“好的”、“这是为您生成的宣告”等前言后语。 
                """
                
                # 调用 Gemini 模型进行瞬间提纯（可以使用更快速的 Flash 模型）
                client = genai.Client(api_key=api_key)
                extract_res = client.models.generate_content(
                    model="gemini-3-flash-preview", 
                    contents=extraction_prompt
                )
                # 获得真正要在风洞中挨揍的“实体战略”
                pure_red_strategy = extract_res.text.strip()
                # 🌟 关键新增：将提纯后的战略永久存入记忆
                st.session_state['pure_red_strategy'] = pure_red_strategy
                # 将提纯后的战略打印在前端，让用户知道系统正在测试什么
                st.info(f"**🎯 锁定红方实体战略：**\n\n> {pure_red_strategy}")
                
                
                # 🎯 新增：从之前的物理量纲中提取历史同构原型
                historic_proto = physics.get('historical_prototype', '常规商业博弈规律')

                # ==========================================
                # 2. 将提纯后的 pure_red_strategy 喂入风洞！
                # ==========================================
                st.write("⚡ 第一人称实体战略已注入，高并发对抗开始...")
                
                v_res = asyncio.run(validator.run_monte_carlo_validation(
                    strategy_vision=pure_red_strategy, # ⚠️ 关键：这里不再传入模糊的 vision_text，而是提纯后的指令
                    oracle_bp=oracle_bp, 
                    historical_prototype=historic_proto,
                    iterations=num_universes,
                    leverage_val=chosen_leverage_val,          # 传入点火杠杆
                    leverage_desc=chosen_leverage_desc,        # 传入装甲文字描述给红方
                    noise_multiplier=chosen_noise_mult   # 🌟 极度关键：传入截图提取的降噪透传率！
                ))
                
                # 🌟 核心修改 1：建立多维度存证缓存池
                if 'v_results_history' not in st.session_state:
                    st.session_state['v_results_history'] = {}
                
                # 以装甲名称为键，保存该次推演的完整快照
                st.session_state['v_results_history'][selected_shield_name] = {
                    "v_res": v_res,
                    "leverage_desc": chosen_leverage_desc,
                    "leverage_val": chosen_leverage_val,
                    "oracle_bp": oracle_bp
                }
                
                st.session_state['v_res'] = v_res  # 存储验证结果以供后续分析
                st.success(f"✅ 已将【{selected_shield_name}】的压测数据存入审计快照池。")
                
                status.update(label="✅ 数字风洞压测完成！先知红线已完成双盲验证。", state="complete", expanded=False)
            except Exception as e:
                st.error(f"🚨 沙盘点火失败: {str(e)}")

    # ==========================================
    # 🌟 【改动点 2】：独立出来的数据看板区 (展示部分)
    # ==========================================
    # 只要记忆体里有数据，就永远显示出来，不怕点击其他按钮刷新页面！
    # ==========================================
    # 🌟 独立出来的数据看板区 (展示部分)
    # ==========================================
    if 'v_res' in st.session_state:
        v_res = st.session_state['v_res']
        oracle_bp = physics.get('applied_threshold', 0.0)
        
        # 🌟 核心修正：生死隔离统计学 (分离阵亡宇宙与幸存宇宙)
        logs = v_res.get('battle_logs', [])
        all_scores = v_res.get('emergent_bps', [])
        
        dead_bps = []       # 记录被打死的宇宙的红线
        survived_scores = [] # 记录活下来的宇宙的余血
        
        for log, score in zip(logs, all_scores):
            if "✅" in log:
                survived_scores.append(score)
            else:
                dead_bps.append(score)
                
        # 计算沙盘存活率
        survival_rate = (len(survived_scores) / len(all_scores)) * 100 if all_scores else 0.0
        
       # 🌟 算法升级：计算综合等效红线 (Effective Emergent BP)
        # 融合阵亡组的致死线与幸存组的残血线，消除“幸存者偏差”
        if len(all_scores) > 0:
            if len(dead_bps) == 0:
                # 触发绝对防御（全员存活）
                avg_bp = 0.0
                raw_delta = -999.0
                emergent_bp_str = "🛡️ 未击穿"
                delta_str = "N/A"
            else:
                # 混合计算：把所有的 all_scores (包含死者的红线和幸存者的残血) 一起平均
                avg_bp = sum(all_scores) / len(all_scores)
                raw_delta = avg_bp - oracle_bp
                emergent_bp_str = f"{avg_bp:.2f}%"
                delta_str = f"{abs(raw_delta):.2f}%"

        if 'pure_red_strategy' in st.session_state:
            st.info(f"**🎯 风洞压测执行战略（已提纯）：**\n\n> {st.session_state['pure_red_strategy']}")
            st.write("") 
            
        st.markdown("### 📊 审计结算矩阵")
        
        # 🌟 升级：四列指标矩阵，加入存活率！
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("先知预估红线 (Oracle BP)", f"{oracle_bp:.2f}%")
        col2.metric("真实涌现红线 (Emergent BP)", emergent_bp_str, help="仅统计在风洞中发生崩溃的宇宙。若显示'未击穿'，说明未测出底线。")
        col3.metric("沙盘绝对存活率", f"{survival_rate:.0f}%", help="在所有平行宇宙推演中，成功扛过所有回合未崩溃的比例。")
        col4.metric("认知置信度误差 (Δ)", delta_str, delta_color="inverse")
        
       # 🌟 动态判词终极升级：引入“存活率一票否决”与“死缓陷阱”分级
        if raw_delta == -999.0:
            st.success(f"👑 **【绝对防御/深度不足】**：令人惊叹！该战略在 {len(all_scores)} 个平行宇宙中达成 100% 存活，风洞未能击穿其底线。这表明战略韧性极高，或当前预设的环境攻击烈度不足以触及其崩溃红线。")
            
        elif survival_rate == 0.0:
            # 🚨 绝对死局下，进一步细分是怎么死的
            if raw_delta < -5.0:
                st.error(f"🩸 **【死缓陷阱 / 慢性失血】**：警告！沙盘存活率为 0%。虽然涌现红线（{avg_bp:.2f}%）低于预估（{oracle_bp:.2f}%），表现出了极强的‘抗揍性’，但这只是‘流血致死’的过程被拉长了。这说明战略大方向已彻底被证伪，庞大的底盘只是在绝望地空耗资源！请立即重构，切勿盲目坚持！")
            else:
                st.error(f"💀 **【系统性猝死】**：沙盘存活率为 0%！您的战略在风洞中遭遇了极速的结构性坍塌（触发了资金断裂或通道窒息）。请立即放弃该幻想，重新校准物理装甲！")
                
        elif abs(raw_delta) <= 5.0:
           st.info("⭐⭐⭐ **【预测极度可靠】**：先知模块与物理沙盘产生高维共振，历史同构极其精准！")
           
        elif raw_delta < -5.0:
            # 只有在有存活率（没死绝）的情况下，BP降低才配叫“超额韧性”
            st.success(f"🛡️ **【涌现超额韧性】**：沙盘推演表明，该战略的实际韧性超出预期（增益 {abs(raw_delta):.2f}%）！风洞在动态博弈中发掘出了隐藏的结构优势，战略安全边际更为宽广。")
            
        elif 5.0 < raw_delta <= 15.0:
            st.warning(f"⭐⭐ **【环境噪声干扰】**：沙盘存活率仅为 {survival_rate:.0f}%。预测方向基本正确，但沙盘中出现了预期外的摩擦，导致崩溃红线上移。")
            
        else:
            st.error(f"★ **【先验逻辑坍塌】**: 红线极度恶化！数字风洞捕获到了静态模型未能预见的极端尾部风险。实际脆弱度远超先验评估，请立即重构防线。")
            

        # 展示交锋战报
        # ==========================================
        # 📜 动态博弈档案渲染区
        # ==========================================
        st.markdown("### 📜 动态博弈档案")
        
        # 提取战报数据
        logs = v_res.get('battle_logs', [])
        scores = v_res.get('emergent_bps', [])
        
        # 如果是“绝对防御”状态（从上方的 raw_delta 继承状态）
        if raw_delta == -999.0:
            st.success("🛡️ **防御壁垒未被击穿**：当前压测深度下，所有平行宇宙的防线均保持完整，未测出崩溃底线。您可以尝试在左侧配置面板增加推演回合数，进行更深度的压力测试。")
            
        # 遍历并渲染每个平行宇宙的战报手风琴
        for i, (log_text, score) in enumerate(zip(logs, scores)):
            # 动态判定手风琴标题
            if "✅" in log_text:
                title = f"🌌 宇宙 {i+1}：详细对抗战报 (🛡️ 完美扛过压测 | 剩余韧性: {score:.1f}%)"
            else:
                title = f"🌌 宇宙 {i+1}：详细对抗战报 (🚨 实测致死红线: {score:.1f}%)"
                
            # 渲染手风琴
            with st.expander(title):
                st.markdown(log_text)

        # 渲染底部的统计学细节
        with st.expander("🔍 查看统计学压测细节"):
            st.write(f"**每次推演结束时的韧性原始记录:** {[f'{x:.1f}%' for x in scores]}")
            st.write(f"**沙盘波动标准差 (Std):** {v_res.get('std_dev', 0.0):.2f}")

# 页脚
st.divider()
st.caption("PHSL (Python Historical Strategy Lab) | 璇玑定量化战略审计终端")