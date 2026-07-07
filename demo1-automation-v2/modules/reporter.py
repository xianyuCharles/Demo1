"""
报表生成模块 - 3个Demo共享
负责：CSV报表、Excel报表、HTML可视化看板
"""
import pandas as pd
from typing import Dict
from datetime import datetime
import os


class ReportGenerator:
    """报表生成器"""
    
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_csv(self, df: pd.DataFrame, filename: str) -> str:
        """保存为CSV文件"""
        file_path = os.path.join(self.output_dir, filename)
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✓ CSV已保存: {file_path}")
        return file_path
    
    def save_excel(self, df: pd.DataFrame, filename: str, sheet_name: str = '数据') -> str:
        """保存为Excel文件"""
        file_path = os.path.join(self.output_dir, filename)
        df.to_excel(file_path, index=False, sheet_name=sheet_name)
        print(f"✓ Excel已保存: {file_path}")
        return file_path
    
    def generate_html_dashboard(self, summary: Dict, daily: pd.DataFrame, 
                                 category: pd.DataFrame, channel: pd.DataFrame,
                                 region: pd.DataFrame) -> str:
        """生成HTML可视化看板"""
        html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>销售日报看板</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header h1 {
            margin: 0;
            font-size: 32px;
        }
        .header .time {
            margin-top: 10px;
            opacity: 0.9;
        }
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card .label {
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .card .value {
            font-size: 28px;
            font-weight: bold;
            color: #333;
        }
        .card .value.primary {
            color: #667eea;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .section h2 {
            margin-top: 0;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .footer {
            text-align: center;
            color: #999;
            padding: 20px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 销售日报看板</h1>
            <div class="time">生成时间：{生成时间}</div>
        </div>
        
        <div class="summary-cards">
            <div class="card">
                <div class="label">总订单数</div>
                <div class="value">{总订单数}</div>
            </div>
            <div class="card">
                <div class="label">销售总额</div>
                <div class="value primary">¥{销售总额}</div>
            </div>
            <div class="card">
                <div class="label">平均客单价</div>
                <div class="value">¥{平均客单价}</div>
            </div>
            <div class="card">
                <div class="label">数据质量</div>
                <div class="value">{错误数} 错误 / {警告数} 警告</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📅 每日销售趋势</h2>
            {daily_table}
        </div>
        
        <div class="section">
            <h2>📦 品类销售排行</h2>
            {category_table}
        </div>
        
        <div class="section">
            <h2>🏪 渠道销售分布</h2>
            {channel_table}
        </div>
        
        <div class="section">
            <h2>🗺️ 地区销售分布</h2>
            {region_table}
        </div>
        
        <div class="footer">
            由 Demo1 自动化系统生成 | 星亦网络科技工作室
        </div>
    </div>
</body>
</html>
        """
        
        # 生成表格HTML
        daily_table = self._df_to_html_table(daily) if not daily.empty else '<p>暂无数据</p>'
        category_table = self._df_to_html_table(category) if not category.empty else '<p>暂无数据</p>'
        channel_table = self._df_to_html_table(channel) if not channel.empty else '<p>暂无数据</p>'
        region_table = self._df_to_html_table(region) if not region.empty else '<p>暂无数据</p>'
        
        # 使用replace方法避免CSS大括号冲突
        html_content = html_template
        html_content = html_content.replace('{生成时间}', str(summary.get('生成时间', '')))
        html_content = html_content.replace('{总订单数}', str(summary.get('总订单数', 0)))
        html_content = html_content.replace('{销售总额}', str(summary.get('销售总额', 0)))
        html_content = html_content.replace('{平均客单价}', str(summary.get('平均客单价', 0)))
        html_content = html_content.replace('{错误数}', str(summary.get('数据质量', {}).get('错误数', 0)))
        html_content = html_content.replace('{警告数}', str(summary.get('数据质量', {}).get('警告数', 0)))
        html_content = html_content.replace('{daily_table}', daily_table)
        html_content = html_content.replace('{category_table}', category_table)
        html_content = html_content.replace('{channel_table}', channel_table)
        html_content = html_content.replace('{region_table}', region_table)
        
        # 保存文件
        file_path = os.path.join(self.output_dir, '日报看板.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ HTML看板已保存: {file_path}")
        return file_path
    
    def _df_to_html_table(self, df: pd.DataFrame) -> str:
        """将DataFrame转换为HTML表格"""
        if df.empty:
            return '<p>暂无数据</p>'
        
        html = '<table>\n<thead>\n<tr>\n'
        for col in df.columns:
            html += f'<th>{col}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'
        
        for _, row in df.iterrows():
            html += '<tr>\n'
            for val in row:
                html += f'<td>{val}</td>\n'
            html += '</tr>\n'
        
        html += '</tbody>\n</table>'
        return html
