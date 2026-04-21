from .engine import XuanjiEngine
from .oracle import StrategicOracle

class XuanjiController:
    def __init__(self, oracle, engine):
        self.oracle = oracle
        self.engine = engine    
    def run_strategic_scout(self):
        """
        [新增] 执行板块战略巡察逻辑
        功能：调用先知模块的主动侦察功能，获取全球战略板块的五事能级 JSON。
        """
        # 调用 Oracle 模块中新增的 scout_strategic_sectors 方法
        scout_json = self.oracle.scout_strategic_sectors()
        
        if not scout_json:
            print("🚨 [中枢] 巡察指令未获得有效数据包，全球雷达扫描中断。")
            return None
        
        # 返回结构化数据供 App.py 进行雷达图渲染
        return scout_json
    
    def execute_full_audit(self, vision_text):
        audit_json = self.oracle.dynamic_isomorphism_discovery(vision_text)
        if not audit_json:
            print("🚨 [中枢] 收到空数据包，物理压测无法点火。请检查网络或 API 配置。")
            return None
        # 提取参数
        vol = audit_json.get('dynamic_volatility', 0.22)
        thr = audit_json.get('strategic_threshold', 38.2)
        ine = audit_json.get('inertia_coefficient', 10.0)
        b = audit_json.get('bayesian_params', {})
        lev_bundle = audit_json.get('leverage', {})
        leverage_desc = lev_bundle.get('解释说明', "无")
        levers = [
            lev_bundle.get('leverage-1', 1.0),
            lev_bundle.get('leverage-2', 1.0),
            lev_bundle.get('leverage-3', 1.0),
            lev_bundle.get('leverage-0', 1.0), # 默认无杠杆，数值为1.0
        ]
        # 新增：从 audit_json 中直接提取杠杆和动态门槛                  # 杠杆系数 L，默认为1.0
        ai_thr = audit_json.get('activation_threshold', 0.5)  # 起效门槛 e，默认为0.5
        # 贝叶斯对冲（使用 ssc_density 进行物理修正）
        refined_density = self.engine.refine_density_with_bayesian(
            b.get('prior', 0.5), b.get('ssc_density', 0.5), 
            b.get('p_e_not_h', 0.2), b.get('noise', 0.1)
        )
        
        # 物理压测
        stabs, bp = self.engine.run_ert_stress_test(vol, thr)
        # 【核心修改】：通过列表推导式，一次性跑完 3 个杠杆的 SIP 压测
        sip_results = [
            self.engine.calculate_activation_threshold(refined_density, ine, L, ai_thr, vol)
            for L in levers # 遍历每个杠杆系数
        ]
        all_effs = [r[0] for r in sip_results]
        all_aps = [r[1] for r in sip_results]
        
        # 1. 计算当前的加权杠杆 (取三个杠杆的平均值或最大值)
        avg_L = sum(levers) / len(levers)
        # 2. 使用加权杠杆进行 FRE 验证
        effective_noise = self.engine.apply_noise_filter(
            noise=b.get('noise', 0.1), 
            leverage=avg_L,
            sensitivity=0.5  # 采用您认可的 0.5 次方语法
        )
        samples, mean, std = self.engine.run_fre_validation(refined_density, effective_noise)

        res = {
            'p_range': self.engine.p_range, 'stabilities': stabs, 'efficiencies': all_effs[0],
            'break_point': bp, 'activation_p': all_aps[0], 'applied_threshold': thr,'effective_noise': effective_noise,
            'samples': samples, 'mean': mean, 'std': std, 'volatility': vol, 'leverage': levers[0], 'leverage_desc': leverage_desc, 'leverage_options': levers, 'ai_threshold': ai_thr,'all_efficiencies': all_effs, 'all_activation_aps': all_aps
        }
        return {"audit_report": audit_json, "physics_results": res}