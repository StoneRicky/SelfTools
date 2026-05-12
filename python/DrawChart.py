import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei'] 
plt.rcParams['axes.unicode_minus'] = False

def draw_architecture():
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # 1. 标题栏
    ax.add_patch(patches.Rectangle((0, 94), 100, 6, color='#001f3f'))
    plt.text(50, 97, '消化内镜耗材管理系统架构图', color='white', fontsize=20, ha='center', va='center', weight='bold')

    def draw_layer(y_start, height, title, sub_layers, color_bg):
        # 大层背景
        ax.add_patch(patches.Rectangle((2, y_start), 96, height, color=color_bg, alpha=0.9))
        
        # --- 修正点：linespacing 去掉下划线 ---
        plt.text(5.5, y_start + height/2, title, fontsize=18, color='white', 
                 ha='center', va='center', rotation=0, weight='bold', linespacing=1.8)
        
        for i, sub in enumerate(sub_layers):
            sub_y = y_start + (height / len(sub_layers)) * (len(sub_layers) - 1 - i) + 2
            sub_h = (height / len(sub_layers)) - 4
            
            # 子层标题
            plt.text(12.5, sub_y + sub_h/2, sub['name'], fontsize=12, color='#333', 
                     ha='center', va='center', weight='bold')
            
            # 子层模块
            items = sub['items']
            n = len(items)
            spacing = 80 / n
            for j, item in enumerate(items):
                rect_x = 18 + j * spacing
                rect_w = spacing - 2
                
                # 绘制圆角模块
                box = patches.FancyBboxPatch(
                    (rect_x, sub_y), rect_w, sub_h,
                    boxstyle="round,pad=0,rounding_size=1",
                    color='#003366', 
                    mutation_scale=1
                )
                ax.add_patch(box)
                plt.text(rect_x + rect_w/2, sub_y + sub_h/2, item, color='white', 
                         fontsize=10, ha='center', va='center', wrap=True)

    # 2. 绘制各层
    draw_layer(60, 32, "应\n用\n层", [
        {"name": "业务应用", "items": ["基础信息管理", "库存管理", "库存盘点", "采购管理", "统计分析", "系统管理", "合规管理"]},
        {"name": "基础应用", "items": ["基础信息维护", "扫码识别", "报表导出", "数据同步", "日志记录", "密码加密", "异常处理"]}
    ], '#8db4e2')

    draw_layer(32, 25, "支\n撑\n层", [
        {"name": "能力支撑", "items": ["数据存储", "数据整合", "权限管理", "资源管理", "文件服务", "图表服务", "接口服务"]}
    ], '#5b9bd5')

    draw_layer(5, 24, "接\n入\n层", [
        {"name": "外部接入", "items": ["医院HIS系统", "物资管理系统", "USB扫码枪", "文档打印机", "MinIO存储"]}
    ], '#3a5a8c')

    plt.tight_layout()
    # 自动保存一份图片，省得截图了
    # plt.savefig('hospital_arch.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    draw_architecture()