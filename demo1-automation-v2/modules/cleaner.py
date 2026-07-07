"""
数据清洗模块 - 3个Demo共享
负责：数据读取、清洗、去重、异常检测
"""
import pandas as pd
from typing import Dict, List, Tuple
import re


class DataCleaner:
    """数据清洗器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def read_csv(self, file_path: str) -> pd.DataFrame:
        """读取CSV文件"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            print(f"✓ 读取成功: {file_path}，共 {len(df)} 行")
            return df
        except Exception as e:
            print(f"✗ 读取失败: {e}")
            raise
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """去除重复行"""
        original_count = len(df)
        df_cleaned = df.drop_duplicates(subset=subset)
        removed = original_count - len(df_cleaned)
        
        if removed > 0:
            self.warnings.append(f"发现 {removed} 条重复数据，已自动去除")
            print(f"⚠ 去除重复: {removed} 条")
        
        return df_cleaned
    
    def clean_empty_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理空行"""
        original_count = len(df)
        df_cleaned = df.dropna(how='all')
        removed = original_count - len(df_cleaned)
        
        if removed > 0:
            self.warnings.append(f"发现 {removed} 行空数据，已清理")
            print(f"⚠ 清理空行: {removed} 行")
        
        return df_cleaned
    
    def validate_phone(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """验证手机号格式"""
        if column not in df.columns:
            return df
        
        def is_valid_phone(phone):
            if pd.isna(phone):
                return False
            phone_str = str(phone).strip()
            # 中国大陆手机号：1开头，11位数字
            return bool(re.match(r'^1[3-9]\d{9}$', phone_str))
        
        invalid_mask = ~df[column].apply(is_valid_phone)
        invalid_count = invalid_mask.sum()
        
        if invalid_count > 0:
            self.errors.append(f"{column} 列发现 {invalid_count} 个无效手机号")
            print(f"✗ 无效手机号: {invalid_count} 个")
        
        return df
    
    def validate_amount(self, df: pd.DataFrame, column: str, min_val: float = 0, max_val: float = 1000000) -> pd.DataFrame:
        """验证金额范围"""
        if column not in df.columns:
            return df
        
        # 转换为数值
        df[column] = pd.to_numeric(df[column], errors='coerce')
        
        # 检查异常值
        invalid_mask = (df[column] < min_val) | (df[column] > max_val) | df[column].isna()
        invalid_count = invalid_mask.sum()
        
        if invalid_count > 0:
            self.errors.append(f"{column} 列发现 {invalid_count} 个异常金额（<{min_val} 或 >{max_val}）")
            print(f"✗ 异常金额: {invalid_count} 个")
        
        return df
    
    def validate_product_code(self, df: pd.DataFrame, column: str, valid_codes: List[str] = None) -> pd.DataFrame:
        """验证商品编号"""
        if column not in df.columns:
            return df
        
        if valid_codes:
            invalid_mask = ~df[column].isin(valid_codes)
            invalid_count = invalid_mask.sum()
            
            if invalid_count > 0:
                self.errors.append(f"{column} 列发现 {invalid_count} 个未知商品编号")
                print(f"✗ 未知商品编号: {invalid_count} 个")
        
        return df
    
    def clean_order_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """清洗订单数据（Demo 1主流程）"""
        print("\n=== 开始清洗订单数据 ===")
        
        # 1. 清理空行
        df = self.clean_empty_rows(df)
        
        # 2. 去重（按订单号）
        if '订单号' in df.columns:
            df = self.remove_duplicates(df, subset=['订单号'])
        
        # 3. 验证手机号
        if '手机号' in df.columns:
            df = self.validate_phone(df, '手机号')
        
        # 4. 验证金额
        if '金额' in df.columns:
            df = self.validate_amount(df, '金额')
        
        # 5. 验证商品编号（如果有商品信息表）
        # valid_codes 可以从商品信息表读取
        
        # 统计清洗结果
        stats = {
            '总行数': len(df),
            '错误数': len(self.errors),
            '警告数': len(self.warnings),
            '错误详情': self.errors,
            '警告详情': self.warnings
        }
        
        print(f"\n✓ 清洗完成: {stats['总行数']} 行有效数据")
        return df, stats
