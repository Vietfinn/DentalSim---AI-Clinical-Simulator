import streamlit as st
import random
import time
from src.utils import load_data, load_css
from src.ai_service import DentalAI
import base64
import os

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="DentalSim Professional",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load dữ liệu
diseases = load_data("data/diseases.json")

# --- 2. CSS STYLING (MODERN & NATIVE HTML CHAT) ---
st.markdown(
    """
<style>
    /* Import Font Manrope & Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@600;700;800&display=swap');
    
    /* GLOBAL TYPOGRAPHY */
    html, body, [class*="css"], .stMarkdown, .stSelectbox {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
        font-size: 18px !important; 
        line-height: 1.6;
    }
    
    h1, h2, h3, h4 { font-family: 'Manrope', sans-serif; color: #0f172a; margin-bottom: 0.5rem; }
    h1 { font-size: 2.5rem !important; font-weight: 800 !important; }
    h3 { font-size: 1.6rem !important; font-weight: 700 !important; }
    
    header {visibility: hidden;}
    .stApp { background-color: #f8fafc; }

    /* ========================================================
       APP HEADER (AI MEDICAL SAAS STYLE - NEURAL WAVES)
       ======================================================== */
    .app-header-wrapper {
        margin-top: -4rem;      
        margin-left: -5rem;     
        margin-right: -5rem;    
        margin-bottom: 40px;
        overflow: hidden; /* Cắt bỏ phần hiệu ứng bị tràn */
    }
    
    .app-header {
        display: flex; 
        justify-content: flex-start;
        align-items: center; 
        /* KÉO LOGO & SLOGAN VỀ GIỮA 1 TÍ BẰNG CÁCH TĂNG PADDING HAI BÊN */
        padding: 35px 12%; 
        position: relative;
        min-height: 125px;
        /* Nền chuyển dần từ trắng sang xanh dương nhạt ở góc phải */
        background: linear-gradient(90deg, #ffffff 40%, #eef6ff 100%);
        border-bottom: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        overflow: hidden;
    }

    /* HIỆU ỨNG 1: ABSTRACT NEURAL LINES (ĐƯỜNG MẠNG LƯỚI AI UỐN CONG) */
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 55%;
        height: 100%;
        /* Vẽ các đường cong Neural & Dots bằng SVG nhúng trực tiếp */
        background-image: url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' viewBox='0 0 800 200' preserveAspectRatio='xMaxYMid slice' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M 0 180 C 200 120, 400 200, 800 50' fill='none' stroke='%2300C8FF' stroke-width='2' stroke-opacity='0.4'/%3E%3Cpath d='M 100 250 C 300 100, 500 50, 800 150' fill='none' stroke='%230F3D91' stroke-width='1.5' stroke-opacity='0.3'/%3E%3Cpath d='M -50 100 C 150 150, 350 0, 800 80' fill='none' stroke='%230F3D91' stroke-width='1' stroke-opacity='0.2'/%3E%3Ccircle cx='200' cy='120' r='3' fill='%230F3D91' fill-opacity='0.5'/%3E%3Ccircle cx='400' cy='200' r='4' fill='%2300C8FF' fill-opacity='0.5'/%3E%3Ccircle cx='300' cy='100' r='2.5' fill='%230F3D91' fill-opacity='0.5'/%3E%3Ccircle cx='500' cy='50' r='3' fill='%230F3D91' fill-opacity='0.4'/%3E%3Ccircle cx='150' cy='150' r='2' fill='%230F3D91' fill-opacity='0.4'/%3E%3Cpath d='M 200 120 L 300 100' fill='none' stroke='%230F3D91' stroke-width='0.5' stroke-opacity='0.3'/%3E%3Cpath d='M 300 100 L 500 50' fill='none' stroke='%230F3D91' stroke-width='0.5' stroke-opacity='0.3'/%3E%3Cpath d='M 400 200 L 500 50' fill='none' stroke='%230F3D91' stroke-width='0.5' stroke-opacity='0.3'/%3E%3C/svg%3E");
        background-size: cover;
        background-position: right center;
        background-repeat: no-repeat;
        z-index: 1;
        pointer-events: none;
    }

    /* HIỆU ỨNG 2: VÙNG ÁNH SÁNG BLUR MỜ & LƯỚI DOT GRID GÓC PHẢI */
    .app-header::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 60%;
        height: 200%;
        background: 
            /* Ánh sáng Cyan nhạt */
            radial-gradient(ellipse at 80% 30%, rgba(0, 200, 255, 0.15) 0%, transparent 50%),
            /* Ánh sáng Navy đậm mờ */
            radial-gradient(ellipse at 100% 70%, rgba(15, 61, 145, 0.1) 0%, transparent 60%),
            /* Lưới Dot Grid */
            radial-gradient(rgba(15, 61, 145, 0.15) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 20px 20px;
        z-index: 0;
        /* Xóa viền gắt của lưới để nó hòa quyện vào nền trắng */
        mask-image: linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%);
        -webkit-mask-image: linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%);
        pointer-events: none;
    }

    /* VÙNG NỘI DUNG HEADER CHÍNH */
    .header-content-container {
        display: flex;
        align-items: center;
        gap: 22px;
        z-index: 10; /* Nằm trên lớp hiệu ứng nền */
        position: relative;
    }

    .app-logo { 
        width: 85px; 
        height: 85px; 
        object-fit: contain;
    } 

    .header-text-group {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .header-top-row {
        display: flex;
        align-items: center;
        margin-bottom: 2px;
    }

    .app-name { 
        font-family: 'Manrope', sans-serif; 
        font-size: 40px; 
        font-weight: 800; 
        color: #0F3D91; /* Xanh Navy Y Khoa */
        line-height: 1; 
        letter-spacing: -0.5px;
    }

    .header-divider {
        width: 1.5px;
        height: 28px;
        background-color: #94a3b8;
        margin: 0 16px;
    }

    /* BADGE CHUẨN SAAS (Bo góc nhẹ, màu tinh tế) */
    .app-badge {
        background-color: #e0e7ff;
        color: #3730a3;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 6px; 
        border: 1px solid #c7d2fe;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    .app-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 500;
        color: #475569;
        margin-top: 4px;
        letter-spacing: -0.2px;
    }

    .app-desc {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #64748b;
        font-weight: 400;
        margin-top: 2px;
    }

    /* --- CONTAINERS & CARDS --- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white; border-radius: 16px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02); padding: 25px;
    }
    
    .feature-card {
        background: white; padding: 18px 20px; border-radius: 16px; 
        border: 1px solid #e2e8f0; height: 100%; min-height: 160px; 
        transition: transform 0.2s; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }
    .feature-card:hover {
        transform: translateY(-5px); box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.1); border-color: #3b82f6;
    }
    .card-icon { font-size: 2.6rem; margin-bottom: 10px; display: block; }
    .card-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 6px; color: #1e293b; }
    .card-desc { font-size: 0.95rem; color: #64748b; line-height: 1.5; }

    /* --- PATIENT PROFILE --- */
    .profile-header-bg {
        background: linear-gradient(135deg, #0F3D91 0%, #3b82f6 100%); color: white;
        padding: 25px; border-radius: 12px 12px 0 0;
    }
    .profile-body { 
        padding: 25px; background: white;
        border: 1px solid #cbd5e1; border-top: none; border-radius: 0 0 12px 12px;
    }

    /* --- NÚT BẤM --- */
    div.stButton > button {
        width: 100% !important; 
        border-radius: 12px; height: 60px; font-size: 18px;
        font-weight: 700; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    div[data-baseweb="select"] > div { font-size: 18px; min-height: 55px; }

    /* ========================================================
       NATIVE HTML CHAT UI
       ======================================================== */
    .custom-chat-wrapper {
        display: flex; flex-direction: column; gap: 20px; padding: 10px 5px;
    }
    .chat-row {
        display: flex; align-items: flex-end; width: 100%; gap: 12px;
        animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .chat-row.right { justify-content: flex-end; }
    .chat-row.left { justify-content: flex-start; }
    
    .chat-avatar {
        width: 42px; height: 42px; border-radius: 50%;
        background-color: #ffffff; border: 1px solid #e2e8f0;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; flex-shrink: 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .chat-bubble {
        padding: 14px 20px; border-radius: 20px; max-width: 75%;
        font-size: 17px; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        word-wrap: break-word;
    }
    .user-bubble {
        background-color: #0F3D91; color: white; border-bottom-right-radius: 4px;
    }
    .bot-bubble {
        background-color: #f1f5f9; color: #1e293b;
        border: 1px solid #e2e8f0; border-bottom-left-radius: 4px;
    }
    [data-testid="stChatMessage"] { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. SESSION STATE ---
if "history" not in st.session_state:
    st.session_state.history = []
if "case" not in st.session_state:
    st.session_state.case = None
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False


# Hàm hỗ trợ đọc ảnh và chuyển sang Base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        return ""


# --- 4. HEADER COMPONENT MỚI ---
def render_header():
    logo_path = "assets/images/logo.png"
    base64_logo = get_base64_image(logo_path)

    # Nếu không tìm thấy file logo local, dùng tạm icon răng xanh mượt mà trên mạng
    img_src = (
        f"data:image/png;base64,{base64_logo}"
        if base64_logo
        else "https://cdn-icons-png.flaticon.com/512/3204/3204093.png"
    )

    st.markdown(
        f"""
    <div class="app-header-wrapper">
        <div class="app-header">
            <div class="header-content-container">
                <img src="{img_src}" class="app-logo">
                <div class="header-text-group">
                    <div class="header-top-row">
                        <div class="app-name">DentalSim</div>
                        <div class="header-divider"></div>
                        <div class="app-badge">AI Patient Simulation</div>
                    </div>
                    <div class="app-subtitle">Nền tảng mô phỏng lâm sàng nha khoa</div>
                    <div class="app-desc">Ứng dụng trí tuệ nhân tạo trong đào tạo và đánh giá kỹ năng</div>
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# --- 5. LOGIC CHÍNH ---

# === TRANG CHỦ (HOME PAGE) ===
if not st.session_state.case:
    render_header()

    st.write("")

    col_left, col_right = st.columns([1, 3], gap="large")

    with col_left:
        with st.container(border=True):
            st.markdown("### 🎯 Chọn Ca Bệnh")
            st.markdown("Lựa chọn chuyên khoa để bắt đầu:")

            categories = sorted(list(set([d["category"] for d in diseases])))
            cat_filter = st.selectbox("Chuyên khoa:", ["Tất cả"] + categories)

            candidates = (
                diseases
                if cat_filter == "Tất cả"
                else [d for d in diseases if d["category"] == cat_filter]
            )

            st.write("")

            if st.button(" BẮT ĐẦU CA MỚI", type="primary"):
                # ==========================================
                # SET ƯU TIÊN KỊCH BẢN DEMO (HARDCODE LOGIC)
                # ==========================================
                target_case = None

                if cat_filter == "Nội Nha":
                    # Ưu tiên lấy ca Nguyễn Văn Nam (ENDO_01)
                    target_case = next(
                        (
                            c
                            for c in candidates
                            if "Nguyễn Văn Nam" in c["patient"]["name"]
                        ),
                        None,
                    )
                elif cat_filter == "Chấn Thương":
                    # Ưu tiên lấy ca Phạm Văn Tài (TRAUMA_02)
                    target_case = next(
                        (
                            c
                            for c in candidates
                            if "Phạm Văn Tài" in c["patient"]["name"]
                        ),
                        None,
                    )

                if target_case:
                    selected_case = target_case
                else:
                    selected_case = random.choice(candidates)
                # ==========================================

                st.session_state.case = selected_case
                st.session_state.history = []
                st.session_state.is_generating = False

                hello = f"Chào bác sĩ... Tôi tên là {selected_case['patient']['name']}. Đợt này tôi bị {selected_case['patient']['complaint'].lower()} khó chịu quá."
                st.session_state.history.append({"role": "assistant", "content": hello})
                st.rerun()

            st.markdown("---")
            st.info(f"⚡ Đang có sẵn **{len(candidates)}** ca lâm sàng.")

    with col_right:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """<div class="feature-card"><span class="card-icon">🤖</span><div class="card-title">Bệnh nhân AI Tự nhiên</div><div class="card-desc">Mô phỏng chân thực cảm xúc, ngôn ngữ và triệu chứng của bệnh nhân theo y văn chuẩn.</div></div>""",
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                """<div class="feature-card"><span class="card-icon">📊</span><div class="card-title">Phản hồi Tức thì</div><div class="card-desc">Hệ thống tự động đánh giá chẩn đoán và cung cấp giải thích chi tiết đúng/sai ngay lập tức.</div></div>""",
                unsafe_allow_html=True,
            )

        st.write("")
        c3, c4 = st.columns(2)
        with c3:
            st.markdown(
                """<div class="feature-card"><span class="card-icon">🖼️</span><div class="card-title">Dữ liệu Đa phương tiện</div><div class="card-desc">Tích hợp phim X-Quang Panorama và hình ảnh lâm sàng trực quan cho từng ca bệnh.</div></div>""",
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                """<div class="feature-card"><span class="card-icon">🛡️</span><div class="card-title">Môi trường An toàn</div><div class="card-desc">Rèn luyện kỹ năng ra quyết định lâm sàng mà không gây rủi ro cho bệnh nhân thật.</div></div>""",
                unsafe_allow_html=True,
            )

