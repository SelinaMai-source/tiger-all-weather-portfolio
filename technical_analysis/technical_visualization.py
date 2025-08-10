# technical_visualization.py
"""
技术分析可视化模块
提供丰富的图表和分析功能
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TechnicalVisualization:
    """技术分析可视化类"""
    
    def __init__(self):
        """初始化可视化类"""
        self.colors = {
            'buy': '#28a745',
            'sell': '#dc3545',
            'hold': '#ffc107',
            'equities': '#1f77b4',
            'bonds': '#ff7f0e',
            'commodities': '#2ca02c',
            'golds': '#d62728'
        }
    
    def create_signals_dashboard(self, technical_manager):
        """创建技术信号仪表板"""
        if not technical_manager.all_signals:
            return None
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('信号分布', '资产类别信号数量', '信号强度分布', '信号时间分布'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "scatter"}]]
        )
        
        # 1. 信号分布饼图
        summary = technical_manager.get_trading_summary()
        signal_counts = [summary['buy_signals'], summary['sell_signals'], summary['hold_signals']]
        signal_labels = ['买入', '卖出', '持有']
        
        fig.add_trace(
            go.Pie(
                labels=signal_labels,
                values=signal_counts,
                name="信号分布",
                marker_colors=[self.colors['buy'], self.colors['sell'], self.colors['hold']]
            ),
            row=1, col=1
        )
        
        # 2. 资产类别信号数量柱状图
        asset_signals = []
        asset_names = []
        for asset_class, signals in technical_manager.all_signals.items():
            if signals is not None and not signals.empty:
                asset_signals.append(len(signals))
                asset_names.append(asset_class.title())
        
        fig.add_trace(
            go.Bar(
                x=asset_names,
                y=asset_signals,
                name="资产类别信号",
                marker_color=[self.colors.get(asset.lower(), '#6c757d') for asset in asset_names]
            ),
            row=1, col=2
        )
        
        # 3. 信号强度分布直方图
        all_strengths = []
        for signals in technical_manager.all_signals.values():
            if signals is not None and not signals.empty and 'strength' in signals.columns:
                all_strengths.extend(signals['strength'].dropna().tolist())
        
        if all_strengths:
            fig.add_trace(
                go.Histogram(
                    x=all_strengths,
                    name="信号强度分布",
                    nbinsx=20,
                    marker_color='#17a2b8'
                ),
                row=2, col=1
            )
        
        # 4. 信号时间分布散点图
        all_timestamps = []
        all_strengths_time = []
        for asset_class, signals in technical_manager.all_signals.items():
            if signals is not None and not signals.empty and 'timestamp' in signals.columns:
                for _, signal in signals.iterrows():
                    if pd.notna(signal['timestamp']):
                        all_timestamps.append(signal['timestamp'])
                        all_strengths_time.append(signal.get('strength', 0))
        
        if all_timestamps:
            fig.add_trace(
                go.Scatter(
                    x=all_timestamps,
                    y=all_strengths_time,
                    mode='markers',
                    name="信号时间分布",
                    marker=dict(
                        size=8,
                        color=all_strengths_time,
                        colorscale='Viridis',
                        showscale=True
                    )
                ),
                row=2, col=2
            )
        
        # 更新布局
        fig.update_layout(
            height=600,
            title_text="技术分析信号仪表板",
            showlegend=True
        )
        
        return fig
    
    def create_asset_class_signals_chart(self, technical_manager, asset_class):
        """创建特定资产类别的信号图表"""
        signals = technical_manager.get_asset_class_signals(asset_class)
        if signals.empty:
            return None
        
        # 创建子图
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(f'{asset_class.title()} 信号分布', f'{asset_class.title()} 信号强度排名'),
            vertical_spacing=0.1
        )
        
        # 1. 信号分布饼图
        if 'signal' in signals.columns:
            signal_dist = signals['signal'].value_counts()
            fig.add_trace(
                go.Pie(
                    labels=signal_dist.index,
                    values=signal_dist.values,
                    name="信号分布",
                    marker_colors=[self.colors.get(signal.lower(), '#6c757d') for signal in signal_dist.index]
                ),
                row=1, col=1
            )
        
        # 2. 信号强度排名柱状图
        if 'strength' in signals.columns:
            top_signals = signals.nlargest(10, 'strength')
            fig.add_trace(
                go.Bar(
                    x=top_signals['ticker'],
                    y=top_signals['strength'],
                    name="信号强度",
                    marker_color='#17a2b8'
                ),
                row=2, col=1
            )
        
        # 更新布局
        fig.update_layout(
            height=500,
            title_text=f"{asset_class.title()} 技术分析详情",
            showlegend=False
        )
        
        return fig
    
    def create_signal_strength_heatmap(self, technical_manager):
        """创建信号强度热力图"""
        # 准备数据
        asset_classes = []
        signal_types = []
        strength_values = []
        
        for asset_class, signals in technical_manager.all_signals.items():
            if signals is not None and not signals.empty and 'signal' in signals.columns and 'strength' in signals.columns:
                for signal_type in ['BUY', 'SELL', 'HOLD']:
                    asset_signals = signals[signals['signal'] == signal_type]
                    if not asset_signals.empty:
                        avg_strength = asset_signals['strength'].mean()
                        asset_classes.append(asset_class.title())
                        signal_types.append(signal_type)
                        strength_values.append(avg_strength)
        
        if not strength_values:
            return None
        
        # 创建热力图
        df_heatmap = pd.DataFrame({
            'Asset Class': asset_classes,
            'Signal Type': signal_types,
            'Strength': strength_values
        })
        
        # 透视表
        pivot_table = df_heatmap.pivot(index='Asset Class', columns='Signal Type', values='Strength')
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='Viridis',
            text=np.round(pivot_table.values, 2),
            texttemplate="%{text}",
            textfont={"size": 12},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="信号强度热力图",
            xaxis_title="信号类型",
            yaxis_title="资产类别",
            height=400
        )
        
        return fig
    
    def create_signal_timeline(self, technical_manager):
        """创建信号时间线图"""
        # 收集所有信号的时间信息
        timeline_data = []
        
        for asset_class, signals in technical_manager.all_signals.items():
            if signals is not None and not signals.empty and 'timestamp' in signals.columns:
                for _, signal in signals.iterrows():
                    if pd.notna(signal['timestamp']):
                        timeline_data.append({
                            'asset_class': asset_class,
                            'ticker': signal.get('ticker', 'N/A'),
                            'signal': signal.get('signal', 'N/A'),
                            'strength': signal.get('strength', 0),
                            'timestamp': signal['timestamp']
                        })
        
        if not timeline_data:
            return None
        
        df_timeline = pd.DataFrame(timeline_data)
        
        # 创建时间线图
        fig = go.Figure()
        
        for asset_class in df_timeline['asset_class'].unique():
            asset_data = df_timeline[df_timeline['asset_class'] == asset_class]
            
            for signal_type in ['BUY', 'SELL', 'HOLD']:
                signal_data = asset_data[asset_data['signal'] == signal_type]
                if not signal_data.empty:
                    fig.add_trace(go.Scatter(
                        x=signal_data['timestamp'],
                        y=signal_data['strength'],
                        mode='markers',
                        name=f"{asset_class.title()} - {signal_type}",
                        marker=dict(
                            size=10,
                            symbol='circle',
                            color=self.colors.get(signal_type.lower(), '#6c757d')
                        ),
                        text=signal_data['ticker'],
                        hovertemplate="<b>%{text}</b><br>" +
                                    "时间: %{x}<br>" +
                                    "强度: %{y:.2f}<br>" +
                                    "<extra></extra>"
                    ))
        
        fig.update_layout(
            title="技术信号时间线",
            xaxis_title="时间",
            yaxis_title="信号强度",
            height=500,
            hovermode='closest'
        )
        
        return fig
    
    def create_performance_metrics(self, technical_manager):
        """创建性能指标图表"""
        # 计算各种性能指标
        metrics = {}
        
        for asset_class, signals in technical_manager.all_signals.items():
            if signals is not None and not signals.empty:
                asset_metrics = {
                    'total_signals': len(signals),
                    'avg_strength': 0,
                    'signal_distribution': {},
                    'high_confidence_signals': 0
                }
                
                if 'strength' in signals.columns:
                    asset_metrics['avg_strength'] = signals['strength'].mean()
                    asset_metrics['high_confidence_signals'] = len(signals[signals['strength'] >= 0.7])
                
                if 'signal' in signals.columns:
                    asset_metrics['signal_distribution'] = signals['signal'].value_counts().to_dict()
                
                metrics[asset_class] = asset_metrics
        
        # 创建性能指标图表
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('信号数量对比', '平均信号强度', '高置信度信号比例', '信号类型分布'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        # 1. 信号数量对比
        asset_names = list(metrics.keys())
        signal_counts = [metrics[asset]['total_signals'] for asset in asset_names]
        
        fig.add_trace(
            go.Bar(
                x=[asset.title() for asset in asset_names],
                y=signal_counts,
                name="信号数量",
                marker_color=[self.colors.get(asset, '#6c757d') for asset in asset_names]
            ),
            row=1, col=1
        )
        
        # 2. 平均信号强度
        avg_strengths = [metrics[asset]['avg_strength'] for asset in asset_names]
        
        fig.add_trace(
            go.Bar(
                x=[asset.title() for asset in asset_names],
                y=avg_strengths,
                name="平均强度",
                marker_color=[self.colors.get(asset, '#6c757d') for asset in asset_names]
            ),
            row=1, col=2
        )
        
        # 3. 高置信度信号比例
        high_conf_ratios = []
        for asset in asset_names:
            if metrics[asset]['total_signals'] > 0:
                ratio = metrics[asset]['high_confidence_signals'] / metrics[asset]['total_signals']
                high_conf_ratios.append(ratio)
            else:
                high_conf_ratios.append(0)
        
        fig.add_trace(
            go.Bar(
                x=[asset.title() for asset in asset_names],
                y=high_conf_ratios,
                name="高置信度比例",
                marker_color=[self.colors.get(asset, '#6c757d') for asset in asset_names]
            ),
            row=2, col=1
        )
        
        # 4. 总体信号类型分布
        all_signals = []
        all_types = []
        for asset_metrics in metrics.values():
            for signal_type, count in asset_metrics['signal_distribution'].items():
                all_signals.append(count)
                all_types.append(signal_type)
        
        if all_signals:
            fig.add_trace(
                go.Pie(
                    labels=all_types,
                    values=all_signals,
                    name="信号类型分布",
                    marker_colors=[self.colors.get(signal_type.lower(), '#6c757d') for signal_type in all_types]
                ),
                row=2, col=2
            )
        
        # 更新布局
        fig.update_layout(
            height=600,
            title_text="技术分析性能指标",
            showlegend=False
        )
        
        return fig
    
    def display_all_charts(self, technical_manager):
        """显示所有图表"""
        st.subheader("📊 技术分析可视化")
        
        # 1. 信号仪表板
        dashboard = self.create_signals_dashboard(technical_manager)
        if dashboard:
            st.plotly_chart(dashboard, use_container_width=True)
        
        # 2. 信号强度热力图
        heatmap = self.create_signal_strength_heatmap(technical_manager)
        if heatmap:
            st.plotly_chart(heatmap, use_container_width=True)
        
        # 3. 信号时间线
        timeline = self.create_signal_timeline(technical_manager)
        if timeline:
            st.plotly_chart(timeline, use_container_width=True)
        
        # 4. 性能指标
        performance = self.create_performance_metrics(technical_manager)
        if performance:
            st.plotly_chart(performance, use_container_width=True)
        
        # 5. 各资产类别详细图表
        st.subheader("📈 各资产类别详细分析")
        
        for asset_class in ['equities', 'bonds', 'commodities', 'golds']:
            asset_chart = self.create_asset_class_signals_chart(technical_manager, asset_class)
            if asset_chart:
                st.plotly_chart(asset_chart, use_container_width=True)

def create_technical_visualization():
    """创建技术分析可视化实例"""
    return TechnicalVisualization()

if __name__ == "__main__":
    # 测试可视化功能
    viz = TechnicalVisualization()
    print("✅ 技术分析可视化模块创建成功")
