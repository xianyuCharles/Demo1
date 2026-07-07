"""
数据分析模块 - 3个Demo共享
负责：数据汇总、统计、分组分析
"""
import pandas as pd
from typing import Dict, List
from datetime import datetime


class DataAnalyzer:
    """数据分析器"""
    
    def analyze_daily_sales(self, df: pd.DataFrame) -> pd.DataFrame:
        """按日期汇总销售数据"""
        if '日期' not in df.columns or '金额' not in df.columns:
            print("⚠ 缺少日期或金额列，无法生成日报")
            return pd.DataFrame()
        
        # 按日期分组统计
        daily = df.groupby('日期').agg({
            '金额': ['sum', 'count', 'mean'],
            '订单号': 'nunique'
        }).reset_index()
        
        # 重命名列
        daily.columns = ['日期', '销售总额', '订单数', '平均客单价', '有效订单数']
        daily['销售总额'] = daily['销售总额'].round(2)
        daily['平均客单价'] = daily['平均客单价'].round(2)
        
        print(f"✓ 日报生成: {len(daily)} 天数据")
        return daily
    
    def analyze_by_category(self, df: pd.DataFrame) -> pd.DataFrame:
        """按品类汇总"""
        if '品类' not in df.columns or '金额' not in df.columns:
            return pd.DataFrame()
        
        category = df.groupby('品类').agg({
            '金额': ['sum', 'count'],
            '订单号': 'nunique'
        }).reset_index()
        
        category.columns = ['品类', '销售总额', '商品数量', '订单数']
        category['销售总额'] = category['销售总额'].round(2)
        category = category.sort_values('销售总额', ascending=False)
        
        print(f"✓ 品类分析: {len(category)} 个品类")
        return category
    
    def analyze_by_channel(self, df: pd.DataFrame) -> pd.DataFrame:
        """按渠道汇总"""
        if '渠道' not in df.columns or '金额' not in df.columns:
            return pd.DataFrame()
        
        channel = df.groupby('渠道').agg({
            '金额': ['sum', 'count'],
            '订单号': 'nunique'
        }).reset_index()
        
        channel.columns = ['渠道', '销售总额', '订单数', '有效订单数']
        channel['销售总额'] = channel['销售总额'].round(2)
        channel = channel.sort_values('销售总额', ascending=False)
        
        print(f"✓ 渠道分析: {len(channel)} 个渠道")
        return channel
    
    def analyze_by_region(self, df: pd.DataFrame) -> pd.DataFrame:
        """按地区汇总"""
        if '地区' not in df.columns or '金额' not in df.columns:
            return pd.DataFrame()
        
        region = df.groupby('地区').agg({
            '金额': ['sum', 'count'],
            '订单号': 'nunique'
        }).reset_index()
        
        region.columns = ['地区', '销售总额', '订单数', '有效订单数']
        region['销售总额'] = region['销售总额'].round(2)
        region = region.sort_values('销售总额', ascending=False)
        
        print(f"✓ 地区分析: {len(region)} 个地区")
        return region
    
    def generate_summary(self, df: pd.DataFrame, clean_stats: Dict) -> Dict:
        """生成总体摘要"""
        summary = {
            '生成时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '总订单数': len(df),
            '销售总额': df['金额'].sum() if '金额' in df.columns else 0,
            '平均客单价': df['金额'].mean() if '金额' in df.columns else 0,
            '日期范围': f"{df['日期'].min()} ~ {df['日期'].max()}" if '日期' in df.columns else '无',
            '数据质量': {
                '错误数': clean_stats.get('错误数', 0),
                '警告数': clean_stats.get('警告数', 0)
            }
        }
        
        # 四舍五入
        summary['销售总额'] = round(summary['销售总额'], 2)
        summary['平均客单价'] = round(summary['平均客单价'], 2)
        
        return summary