# === TRANG THỰC HÀNH (CHAT PAGE) ===
else:
    render_header()
    case = st.session_state.case

    if st.button("⬅️ Trở về Trang Chủ", type="secondary"):
        st.session_state.case = None
        st.session_state.is_generating = False
        st.rerun()

    st.write("")

    col_info, col_chat = st.columns([3, 7], gap="large")

    with col_info:
        st.markdown(
            f"""
        <div class="profile-header-bg">
            <div style="font-size:22px; font-weight:700;">{case['patient']['name']}</div>
            <div style="font-size:16px; opacity:0.9; margin-top:5px;">{case['patient']['age']} Tuổi • {case['patient']['gender']}</div>
        </div>
        <div class="profile-body">
            <div style="font-size:14px; color:#64748b; font-weight:700; text-transform:uppercase;">Lý do khám chính</div>
            <div style="font-size:18px; font-weight:700; color:#dc2626; margin-top:5px;">{case['patient']['complaint']}</div>
            <hr style="border-top:1px solid #e2e8f0; margin:15px 0;">
            <div style="font-size:14px; color:#64748b;">Mã hồ sơ: <strong>{case['id']}</strong></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.write("")

        # HÌNH ẢNH CẬN LÂM SÀNG
        with st.container(border=True):
            st.markdown("### 📷 Hình ảnh Cận lâm sàng")

            fallback_web_img = "https://media.istockphoto.com/id/1145009653/photo/panoramic-dental-x-ray.jpg?s=612x612&w=0&k=20&c=6c6FzCjPzFw_k4kFzE5hTz7yQy6g_9oK1mF_5_j1jQ="
            fallback_local_img = "assets/images/default.png"

            img_path = case.get("image_url", fallback_web_img)

            if img_path and not str(img_path).startswith("http"):
                if not os.path.exists(img_path):
                    if os.path.exists(fallback_local_img):
                        img_path = fallback_local_img
                    else:
                        img_path = fallback_web_img

            st.image(img_path, use_container_width=True)

        st.write("")

        with st.container(border=True):
            st.markdown("### 🩺 Kết luận")
            all_diags = sorted(list(set([d["diagnosis"] for d in diseases])))
            user_choice = st.selectbox(
                "Chọn chẩn đoán xác định:", ["-- Vui lòng chọn --"] + all_diags
            )

            st.write("")
            if st.button("✅ Xác nhận Kết quả", type="primary"):
                if user_choice == "-- Vui lòng chọn --":
                    st.warning("Vui lòng chọn một chẩn đoán trước khi xác nhận.")
                elif user_choice == case["diagnosis"]:
                    st.success("🎉 CHÍNH XÁC!")
                    st.markdown(f"**Giải thích:** {case['explanation']}")
                    st.balloons()
                else:
                    st.error(f"❌ CHƯA CHÍNH XÁC")
                    st.markdown(f"Đáp án đúng là: **{case['diagnosis']}**")
                    with st.expander("Xem giải thích chi tiết"):
                        st.write(case["explanation"])

    # --- CỘT PHẢI: KHUNG CHAT HTML TÙY CHỈNH ---
    with col_chat:
        chat_container = st.container(height=750, border=True)

        with chat_container:
            chat_placeholder = st.empty()

            def render_chat(messages):
                html = '<div class="custom-chat-wrapper">'
                for m in messages:
                    text = str(m["content"]).replace("\n", "<br>")
                    if m["role"] == "user":
                        html += f"""
                        <div class="chat-row right">
                            <div class="chat-bubble user-bubble">{text}</div>
                            <div class="chat-avatar">👨‍⚕️</div>
                        </div>"""
                    else:
                        html += f"""
                        <div class="chat-row left">
                            <div class="chat-avatar">👤</div>
                            <div class="chat-bubble bot-bubble">{text}</div>
                        </div>"""
                html += "</div>"
                return html

            chat_placeholder.markdown(
                render_chat(st.session_state.history), unsafe_allow_html=True
            )

            if st.session_state.is_generating:
                with st.spinner("Bệnh nhân đang suy nghĩ..."):
                    ai = DentalAI()
                    reply = ai.get_response(st.session_state.history, case)
                    time.sleep(0.5)

                    st.session_state.history.append(
                        {"role": "assistant", "content": reply}
                    )
                    st.session_state.is_generating = False
                    st.rerun()

        if prompt := st.chat_input("Nhập câu hỏi khai thác bệnh sử tại đây..."):
            st.session_state.history.append({"role": "user", "content": prompt})
            st.session_state.is_generating = True
            st.rerun()
