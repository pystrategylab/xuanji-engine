import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from phsl import StrategicOracle, XuanjiEngine, XuanjiController, PHSLVisualizer

# --- 页面配置 ---
st.set_page_config(
    page_title="璇玑通用战略审计终端",
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

# --- 初始化组件 ---
def init_system(api_key):
    oracle = StrategicOracle(api_key)
    engine = XuanjiEngine()
    controller = XuanjiController(oracle, engine)
    viz = PHSLVisualizer(theme='dark')
    return controller, viz

# --- 侧边栏：控制台 ---
# 1. 在侧边栏最上方插入 Logo
st.sidebar.image(
    "https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,fit=crop,q=95/1evUiS818YahKfZE/pythonlogo2-AfiMET3ydIQjjfId.png", 
    width="stretch"
)

# 2. 加上实验室名称与标语
st.sidebar.title("Python历史战略实验室")
st.sidebar.caption("PHSL | 璇玑定量化战略审计中枢")

# 3. 加上一条分割线，区分品牌区与操作区
st.sidebar.markdown("---")
st.sidebar.title("🛠️ 璇玑指挥控制台")
api_key = st.sidebar.text_input("API KEY", type="password")
vision_text = st.sidebar.text_area("输入战略愿景描述", height=150, 
                                 placeholder="例如：一带一路倡议对全球供应链的重构推演...")

with st.sidebar.expander("⚖️ 战略推演物理公理", expanded=True):
    st.latex(r"E = \frac{P \cdot (ssc\_d \cdot L)}{(I \cdot (1 + vol)) + P}")
    st.markdown("""
    **量纲说明：**
    * $E$: **战略效能** (Strategic Effectiveness)
    * $P$: **资源压强** (Resource Pressure)
    * $ssc\_d$: **逻辑密度** (SSC Density)
    * $L$: **战略杠杆** (Leverage)
    * $I$: **惯性阻力** (Inertia)
    * $vol$: **波动摩擦** (Volatility)
    """)

run_audit = st.sidebar.button("⚡ 启动全领域审计")

st.title("🛡️ 璇玑通用战略原型机 - 终端界面")
# 在 app.py 的 st.title 下方加入
st.latex(r"E = \frac{P \cdot (ssc\_d \cdot L)}{(I \cdot (1 + vol)) + P}")
st.caption("计算战略第四定律 | 同构即守恒")
def display_parameter_audit_module(report, physics):
    with st.container():
        # 1. 核心逻辑与先验层
        st.markdown("#### 🔍 逻辑与先验审计")
        col1, col2 = st.columns(2)
        
        # 链式 get 防止嵌套键缺失崩溃
        bp_params = report.get('bayesian_params', {})
        
        with col1:
            st.info(f"**逻辑密度 (ssc_density): {bp_params.get('ssc_density', 0.5)}**")
            st.caption("物理意义：战略逻辑与物理资产的绑定强度。")
        with col2:
            st.info(f"**先验胜率 (Prior): {bp_params.get('prior', 0.5)}**")
            st.caption("物理意义：基于历史同构案例计算的初始成功概率。")
        
        st.write(f"**审计依据：** {bp_params.get('解释说明', '暂无详细逻辑存证。')}")
        
        # 2. 环境层
        st.markdown("#### 🌪️ 环境对冲审计")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.warning(f"**波动率 (vol): {physics.get('volatility', 0.0)}**")
        with c2:
            st.warning(f"**阻力系数 (I): {report.get('inertia_coefficient', 10.0)}**")
        with c3:
            st.warning(f"**崩溃红线 (BP): {physics.get('applied_threshold', 0.0)}**")
            
        st.write(f"**环境评估依据：** {report.get('解释说明', '环境数据已由 Oracle 模块实时校准。')}")

        # 3. 攻势杠杆层
        st.markdown("#### 🚀 攻势杠杆审计")
        # 确保 ai_threshold 存在，controller 中已计算
        st.success(f"**起效门槛 (Activation Threshold): {physics.get('ai_threshold', 0.5)}**")
        
        lev_info = report.get('leverage', {})
        st.write(f"**杠杆评估依据：** {lev_info.get('解释说明', '杠杆参数已根据技术代差/资源集中度修正。')}")
        
if run_audit:
    if not api_key or not vision_text:
        st.error("🚨 请输入 API Key 并填写战略愿景。")
    else:
        with st.spinner("🚀 [璇玑] 系统全频率点火，正在检索历史同构并执行多杠杆物理推演..."):
            try:
                controller, viz = init_system(api_key)
                # 执行审计
                results = controller.execute_full_audit(vision_text)
                if results:
                    report = results['audit_report']
                    physics = results['physics_results']

                    # --- 第一板块：战略背景与同构 ---
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.subheader("🏛️ 首席审计官简报")
                        # 增加 .get() 保护
                        st.info(f"**核心同构原型：** {report.get('history_prototype', '未知')}")
                        st.markdown(f"> {physics.get('leverage_desc', '无数据')}")

                    with col2:
                        st.subheader("🚀 物理量纲监控")
                        m1, m2, m3 = st.columns(3)
                        # 这里你已经处理得很好，使用了变量保护
                        vol_val = physics.get('volatility', 0.00)
                        ine_val = report.get('inertia_coefficient', 10.0) # 建议默认值给 10.0
                        bp_val = physics.get('applied_threshold', 0.0)

                        m1.metric("环境波动 (vol)", f"{vol_val:.2f}")
                        m2.metric("惯性阻力 (I)", f"{ine_val}")
                        m3.metric("崩溃红线 (BP)", f"{bp_val}")
                    st.divider()

                    # --- 第二板块：逻辑与历史（文字报告区） ---
                    # ... (这部分逻辑正常)
                    # --- 第二板块：逻辑与历史（文字报告区） ---
                    c_left, c_right = st.columns(2)
                    
                    with c_left:
                        st.markdown('<div class="report-card">', unsafe_allow_html=True)
                        st.subheader("📜 《逻辑覆盖率审计报告》")
                        st.write(report.get("《逻辑覆盖率审计报告》", "暂无数据"))
                        # 显示节点状态
                        nodes = report.get('ssc_audit_nodes', {})
                        explanation = report.get('节点解释说明', '暂无节点解释说明。')
                        st.caption(f"节点解释：{explanation}")
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
                    # --- 第三板块：系统脆性压测报告 ---
                    st.markdown("---")
                    
                    st.subheader("🌋 《系统脆性压测报告》")
                    # 1. 获取描述文本
                    desc = physics.get('leverage_desc', "暂无战略校准建议")
                   # 1. 绘制并显示效能对冲图 (SIP)
                    fig_sip = viz.plot_sip_audit(physics, title_prefix="当前审计预案")
                    st.pyplot(fig_sip)
                    st.info(f"**💡 AI 战略建议**：\n\n{desc}")
                    # 2. 绘制并显示结构韧性图 (ERT)
                    fig_res = viz.plot_resilience_audit(physics)
                    st.pyplot(fig_res)
                    
                    with st.expander("查看压测细节数据"):
                        lever_df = pd.DataFrame({
                            "杠杆预案": ["L1", "L2", "L3", "L-0 基准"],
                            "系数": physics.get('leverage_options', [1.0, 1.0, 1.0, 1.0]),
                            "点火压强 (AP)": [f"{p:.2f}" if p else "战略死区" for p in physics.get('all_activation_aps', [])]
                        })
                        st.table(lever_df)

                    # --- 第四板块：贝叶斯认知更新 ---
                    st.subheader("🔮 《贝叶斯认知更新与后验胜率图谱》")
                    # 使用 .get() 保护核心数据
                    mean_val = physics.get('mean', 0.5)
                    samples_val = physics.get('samples', [])
                    
                    if len(samples_val) > 0:
                        fig_truth = viz.plot_truth_curve(mean_val, samples_val)
                        st.pyplot(fig_truth, width="stretch")
                    
                    st.success(f"🎯 最终审计结论：后验平均胜率（真理值）为 **{mean_val:.2%}]**")

                    # --- 重要修复：在此处调用参数解释模块 ---
                    display_parameter_audit_module(report, physics)
                else:
                    st.error("🚨 审计链路中断，先知模块(Oracle)返回异常。")

            # 🛑 检查这里！必须有这个 except 块，并且与 try 对齐
            except Exception as e:
                st.error(f"❌ 系统崩溃: {str(e)}")
else:
    # 待机界面
    st.info("💡 请在左侧输入指令，点击‘启动全领域审计’以唤醒璇玑。")
    # 创建三列，比例为 1:2:1，图片放在中间列
    col1, col2, col3 = st.columns([1, 2, 1]) 
    
    with col2:
        st.image("https://assets.zyrosite.com/1evUiS818YahKfZE/cc-jbS5206kEeW4ygoV.png", width="stretch")

st.markdown("---")
st.caption("PHSL (Python History Strategy Lab) | 璇玑系统战略审计终端")