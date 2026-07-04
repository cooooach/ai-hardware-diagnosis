"""
AI 硬件故障诊断助手 - 硬件工程师的智能诊断工具
作者：钟睿恒 | 深圳大学 测控技术与仪器
"""

import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ========== 页面配置 ==========
st.set_page_config(
    page_title="AI 硬件故障诊断助手",
    page_icon="🔧",
    layout="wide",
)

# ========== 自定义样式 ==========
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .main-header h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .result-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #2a2a4a;
    }
    .category-tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        background: #2a2a4a;
        color: #a0a0d0;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #333;
        background-color: #1a1a2e;
        color: #e0e0e0;
    }
    .stTextArea textarea:focus {
        border-color: #667eea;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== 预设故障场景（快捷输入） ==========
PRESET_SCENARIOS = {
    "💡 LED 不亮": "电路板上电后，电源指示灯正常亮，但所有功能LED都不亮，用万用表测过各节点电压都正常，换了新的LED也不亮。",
    "🔌 电源异常": "电路板通电后，5V电源输出只有3.2V左右，负载电流正常，但电压一直上不去，更换电源模块后问题依旧。",
    "📡 信号干扰": "示波器观察到信号线上有约50Hz的周期性毛刺，峰峰值约200mV，影响了ADC采样精度，确认不是示波器探头问题。",
    "🔥 芯片过热": "STM32主控芯片在正常运行5分钟后温度升到65°C以上，手指触碰有明显灼热感，程序运行正常但担心长期可靠性。",
    "🔊 音频噪声": "功放电路输出端有持续的高频嘶嘶声，断开输入信号后噪声依然存在，音量调至最低也无法消除。",
    "🔄 通信失败": "I2C通信时好时坏，有时读取传感器数据正常，有时返回全0xFF，上拉电阻已确认焊接无误，总线速率已降至100kHz仍不行。",
}

# ========== 系统提示词 ==========
SYSTEM_PROMPT = """你是一位拥有20年经验的资深硬件工程师，精通模拟电路、数字电路、嵌入式系统和各类电子测量仪器。

用户会向你描述硬件故障现象，请按以下结构给出专业诊断：

## 🔍 故障分析
- 简要归类故障类型（电源问题/信号完整性问题/元器件故障/焊接装配问题/设计缺陷）
- 分析最可能的2-3个原因，按可能性排序

## 📋 排查步骤
按顺序给出具体排查步骤，每一步包含：
1. 操作内容（用万用表/示波器测哪里）
2. 预期结果
3. 如果不符合预期该怎么办

## 🛠️ 解决方案
给出推荐的修复方案，说明原理

## ⚠️ 注意事项
操作安全提醒，避免二次损坏

要求：
- 用中文回答
- 专业但不晦涩，让有一定基础的硬件工程师能看懂
- 提到具体测量参数和参考值
- 如果能结合测控/仪器专业知识更好"""

# ========== 主界面 ==========
# 顶部标题
st.markdown("""
<div class="main-header">
    <h1>🔧 AI 硬件故障诊断助手</h1>
    <p style="color: #888; font-size: 1.1rem;">基于大语言模型的智能硬件诊断系统 · 输入故障现象，获取专业排查方案</p>
</div>
""", unsafe_allow_html=True)

# 两栏布局
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 描述故障现象")
    
    # 快捷场景选择
    selected_scenario = st.selectbox(
        "💡 快捷场景（可选）",
        ["自定义输入"] + list(PRESET_SCENARIOS.keys()),
        index=0,
        help='选择一个预设场景快速填充，或选择「自定义输入」手动描述'
    )
    
    # 根据选择填充默认文本
    default_text = ""
    if selected_scenario != "自定义输入":
        default_text = PRESET_SCENARIOS[selected_scenario]
    
    user_input = st.text_area(
        "请详细描述故障现象：",
        value=default_text,
        height=200,
        placeholder="例如：电路板上电后电源指示灯亮，但MCU不启动，测3.3V电压只有2.1V...\n\n提示：越详细越好，包括已做的排查、测量数据等",
        label_visibility="collapsed",
    )
    
    # 附加信息
    with st.expander("📎 补充信息（可选）"):
        device_type = st.selectbox("设备类型", ["", "嵌入式系统", "模拟电路", "数字电路", "电源模块", "传感器", "通信接口", "其他"])
        tools_available = st.multiselect("可用仪器", ["万用表", "数字示波器", "信号发生器", "逻辑分析仪", "频谱分析仪", "LCR表", "热成像仪"], default=["万用表", "数字示波器"])
    
    analyze_btn = st.button("🔍 开始诊断", type="primary", use_container_width=True)

with col2:
    st.markdown("### 📊 诊断结果")
    
    if "diagnosis_result" not in st.session_state:
        st.session_state.diagnosis_result = None
    
    if st.session_state.diagnosis_result:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown(st.session_state.diagnosis_result)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info('👈 请在左侧输入故障现象，点击「开始诊断」获取 AI 专业分析')
        
        # 展示功能亮点
        st.markdown("""
        <div style="background: #1a1a2e; border-radius: 12px; padding: 1.5rem; margin-top: 1rem;">
            <h4 style="color: #667eea;">✨ 功能亮点</h4>
            <ul style="color: #a0a0d0; line-height: 2;">
                <li>🔬 结合测控专业知识的深度故障分析</li>
                <li>📋 结构化的排查步骤与预期结果</li>
                <li>🛠️ 可操作的解决方案与原理说明</li>
                <li>⚡ 支持模拟/数字/嵌入式等多种场景</li>
                <li>🎯 基于大语言模型的精准诊断</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ========== 诊断逻辑 ==========
if analyze_btn:
    if not user_input.strip():
        st.error("⚠️ 请输入故障现象描述")
    else:
        # 检查 API Key
        api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
        
        if not api_key:
            st.error("❌ 未配置 API Key，请在 `.env` 文件中设置 `DEEPSEEK_API_KEY`")
        else:
            with st.spinner("🤔 AI 正在分析故障，请稍候..."):
                try:
                    client = OpenAI(api_key=api_key, base_url=api_base)
                    
                    # 构建完整提示
                    full_prompt = f"""故障现象：
{user_input}

设备类型：{device_type if device_type else '未指定'}
可用仪器：{', '.join(tools_available) if tools_available else '万用表'}

请按照系统提示词中的结构给出诊断。"""
                    
                    response = client.chat.completions.create(
                        model=os.getenv("MODEL_NAME", "deepseek-chat"),
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": full_prompt},
                        ],
                        temperature=0.7,
                        max_tokens=2048,
                    )
                    
                    result = response.choices[0].message.content
                    st.session_state.diagnosis_result = result
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ 诊断出错：{str(e)}")
                    st.info("💡 常见原因：API Key 无效、网络问题、或 API 额度不足")

# ========== 底部 ==========
st.markdown("""
<div class="footer">
    <p>AI 硬件故障诊断助手 v1.0 | 深圳大学 测控技术与仪器 钟睿恒</p>
    <p>Powered by DeepSeek + Streamlit</p>
</div>
""", unsafe_allow_html=True)
