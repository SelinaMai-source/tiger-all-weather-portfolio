import streamlit as st
import os
import sys

st.set_page_config(page_title="模块导入测试", page_icon="🧪")

st.title("🧪 模块导入测试")

# 显示环境信息
st.write("### 环境信息")
st.write(f"当前工作目录: {os.getcwd()}")
st.write(f"Python版本: {sys.version}")
st.write(f"Python路径: {sys.executable}")

# 显示项目结构
st.write("### 项目结构")
current_dir = os.path.dirname(os.path.abspath(__file__))
st.write(f"当前文件目录: {current_dir}")

# 列出目录内容
try:
    files = os.listdir(current_dir)
    st.write("当前目录文件:")
    for file in files:
        st.write(f"- {file}")
except Exception as e:
    st.error(f"无法读取目录: {e}")

# 测试导入
st.write("### 模块导入测试")

# 测试基本面分析
st.write("**测试基本面分析模块:**")
try:
    sys.path.append(current_dir)
    from fundamental_analysis.equities.fetch_equity_data import screen_vm_candidates
    st.success("✅ 基本面分析模块导入成功")
    
    # 测试函数调用
    try:
        result = screen_vm_candidates()
        st.success(f"✅ 函数调用成功，返回 {len(result)} 只股票")
    except Exception as e:
        st.error(f"❌ 函数调用失败: {e}")
        
except ImportError as e:
    st.error(f"❌ 基本面分析模块导入失败: {e}")
    st.write("尝试其他导入方式...")
    
    try:
        # 尝试直接导入
        import fundamental_analysis.equities.fetch_equity_data as fe
        st.success("✅ 使用别名导入成功")
        screen_vm_candidates = fe.screen_vm_candidates
    except Exception as e2:
        st.error(f"❌ 别名导入也失败: {e2}")

# 测试技术分析
st.write("**测试技术分析模块:**")
try:
    from technical_analysis.technical_signals import TechnicalAnalysisManager
    st.success("✅ 技术分析模块导入成功")
    
    # 测试类实例化
    try:
        tech_manager = TechnicalAnalysisManager()
        st.success("✅ 技术分析管理器实例化成功")
    except Exception as e:
        st.error(f"❌ 实例化失败: {e}")
        
except ImportError as e:
    st.error(f"❌ 技术分析模块导入失败: {e}")

st.write("### 测试完成")
