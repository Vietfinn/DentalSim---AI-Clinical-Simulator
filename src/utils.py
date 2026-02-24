import json
import streamlit as st


@st.cache_data
def load_data(filepath="data/diseases.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Lỗi: Không tìm thấy file dữ liệu tại {filepath}")
        return []


def load_css():
    st.markdown(
        """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1e293b;
        }

        /* Ẩn Header mặc định */
        header {visibility: hidden;}
        
        /* Nền App */
        .stApp { background-color: #f8fafc; }

        /* --- 1. APP HEADER (Trang chủ) --- */
        .app-header {
            display: flex;
            align-items: center;
            background: white;
            padding: 20px 30px;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            border-bottom: 3px solid #3b82f6;
        }
        .logo-img {
            width: 64px;
            height: 64px;
            margin-right: 20px;
        }
        .brand-name {
            font-size: 32px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.2;
        }
        .slogan {
            font-size: 16px;
            color: #64748b;
            font-weight: 500;
            margin-left: 20px;
            padding-left: 20px;
            border-left: 2px solid #e2e8f0;
            font-style: italic;
        }

        /* --- 2. HERO SECTION (Lợi ích web) --- */
        .hero-box {
            background: white;
            padding: 30px;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
            text-align: center;
            height: 100%;
            transition: transform 0.2s;
        }
        .hero-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
        .hero-icon {
            font-size: 40px;
            margin-bottom: 15px;
            display: block;
        }
        .hero-title {
            font-size: 18px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        }
        .hero-desc {
            font-size: 14px;
            color: #64748b;
            line-height: 1.5;
        }

        /* --- 3. COMPACT PATIENT CARD (Hồ sơ gọn bên trái) --- */
        .patient-compact {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 12px 12px 0 0; /* Bo góc trên */
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .patient-details {
            background: white;
            padding: 15px;
            border: 1px solid #e2e8f0;
            border-top: none;
            border-radius: 0 0 12px 12px; /* Bo góc dưới */
            margin-bottom: 20px;
            font-size: 14px;
        }

        /* --- 4. CHAT INTERFACE --- */
        [data-testid="stChatMessage"] {
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        [data-testid="stChatMessageUser"] {
            background-color: #eff6ff;
        }

        /* --- 5. CLINICAL DATA BOX (Bên phải) --- */
        .clinical-box {
            background: white;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #f1f5f9;
            border-right: 1px solid #e2e8f0;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def render_app_header():
    """Header Trang Chủ với Logo + Tên + Slogan"""
    icon_url = "https://cdn-icons-png.flaticon.com/512/4996/4996232.png"
    st.markdown(
        f"""
    <div class="app-header">
        <img src="{icon_url}" class="logo-img">
        <div>
            <div class="brand-name">DENTALSIM</div>
            <div style="font-size: 14px; color: #3b82f6; font-weight: 600;">PROFESSIONAL EDITION</div>
        </div>
        <div class="slogan">
            "Nâng tầm kỹ năng lâm sàng - Kiến tạo tương lai Nha khoa"
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
