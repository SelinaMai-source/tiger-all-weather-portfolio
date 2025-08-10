#!/usr/bin/env python3
"""
🐯 Tiger All Weather Portfolio - 部署检查脚本

检查所有必要的配置和依赖，确保Streamlit Cloud部署成功
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 9:
        print("   ✅ Python版本符合要求")
        return True
    else:
        print("   ❌ Python版本过低，需要3.9+")
        return False

def check_required_packages():
    """检查必需的包"""
    print("\n📦 检查必需的包...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'plotly', 'yfinance',
        'requests', 'beautifulsoup4', 'lxml', 'fredapi'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - 缺失")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   缺失的包: {', '.join(missing_packages)}")
        return False
    else:
        print("   ✅ 所有必需的包都已安装")
        return True

def check_project_structure():
    """检查项目结构"""
    print("\n📁 检查项目结构...")
    
    current_dir = Path.cwd()
    required_files = [
        'interactive_portfolio_app.py',
        'requirements.txt',
        '.streamlit/config.toml'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = current_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - 缺失")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n   缺失的文件: {', '.join(missing_files)}")
        return False
    else:
        print("   ✅ 项目结构完整")
        return True

def check_streamlit_config():
    """检查Streamlit配置"""
    print("\n⚙️ 检查Streamlit配置...")
    
    config_file = Path('.streamlit/config.toml')
    if config_file.exists():
        print("   ✅ .streamlit/config.toml 存在")
        
        # 检查关键配置
        config_content = config_file.read_text()
        if 'headless = true' in config_content:
            print("   ✅ headless模式已启用")
        else:
            print("   ⚠️  headless模式未启用")
            
        if 'enableCORS = false' in config_content:
            print("   ✅ CORS已禁用")
        else:
            print("   ⚠️  CORS未禁用")
    else:
        print("   ❌ .streamlit/config.toml 缺失")
        return False
    
    return True

def check_requirements():
    """检查requirements.txt"""
    print("\n📋 检查requirements.txt...")
    
    req_file = Path('requirements.txt')
    if req_file.exists():
        print("   ✅ requirements.txt 存在")
        
        # 检查关键依赖
        req_content = req_file.read_text()
        key_deps = ['streamlit', 'pandas', 'numpy', 'plotly']
        
        for dep in key_deps:
            if dep in req_content:
                print(f"   ✅ {dep} 已包含")
            else:
                print(f"   ❌ {dep} 未包含")
        
        return True
    else:
        print("   ❌ requirements.txt 缺失")
        return False

def check_main_app():
    """检查主应用文件"""
    print("\n🚀 检查主应用文件...")
    
    app_file = Path('interactive_portfolio_app.py')
    if app_file.exists():
        print("   ✅ interactive_portfolio_app.py 存在")
        
        # 尝试导入主应用
        try:
            sys.path.insert(0, str(Path.cwd()))
            from interactive_portfolio_app import main
            print("   ✅ 主应用可以正常导入")
            return True
        except Exception as e:
            print(f"   ❌ 主应用导入失败: {e}")
            return False
    else:
        print("   ❌ interactive_portfolio_app.py 缺失")
        return False

def check_git_status():
    """检查Git状态"""
    print("\n🔧 检查Git状态...")
    
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            print("   ⚠️  有未提交的更改")
            print(f"   更改内容:\n{result.stdout}")
            return False
        else:
            print("   ✅ 工作目录干净")
            return True
    except subprocess.CalledProcessError:
        print("   ❌ Git命令执行失败")
        return False

def main():
    """主检查函数"""
    print("🐯 Tiger All Weather Portfolio - 部署检查")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_required_packages,
        check_project_structure,
        check_streamlit_config,
        check_requirements,
        check_main_app,
        check_git_status
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"   ❌ 检查失败: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 检查结果汇总:")
    
    passed = sum(results)
    total = len(results)
    
    for i, (check, result) in enumerate(zip(checks, results)):
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {i+1}. {check.__name__}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 项检查通过")
    
    if passed == total:
        print("🎉 所有检查都通过了！可以开始部署到Streamlit Cloud")
        print("\n🚀 下一步:")
        print("   1. 访问 https://share.streamlit.io/")
        print("   2. 使用GitHub账号登录")
        print("   3. 选择仓库: SelinaMai-source/tiger-all-weather-portfolio")
        print("   4. 设置主文件: interactive_portfolio_app.py")
        print("   5. 点击 Deploy!")
    else:
        print("⚠️  请先解决上述问题，然后再尝试部署")
    
    return passed == total

if __name__ == "__main__":
    main()
