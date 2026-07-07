"""
通知模块 - 3个Demo共享
负责：生成企业微信/钉钉通知文案
"""
from typing import Dict
from datetime import datetime


class Notifier:
    """通知生成器"""
    
    def generate_wechat_message(self, summary: Dict) -> str:
        """生成企业微信通知文案"""
        message = f"""📊 销售日报生成完成

━━━━━━━━━━━━━━
📋 数据概览
━━━━━━━━━━━━━━
• 总订单数：{summary.get('总订单数', 0)} 单
• 销售总额：¥{summary.get('销售总额', 0)}
• 平均客单价：¥{summary.get('平均客单价', 0)}
• 日期范围：{summary.get('日期范围', '无')}

━━━━━━━━━━━━━━
✅ 处理状态
━━━━━━━━━━━━━━
• 错误：{summary.get('数据质量', {}).get('错误数', 0)} 个
• 警告：{summary.get('数据质量', {}).get('警告数', 0)} 个

━━━━━━━━━━━━━━
📁 输出文件
━━━━━━━━━━━━━━
• 清洗明细.csv
• 每日汇总.csv
• 品类汇总.csv
• 渠道汇总.csv
• 地区汇总.csv
• 日报看板.html

━━━━━━━━━━━━━━
生成时间：{summary.get('生成时间', '')}
        """
        
        # 保存到文件
        with open('output/企微通知文案.txt', 'w', encoding='utf-8') as f:
            f.write(message)
        
        print("✓ 企微通知文案已生成")
        return message
    
    def generate_dingtalk_message(self, summary: Dict) -> str:
        """生成钉钉通知文案"""
        message = f"""## 📊 销售日报生成完成

### 数据概览
- **总订单数**：{summary.get('总订单数', 0)} 单
- **销售总额**：¥{summary.get('销售总额', 0)}
- **平均客单价**：¥{summary.get('平均客单价', 0)}
- **日期范围**：{summary.get('日期范围', '无')}

### 处理状态
- 错误：{summary.get('数据质量', {}).get('错误数', 0)} 个
- 警告：{summary.get('数据质量', {}).get('警告数', 0)} 个

### 输出文件
- 清洗明细.csv
- 每日汇总.csv
- 品类汇总.csv
- 渠道汇总.csv
- 地区汇总.csv
- 日报看板.html

---
生成时间：{summary.get('生成时间', '')}
        """
        
        # 保存到文件
        with open('output/钉钉通知文案.txt', 'w', encoding='utf-8') as f:
            f.write(message)
        
        print("✓ 钉钉通知文案已生成")
        return message
    
    def generate_all(self, summary: Dict):
        """生成所有通知文案"""
        self.generate_wechat_message(summary)
        self.generate_dingtalk_message(summary)
