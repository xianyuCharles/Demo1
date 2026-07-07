"""
Demo 1: 订单数据自动化处理系统
主入口脚本

使用方法：
1. 将CSV文件放入 input/ 文件夹
2. 运行本脚本
3. 查看 output/ 文件夹中的结果

功能：
- 读取订单CSV → 自动清洗脏数据
- 生成清洗后订单明细
- 生成每日/品类/渠道/地区汇总
- 生成HTML可视化销售日报看板
- 生成企微/钉钉通知文案
"""
import os
import sys
from pathlib import Path

# 兼容PyInstaller打包后的路径
if getattr(sys, 'frozen', False):
    # 打包后：exe所在目录为工作目录
    BASE_DIR = Path(sys.executable).parent
else:
    # 开发时：项目根目录
    BASE_DIR = Path(__file__).parent.parent
    # 开发时需要添加模块搜索路径
    sys.path.insert(0, str(BASE_DIR))

os.chdir(BASE_DIR)

from modules.cleaner import DataCleaner
from modules.analyzer import DataAnalyzer
from modules.reporter import ReportGenerator
from modules.notifier import Notifier


def main():
    """主处理流程"""
    print("=" * 60)
    print("📊 Demo 1: 订单数据自动化处理系统")
    print("=" * 60)
    
    # 检查输入文件
    input_dir = Path('input')
    if not input_dir.exists():
        print(f"✗ 输入目录不存在: {input_dir}")
        return
    
    # 查找CSV文件
    csv_files = list(input_dir.glob('*.csv'))
    if not csv_files:
        print(f"✗ 未找到CSV文件，请将文件放入 {input_dir}/ 目录")
        return
    
    print(f"\n找到 {len(csv_files)} 个CSV文件:")
    for f in csv_files:
        print(f"  - {f.name}")
    
    # 初始化模块
    cleaner = DataCleaner()
    analyzer = DataAnalyzer()
    reporter = ReportGenerator('output')
    notifier = Notifier()
    
    # 读取订单数据
    order_file = None
    for f in csv_files:
        if '订单' in f.name or 'order' in f.name.lower():
            order_file = f
            break
    
    if not order_file:
        order_file = csv_files[0]  # 默认使用第一个文件
    
    print(f"\n正在处理: {order_file.name}")
    df_orders = cleaner.read_csv(order_file)
    
    # 数据清洗
    df_cleaned, clean_stats = cleaner.clean_order_data(df_orders)
    
    if df_cleaned.empty:
        print("✗ 清洗后无有效数据，终止处理")
        return
    
    # 保存清洗后的明细
    reporter.save_csv(df_cleaned, '清洗明细.csv')
    
    # 数据分析
    print("\n=== 开始数据分析 ===")
    daily = analyzer.analyze_daily_sales(df_cleaned)
    category = analyzer.analyze_by_category(df_cleaned)
    channel = analyzer.analyze_by_channel(df_cleaned)
    region = analyzer.analyze_by_region(df_cleaned)
    
    # 保存汇总报表
    print("\n=== 保存报表 ===")
    if not daily.empty:
        reporter.save_csv(daily, '每日汇总.csv')
    if not category.empty:
        reporter.save_csv(category, '品类汇总.csv')
    if not channel.empty:
        reporter.save_csv(channel, '渠道汇总.csv')
    if not region.empty:
        reporter.save_csv(region, '地区汇总.csv')
    
    # 生成摘要
    summary = analyzer.generate_summary(df_cleaned, clean_stats)
    
    # 生成HTML看板
    print("\n=== 生成可视化看板 ===")
    reporter.generate_html_dashboard(summary, daily, category, channel, region)
    
    # 生成通知文案
    print("\n=== 生成通知文案 ===")
    notifier.generate_all(summary)
    
    # 完成
    print("\n" + "=" * 60)
    print("✅ 处理完成！")
    print("=" * 60)
    print(f"\n📁 输出目录: output/")
    print("  - 清洗明细.csv")
    if not daily.empty:
        print("  - 每日汇总.csv")
    if not category.empty:
        print("  - 品类汇总.csv")
    if not channel.empty:
        print("  - 渠道汇总.csv")
    if not region.empty:
        print("  - 地区汇总.csv")
    print("  - 日报看板.html")
    print("  - 企微通知文案.txt")
    print("  - 钉钉通知文案.txt")
    print("\n提示: 打开 日报看板.html 查看可视化报表")
    print("=" * 60)
    
    # 保存异常清单
    if clean_stats['错误数'] > 0 or clean_stats['警告数'] > 0:
        with open('output/异常清单.txt', 'w', encoding='utf-8') as f:
            f.write("=== 数据异常清单 ===\n\n")
            if clean_stats['错误详情']:
                f.write("【错误】\n")
                for err in clean_stats['错误详情']:
                    f.write(f"  - {err}\n")
            if clean_stats['警告详情']:
                f.write("\n【警告】\n")
                for warn in clean_stats['警告详情']:
                    f.write(f"  - {warn}\n")
        print("  - 异常清单.txt")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n✗ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
