import matplotlib.pyplot as plt
import numpy as np

# 1. 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

class PHSLVisualizer:
    """
    璇玑战略可视化标准库 (全量样本增强版)
    """
    
    def __init__(self, theme='dark'):
        # 修复：去掉了 @staticmethod，改为标准的构造函数
        # 设置 2026 科技感审美风格
        self.colors = ['#FFD700', '#FFA500', '#FF4500']  # 黄金、橙色、深橙（对应L1-L3）
        self.stab_color = '#00FFCC'                     # 稳定性曲线颜色
        if theme == 'dark':
            plt.style.use('dark_background')
        else:
            plt.style.use('seaborn-v0_8')

    @staticmethod
    def plot_truth_curve(prior, samples):
        """
        绘制 FRE 真相分布图 (体现全量样本颗粒感)
        """
        mean = np.mean(samples)
        std = np.std(samples)
        
        fig, ax = plt.subplots(figsize=(20, 14), facecolor='#0e1117')
        ax.set_facecolor('#0e1117')

        # 绘制原始样本直方图
        ax.hist(samples, bins=60, density=True, alpha=0.25, color='#00ffcc', 
                label='Monte Carlo Raw Samples')

        # 绘制理论真相曲线 (高斯分布)
        x = np.linspace(0, 1, 200)
        epsilon = 1e-9
        y = (1/((std + epsilon) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean)/(std + epsilon))**2)
        ax.plot(x, y, color='#00ffcc', lw=3, label='Fitted Truth Curve')
        
        # 标记关键战略基准线
        ax.axvline(prior, color='#ff4b4b', linestyle='--', lw=2, label=f'Prior Logic: {prior:.2f}')
        ax.axvline(mean, color='#f6ff00', linestyle='-', lw=2, label=f'Final Truth Mean: {mean:.2f}')
        ax.axvline(mean, color='#00ffcc', linestyle='-', lw=2, label=f'std: {std:.2f}')
        ax.set_title("Xuanji Strategic Audit: Truth Distribution (FRE)", color='white', fontsize=14, pad=15)
        ax.set_xlabel("Probability of Success (Win Rate)", color='white')
        ax.set_ylabel("Density / Confidence", color='white')
        ax.set_xlim(0, 1)
        ax.grid(color='#444', linestyle=':', alpha=0.4)
        ax.tick_params(colors='white')
        ax.legend(facecolor='#1e1e1e', edgecolor='#444', labelcolor='white')
        
        plt.tight_layout()
        return fig

    def plot_sip_audit(self, physics, title_prefix="Strategic Hope Audit"):
        """
        [子图 1 拆分] 效能对冲审计：基准线 vs 战略杠杆 (SIP Analysis)
        """
        p = physics['p_range']
        ai_thr = physics.get('ai_threshold', 0.5)
        lev_options = physics.get('leverage_options', [1.0, 1.0, 1.0, 1.0])
        all_effs = physics.get('all_efficiencies', [])
        all_aps = physics.get('all_activation_aps', [])
        desc = physics.get('leverage_desc', "基于旧逻辑校准的战略反馈")

    # 创建独立的画布
        fig, ax1 = plt.subplots(figsize=(15, 8))
    
    # 绘制点火阈值线
        ax1.axhline(y=ai_thr, color='red', linestyle='--', alpha=0.4, label=f'Ignition Threshold ({ai_thr})', zorder=1)
    
    # 1. 绘制 L0 基准线 (灰色虚线)
        if len(all_effs) > 3:
            base_eff = all_effs[3]
            base_ap = all_aps[3]
            ax1.plot(p, base_eff, color='#888888', linestyle='--', linewidth=2, label='Baseline (L=1.0)', alpha=0.6, zorder=2)
            if base_ap:
                ax1.scatter(base_ap, ai_thr, color='#888888', s=60, zorder=2)
                ax1.annotate(f"Base AP: {base_ap:.1f}", (base_ap, ai_thr), xytext=(5, -15), 
                         textcoords='offset points', fontsize=9, color='#888888')

    # 2. 循环绘制 L1-L3 战略杠杆曲线
        colors = ['#FFD700', '#FF8C00', '#FF4500'] 
        for i in range(min(3, len(all_effs))):
            effs = all_effs[i]
            ap = all_aps[i]
            if effs is None: continue
        
            label = f"战略杠杆 L{i+1}: {lev_options[i]:.2f}"
            ax1.plot(p, effs, color=colors[i], linewidth=3, label=label, alpha=0.9, zorder=3)
        
            if ap:
                ax1.scatter(ap, ai_thr, color=colors[i], s=120, edgecolors='white', zorder=5)
                advance_str = ""
                if len(all_aps) > 3 and all_aps[3]:
                    advance = all_aps[3] - ap
                    advance_str = f"\n(提前: {advance:.1f})"
            
                ax1.annotate(f"AP{i+1}: P={ap:.1f}{advance_str}", (ap, ai_thr), 
                         xytext=(0, 15), textcoords='offset points', 
                         ha='center', fontsize=10, color=colors[i], fontweight='bold')

        ax1.set_title(f"{title_prefix} - 效能对冲 (杠杆前移审计)", fontsize=16, pad=20)
        ax1.set_ylabel("战略效能 (Effectiveness)", fontsize=12)
        ax1.set_xlabel("资源投入压强 (P)", fontsize=12) # 独立画时建议加上 X 轴标签
        ax1.set_ylim(0, 1.1)
        ax1.grid(alpha=0.1)
        ax1.legend(loc='lower right', frameon=True, framealpha=0.9)

        plt.tight_layout()
        return fig
    def plot_resilience_audit(self, physics):
        """
        [子图 2 拆分] 结构韧性审计：系统稳定性 (ERT Analysis)
        """
        p = physics['p_range']
        stabilities = physics['stabilities'] 
        bp_thr = physics['applied_threshold']
        bp = physics['break_point']

    # 创建独立的画布
        fig, ax2 = plt.subplots(figsize=(15, 6))

        ax2.plot(p, stabilities, color='#00FFCC', linewidth=3, label='System Stability')
        ax2.axhline(y=bp_thr, color='#FF3366', linestyle=':', linewidth=2, label='Collapse Line')
    
    # 填充崩溃区
        ax2.fill_between(p, 0, stabilities, where=(np.array(stabilities) < bp_thr), 
                     color='#FF3366', alpha=0.15, label='Collapse Zone')

        if bp and bp < max(p):
            ax2.scatter(bp, bp_thr, color='#FF3366', s=120, zorder=5)
            ax2.annotate(f"战略崩溃点 BP: P={bp:.1f}", (bp, bp_thr), 
                     xytext=(15, 15), textcoords='offset points', 
                     arrowprops=dict(arrowstyle='->', color='#FF3366'),
                     color='#FF3366', fontweight='bold')

        ax2.set_title(f"结构稳定性审计 (现实阻力对冲)", fontsize=14)
        ax2.set_xlabel("资源投入压强 (P)", fontsize=12)
        ax2.set_ylabel("系统稳定性 (%)", fontsize=12)
        ax2.set_ylim(0, 110)
        ax2.grid(alpha=0.1)
        ax2.legend(loc='upper right')

        return fig
    # visualizer.py 增量更新