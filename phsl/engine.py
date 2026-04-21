import numpy as np

class XuanjiEngine:
    def __init__(self):
        # 统一采样分辨率，解决绘图对齐问题
        self.p_range = np.linspace(0, 25, 500)
        self.nodes = {} 
        self.audit_results = {}

    @staticmethod
    def refine_density_with_bayesian(prior, p_e_h, p_e_not_h, noise):
        """贝叶斯噪声对冲核心"""
        p_e_h_n = (p_e_h * (1 - noise)) + (0.5 * noise)
        p_e_not_h_n = (p_e_not_h * (1 - noise)) + (0.5 * noise)
        p_e = (p_e_h_n * prior) + (p_e_not_h_n * (1 - prior))
        return (p_e_h_n * prior) / p_e if p_e != 0 else prior

    def run_ert_stress_test(self, volatility, threshold=None):
        """
       ERT 压测：计算崩坏线
        如果没有传入 threshold，则默认为 38.2 (黄金分割红线)
        """
        if threshold is None:
            threshold = 38.2
        stabilities = [100 - (p**2 * volatility) for p in self.p_range]
    # 增加安全性检查，防止 bp 为 None
        bp = next((p for p, s in zip(self.p_range, stabilities) if s <= threshold), None)
        return stabilities, bp

    def calculate_activation_threshold(self, ssc_density, inertia_coefficient, leverage=1.0, ai_threshold=None, volatility=None):
        """
        SIP 压测：计算点火点
        ai_threshold: 由 AI 估计的起效门槛 (0.0 - 1.0)
    
        """
        effective_resistance = inertia_coefficient * (1 + volatility)
        # 计算效能分布
        efficiencies = [(p * (ssc_density * leverage)) / (effective_resistance + p) for p in self.p_range]
        
        # 寻找第一个超过 AI 设定门槛的压强点
        # 这里的 0.5 被替换成了动态的 ai_threshold
        ap = next((p for p, e in zip(self.p_range, efficiencies) if e >= ai_threshold), None)
        
        return efficiencies, ap
    def apply_noise_filter(self, noise, leverage, sensitivity=0.7):
        """
        方案 B：杠杆降噪滤波器
        物理意义：利用技术或标准代差 (L) 强行穿透地缘环境噪声 (noise)
        :param sensitivity: 敏感度，0.5 为标准开方，0.7 为强穿透，0.3 为弱抵消
        """
    # 确保杠杆不小于 1.0，防止噪声反向放大
        safe_leverage = max(leverage, 1.0) 
    
    # 核心公式：噪声随杠杆幂律衰减
        effective_noise = noise / (safe_leverage ** sensitivity)
    
        return effective_noise
    def run_fre_validation(self, prior_base, noise, iterations=10000):
        """FRE 验证：蒙特卡洛真相模拟"""
        samples = np.random.normal(prior_base, noise, iterations)
        samples = np.clip(samples, 0, 1)
        return samples, np.mean(samples), np.std(samples)
    