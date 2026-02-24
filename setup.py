import os
import json

# ==========================================
# CẤU HÌNH DỰ ÁN
# ==========================================
PROJECT_NAME = "DentalSim_Enterprise"

# ==========================================
# 1. DỮ LIỆU BỆNH ÁN (DATASET - 20 CA)
# ==========================================
DISEASES_DATA = [
    # --- NỘI NHA ---
    {
        "id": "ENDO_01",
        "category": "Nội Nha",
        "name": "Viêm tủy không hồi phục (Cấp)",
        "patient": {
            "name": "Nguyễn Văn Nam",
            "age": 34,
            "gender": "Nam",
            "complaint": "Đau buốt dữ dội răng hàm dưới phải",
        },
        "ai_persona": "Đang rất đau, tay ôm má, giọng nói cáu gắt. Khẳng định đau tự nhiên, đau về đêm không ngủ được.",
        "logic": "Đau tự phát, đau lan lên thái dương. Buốt > 30s với lạnh (Lingering pain). Gõ dọc đau nhẹ.",
        "diagnosis": "Viêm tủy không hồi phục",
        "explanation": "Đau tự phát + Lingering pain (lạnh) + Đau về đêm.",
    },
    {
        "id": "ENDO_02",
        "category": "Nội Nha",
        "name": "Viêm tủy có hồi phục",
        "patient": {
            "name": "Lê Thị Mai",
            "age": 22,
            "gender": "Nữ",
            "complaint": "Ê buốt khi uống nước đá",
        },
        "ai_persona": "Vui vẻ, chỉ nhăn mặt khi nhắc đến đồ lạnh. Sợ khoan răng.",
        "logic": "Chỉ đau khi kích thích (lạnh/ngọt). Hết đau ngay khi ngừng kích thích (Transient pain). Không đau về đêm.",
        "diagnosis": "Viêm tủy có hồi phục",
        "explanation": "Đau thoáng qua (Transient), không đau tự phát, tủy còn khả năng hồi phục.",
    },
    {
        "id": "ENDO_03",
        "category": "Nội Nha",
        "name": "Hoại tử tủy",
        "patient": {
            "name": "Trần Văn Bảy",
            "age": 45,
            "gender": "Nam",
            "complaint": "Răng đổi màu xám, không đau",
        },
        "ai_persona": "Bình thản. Lo lắng về thẩm mỹ. Kể lại hồi xưa có ngã xe đập miệng.",
        "logic": "Không đau nhức. Thử điện/nhiệt âm tính (không cảm giác). Răng đổi màu.",
        "diagnosis": "Hoại tử tủy",
        "explanation": "Tiền sử chấn thương + Răng đổi màu + Thử tủy âm tính.",
    },
    {
        "id": "ENDO_04",
        "category": "Nội Nha",
        "name": "Viêm quanh chóp cấp",
        "patient": {
            "name": "Hoàng Thị Lan",
            "age": 29,
            "gender": "Nữ",
            "complaint": "Đau khi cắn chạm, cảm giác răng trồi",
        },
        "ai_persona": "Chỉ tay chính xác vào răng đau. Không dám ăn nhai bên đó. Sợ hãi.",
        "logic": "Đau dữ dội khi gõ dọc. Cảm giác răng dài ra. Chết tủy từ trước.",
        "diagnosis": "Viêm quanh chóp cấp",
        "explanation": "Phản ứng gõ dương tính mạnh + Cảm giác răng trồi cao.",
    },
    {
        "id": "ENDO_05",
        "category": "Nội Nha",
        "name": "Áp xe quanh chóp cấp",
        "patient": {
            "name": "Phạm Văn Kính",
            "age": 50,
            "gender": "Nam",
            "complaint": "Sưng mặt, đau nhức dữ dội, sốt",
        },
        "ai_persona": "Mệt mỏi, sốt, mặt sưng húp một bên. Đòi nhổ răng ngay lập tức.",
        "logic": "Sưng nóng đỏ đau vùng mặt. Có mủ. Răng lung lay. Sốt toàn thân.",
        "diagnosis": "Áp xe quanh chóp cấp",
        "explanation": "Sưng mặt + Tụ mủ + Triệu chứng toàn thân (Sốt).",
    },
    # --- NHA CHU ---
    {
        "id": "PERIO_01",
        "category": "Nha Chu",
        "name": "Viêm lợi (Gingivitis)",
        "patient": {
            "name": "Trương Tuấn Tú",
            "age": 19,
            "gender": "Nam",
            "complaint": "Chảy máu khi đánh răng",
        },
        "ai_persona": "Ngại ngùng vì hôi miệng. Không đau.",
        "logic": "Lợi sưng đỏ, dễ chảy máu. Không đau. Không có túi nha chu sâu.",
        "diagnosis": "Viêm lợi",
        "explanation": "Viêm khu trú mô mềm, chảy máu nhưng không mất bám dính.",
    },
    {
        "id": "PERIO_02",
        "category": "Nha Chu",
        "name": "Viêm nha chu mạn",
        "patient": {
            "name": "Ngô Thị Bích",
            "age": 55,
            "gender": "Nữ",
            "complaint": "Răng lung lay, tụt lợi, ăn nhai yếu",
        },
        "ai_persona": "Buồn phiền vì răng thưa, dài ra. Sợ rụng răng giả.",
        "logic": "Có túi nha chu sâu (5-6mm). Tiêu xương trên X-quang. Răng lung lay.",
        "diagnosis": "Viêm nha chu mạn",
        "explanation": "Mất bám dính + Tiêu xương ổ răng + Lung lay.",
    },
    {
        "id": "PERIO_03",
        "category": "Nha Chu",
        "name": "Áp xe nha chu",
        "patient": {
            "name": "Đỗ Văn Minh",
            "age": 42,
            "gender": "Nam",
            "complaint": "Sưng cục ở lợi, ấn ra mủ",
        },
        "ai_persona": "Khó chịu vì cục sưng cấn. Răng vẫn còn cảm giác nóng lạnh.",
        "logic": "Sưng khu trú bên hông răng. Tủy vẫn sống (+). Ấn có mủ trào ra từ túi lợi.",
        "diagnosis": "Áp xe nha chu",
        "explanation": "Sưng khu trú + Tủy sống + Có túi nha chu sâu (khác với áp xe quanh chóp là tủy chết).",
    },
    # --- PHẪU THUẬT ---
    {
        "id": "SURG_01",
        "category": "Phẫu Thuật",
        "name": "Viêm lợi trùm răng khôn",
        "patient": {
            "name": "Trần Thu Hà",
            "age": 21,
            "gender": "Nữ",
            "complaint": "Đau góc hàm, khó há miệng",
        },
        "ai_persona": "Đau nhăn nhó, nói khó nghe (khít hàm). Sốt nhẹ.",
        "logic": "Đau vùng góc hàm răng 8. Há miệng hạn chế (Khít hàm). Lợi trùm sưng đỏ.",
        "diagnosis": "Viêm lợi trùm răng khôn",
        "explanation": "Tam chứng: Khít hàm + Viêm quanh răng 8 + Tuổi mọc răng khôn.",
    },
    {
        "id": "SURG_02",
        "category": "Phẫu Thuật",
        "name": "Viêm huyệt ổ răng khô (Dry Socket)",
        "patient": {
            "name": "Nguyễn Văn Đức",
            "age": 30,
            "gender": "Nam",
            "complaint": "Đau dữ dội sau nhổ răng 3 ngày",
        },
        "ai_persona": "Bức xúc, đau kịch phát lan lên tai. Hôi miệng nồng nặc.",
        "logic": "Đau tăng lên vào ngày thứ 3 sau nhổ. Huyệt ổ răng rỗng, lộ xương, không có cục máu đông.",
        "diagnosis": "Viêm huyệt ổ răng khô",
        "explanation": "Đau tăng ngày thứ 3 + Mất cục máu đông + Lộ xương.",
    },
    {
        "id": "SURG_03",
        "category": "Phẫu Thuật",
        "name": "Sót chân răng",
        "patient": {
            "name": "Lê Văn Tám",
            "age": 40,
            "gender": "Nam",
            "complaint": "Cấn đau chỗ nhổ răng cũ",
        },
        "ai_persona": "Khó chịu khi ăn nhai. Sờ thấy vật nhọn.",
        "logic": "Vết nhổ chưa lành hẳn. X-quang thấy hình ảnh cản quang dạng chân răng.",
        "diagnosis": "Sót chân răng",
        "explanation": "Hình ảnh X-quang xác nhận chân răng còn sót lại.",
    },
    # --- BỆNH LÝ MIỆNG ---
    {
        "id": "PATH_01",
        "category": "Bệnh Lý Miệng",
        "name": "Nhiệt miệng (Aphthous)",
        "patient": {
            "name": "Nguyễn Thị Mơ",
            "age": 25,
            "gender": "Nữ",
            "complaint": "Đau rát trong miệng, không ăn mặn được",
        },
        "ai_persona": "Nhăn nhó khi nói. Sợ bị ung thư miệng.",
        "logic": "Vết loét hình tròn, đáy vàng, viền đỏ rực. Đau rát nhiều. Sờ mềm.",
        "diagnosis": "Viêm loét Aphthous",
        "explanation": "Loét niêm mạc di động + Đau rát + Đáy sạch, viền đỏ.",
    },
    {
        "id": "PATH_02",
        "category": "Bệnh Lý Miệng",
        "name": "Nấm miệng (Candida)",
        "patient": {
            "name": "Trần Văn Ơn",
            "age": 65,
            "gender": "Nam",
            "complaint": "Rát lưỡi, miệng có mảng trắng",
        },
        "ai_persona": "Đau rát, miệng hôi. Đang dùng hàm giả tháo lắp.",
        "logic": "Mảng trắng như váng sữa, cạo được, để lại nền đỏ rớm máu.",
        "diagnosis": "Nấm miệng Candida",
        "explanation": "Giả mạc trắng cạo được + Nền viêm đỏ + Cơ địa người già/đeo hàm giả.",
    },
    # --- CHẤN THƯƠNG ---
    {
        "id": "TRAUMA_01",
        "category": "Chấn Thương",
        "name": "Gãy thân răng lộ tủy",
        "patient": {
            "name": "Bé Lê Hùng",
            "age": 9,
            "gender": "Nam",
            "complaint": "Gãy răng cửa do ngã xe",
        },
        "ai_persona": "Khóc lóc, sợ hãi. Đau buốt khi gió lùa vào.",
        "logic": "Gãy 1/3 thân răng. Nhìn thấy điểm tủy đỏ tươi chảy máu.",
        "diagnosis": "Gãy thân răng lộ tủy",
        "explanation": "Tổn thương mất mô cứng + Lộ buồng tủy ra môi trường miệng.",
    },
    {
        "id": "TRAUMA_02",
        "category": "Chấn Thương",
        "name": "Hội chứng nứt răng",
        "patient": {
            "name": "Phạm Văn Tài",
            "age": 40,
            "gender": "Nam",
            "complaint": "Nhói buốt khi cắn vào điểm nhất định",
        },
        "ai_persona": "Đau chói bất ngờ (Rebound pain). Hay ăn đồ cứng.",
        "logic": "Đau nhói khi nhả khớp cắn. Không thấy lỗ sâu rõ ràng.",
        "diagnosis": "Hội chứng nứt răng",
        "explanation": "Đau kiểu Rebound pain (đau khi nhả khớp) + Tiền sử ăn nhai đồ cứng.",
    },
    # --- PHỤC HỒI ---
    {
        "id": "REST_01",
        "category": "Phục Hồi",
        "name": "Sâu ngà sâu",
        "patient": {
            "name": "Hoàng Anh Tú",
            "age": 16,
            "gender": "Nam",
            "complaint": "Dắt thức ăn, ê khi ăn ngọt",
        },
        "ai_persona": "Hồn nhiên. Chỉ khó chịu vì dắt răng. Hết đau ngay khi súc miệng.",
        "logic": "Lỗ sâu lớn đáy mềm. Ê buốt khi kích thích nhưng hết ngay. Tủy sống.",
        "diagnosis": "Sâu ngà sâu",
        "explanation": "Lỗ sâu to + Tủy sống bình thường + Không đau tự phát.",
    },
    {
        "id": "REST_02",
        "category": "Phục Hồi",
        "name": "Mòn cổ răng",
        "patient": {
            "name": "Nguyễn Thị Yến",
            "age": 48,
            "gender": "Nữ",
            "complaint": "Ê buốt cổ răng khi chải răng",
        },
        "ai_persona": "Kỹ tính, chải răng ngang rất mạnh. Sợ nước lạnh.",
        "logic": "Khuyết hình chêm (V-shape) ở cổ răng. Bề mặt cứng láng bóng. Ê buốt.",
        "diagnosis": "Mòn cổ răng",
        "explanation": "Tổn thương hình chêm điển hình + Thói quen chải răng sai cách.",
    },
    # --- CHỈNH NHA ---
    {
        "id": "ORTHO_01",
        "category": "Chỉnh Nha",
        "name": "Chen chúc răng",
        "patient": {
            "name": "Phạm Thị Thảo",
            "age": 15,
            "gender": "Nữ",
            "complaint": "Răng khấp khểnh, ngại cười",
        },
        "ai_persona": "Tự ti, che miệng khi cười. Không đau.",
        "logic": "Cung hàm hẹp, các răng chồng chéo lên nhau. Khớp cắn sai lệch.",
        "diagnosis": "Chen chúc răng",
        "explanation": "Bất hài hòa kích thước răng và kích thước cung hàm.",
    },
    # --- PHỤC HÌNH ---
    {
        "id": "PROS_01",
        "category": "Phục Hình",
        "name": "Mất răng (Kennedy Class III)",
        "patient": {
            "name": "Lê Văn Cẩn",
            "age": 50,
            "gender": "Nam",
            "complaint": "Mất răng hàm dưới, ăn nhai khó",
        },
        "ai_persona": "Muốn trồng răng giả để ăn ngon hơn. Răng bên cạnh hơi xô lệch.",
        "logic": "Khoảng mất răng đã lành thương xương. Răng đối diện trồi xuống.",
        "diagnosis": "Mất răng bán phần",
        "explanation": "Mất răng giới hạn 2 đầu (Class III).",
    },
    {
        "id": "ENDO_06",
        "category": "Nội Nha",
        "name": "Polyp tủy",
        "patient": {
            "name": "Bé Nguyễn Văn Tí",
            "age": 10,
            "gender": "Nam",
            "complaint": "Cục thịt dư trong răng",
        },
        "ai_persona": "Không đau, hay chảy máu khi nhai trúng.",
        "logic": "Khối mô đỏ lấp đầy lỗ sâu. Xuất phát từ buồng tủy. Không đau.",
        "diagnosis": "Polyp tủy",
        "explanation": "Viêm tủy mạn tăng sinh (Polyp) thường gặp ở răng trẻ.",
    },
]

# ==========================================
# 2. NỘI DUNG CÁC FILE CODE (SOURCE CODE)
# ==========================================

# --- requirements.txt ---
REQUIREMENTS_CONTENT = """streamlit
groq
python-dotenv
pillow
"""

# --- .env.example ---
ENV_EXAMPLE_CONTENT = """# Đây là file cấu hình bảo mật.
# Hãy đổi tên file này thành ".env" và điền API Key của bạn vào.
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

# --- src/utils.py ---
UTILS_CONTENT = """import json
import streamlit as st

@st.cache_data
def load_data(filepath='data/diseases.json'):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ Lỗi: Không tìm thấy file dữ liệu tại {filepath}")
        return []

def load_css():
    st.markdown(\"\"\"
    <style>
        /* Modern Clean UI */
        .stApp { background-color: #f8f9fa; }
        
        /* Header ẩn */
        header {visibility: hidden;}
        
        /* Card Style cho thông tin bệnh nhân */
        .patient-card {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid #007bff;
            margin-bottom: 20px;
        }
        
        /* Chat Message */
        .stChatMessage {
            border-radius: 15px;
            padding: 10px;
        }
        
        /* Buttons */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
        }
    </style>
    \"\"\", unsafe_allow_html=True)
"""

# --- src/ai_service.py ---
AI_SERVICE_CONTENT = """import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Tự động load biến môi trường từ file .env
load_dotenv()

class DentalAI:
    def __init__(self):
        # Ưu tiên lấy từ .env (Local), nếu không có thì lấy từ st.secrets (Cloud)
        self.api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
        
        if not self.api_key:
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)

    def generate_system_prompt(self, case):
        return f\"\"\"
        BẠN LÀ BỆNH NHÂN THỰC TẾ (SIMULATED PATIENT) TRONG BUỔI KHÁM NHA KHOA.
        
        --- HỒ SƠ NHÂN VẬT ---
        - Tên: {case['patient']['name']}
        - Tuổi: {case['patient']['age']}
        - Giới tính: {case['patient']['gender']}
        - Tính cách/Thái độ: {case['ai_persona']}
        
        --- DỮ LIỆU Y KHOA (TUYỆT ĐỐI BÍ MẬT - KHÔNG TIẾT LỘ TRỰC TIẾP) ---
        {case['logic']}
        
        --- QUY TẮC NHẬP VAI ---
        1. Ngôn ngữ: Tiếng Việt đời thường, dân dã (Ví dụ: Không nói "viêm tủy", hãy nói "buốt tận óc").
        2. Nếu bác sĩ hỏi đúng triệu chứng trong dữ liệu -> Trả lời thật chi tiết.
        3. Nếu bác sĩ hỏi triệu chứng KHÔNG có trong dữ liệu -> Trả lời "Không có", "Bình thường" hoặc bịa ra một cách logic.
        4. TUYỆT ĐỐI KHÔNG BAO GIỜ nói tên bệnh hoặc chẩn đoán ra.
        5. Giữ câu trả lời ngắn gọn (dưới 3 câu) để hội thoại tự nhiên.
        \"\"\"

    def get_response(self, history, case):
        if not self.client:
            return "⚠️ Lỗi Hệ Thống: Chưa cấu hình API Key trong file .env"
            
        try:
            # Tạo context cho AI
            messages = [{"role": "system", "content": self.generate_system_prompt(case)}] + history
            
            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile", # Model tốt nhất hiện nay trên Groq
                messages=messages,
                temperature=0.6,
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"❌ Lỗi kết nối AI: {str(e)}"
"""

# --- app.py ---
APP_CONTENT = """import streamlit as st
import random
import time
from src.utils import load_data, load_css
from src.ai_service import DentalAI

# --- CONFIG ---
st.set_page_config(
    page_title="DentalSim Enterprise",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load giao diện & Data
load_css()
diseases = load_data('data/diseases.json')

# --- SESSION STATE ---
if "case" not in st.session_state: st.session_state.case = None
if "history" not in st.session_state: st.session_state.history = []

# --- SIDEBAR (CONTROLS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=80)
    st.title("DentalSim Enterprise")
    st.caption("v3.0 | Professional Training Platform")
    
    st.markdown("---")
    
    # Kiểm tra trạng thái API
    ai_check = DentalAI()
    if ai_check.client:
        st.success("🟢 Hệ thống AI: Online")
    else:
        st.error("🔴 Hệ thống AI: Offline (Thiếu .env)")
    
    st.markdown("### 🗂️ Chọn Ca Lâm Sàng")
    categories = list(set([d['category'] for d in diseases]))
    cat_filter = st.selectbox("Chuyên khoa:", ["Tất cả"] + categories)
    
    candidates = diseases if cat_filter == "Tất cả" else [d for d in diseases if d['category'] == cat_filter]
    
    if st.button("🚀 BẮT ĐẦU CA MỚI", type="primary"):
        st.session_state.case = random.choice(candidates)
        st.session_state.history = []
        # Tin nhắn mở đầu
        hello_msg = f"Bác sĩ ơi... tôi là {st.session_state.case['patient']['name']}... đau quá..."
        st.session_state.history.append({"role": "assistant", "content": hello_msg})
        st.rerun()
        
    st.info(f"📊 Kho dữ liệu: {len(diseases)} bệnh án")

# --- MAIN INTERFACE ---
if st.session_state.case:
    case = st.session_state.case
    
    # --- PATIENT CARD (DASHBOARD) ---
    st.markdown(f\"\"\"
    <div class="patient-card">
        <h3 style="margin:0; color:#007bff">👤 Hồ Sơ Bệnh Nhân: {case['patient']['name']}</h3>
        <p><strong>Tuổi:</strong> {case['patient']['age']} | <strong>Giới tính:</strong> {case['patient']['gender']}</p>
        <p style="color:#dc3545"><strong>Lý do đến khám:</strong> {case['patient']['complaint']}</p>
    </div>
    \"\"\", unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 4], gap="large")
    
    # --- LEFT COLUMN: CHAT ---
    with col1:
        st.subheader("💬 Hội Thoại Lâm Sàng")
        chat_container = st.container(height=500)
        
        for msg in st.session_state.history:
            avatar = "👨‍⚕️" if msg['role'] == "user" else "👤"
            chat_container.chat_message(msg['role'], avatar=avatar).write(msg['content'])
            
        if prompt := st.chat_input("Nhập câu hỏi bệnh sử..."):
            st.session_state.history.append({"role": "user", "content": prompt})
            chat_container.chat_message("user", avatar="👨‍⚕️").write(prompt)
            
            ai = DentalAI()
            with st.spinner("Bệnh nhân đang trả lời..."):
                response = ai.get_response(st.session_state.history, case)
                time.sleep(0.5) # Fake delay for realism
                
            st.session_state.history.append({"role": "assistant", "content": response})
            chat_container.chat_message("assistant", avatar="👤").write(response)
            st.rerun()

    # --- RIGHT COLUMN: EHR & DIAGNOSIS ---
    with col2:
        st.subheader("📋 Bảng Chẩn Đoán")
        
        with st.expander("Hình ảnh Cận Lâm Sàng (Giả lập)", expanded=True):
            st.image("https://media.istockphoto.com/id/1145009653/photo/panoramic-dental-x-ray.jpg?s=612x612&w=0&k=20&c=6c6FzCjPzFw_k4kFzE5hTz7yQy6g_9oK1mF_5_j1jQ=", 
                     caption="Phim X-Quang Panorama", use_column_width=True)
        
        st.markdown("---")
        st.write("### 🩺 Kết luận của Bác sĩ")
        
        all_diagnoses = sorted(list(set([d['diagnosis'] for d in diseases])))
        user_diagnosis = st.selectbox("Chọn chẩn đoán xác định:", ["-- Vui lòng chọn --"] + all_diagnoses)
        
        if st.button("✅ Xác Nhận Kết Quả", use_container_width=True):
            if user_diagnosis == "-- Vui lòng chọn --":
                st.warning("Vui lòng chọn một chẩn đoán!")
            elif user_diagnosis == case['diagnosis']:
                st.balloons()
                st.success(f"CHÍNH XÁC! Bệnh nhân bị: **{case['diagnosis']}**")
                st.markdown(f"**📝 Giải thích y khoa:** {case['explanation']}")
            else:
                st.error("CHƯA CHÍNH XÁC.")
                st.write(f"Đáp án đúng là: **{case['diagnosis']}**")

else:
    # --- WELCOME SCREEN ---
    st.markdown(\"\"\"
    <div style="text-align: center; padding-top: 50px;">
        <h1 style="color:#007bff; font-size: 3em;">DentalSim Enterprise</h1>
        <p style="font-size: 1.2em; color:#666;">Nền tảng đào tạo Nha khoa Lâm sàng Ảo hóa</p>
        <br>
        <p>👈 Vui lòng chọn Chuyên khoa bên trái để bắt đầu phiên làm việc.</p>
    </div>
    \"\"\", unsafe_allow_html=True)
"""


# ==========================================
# 3. HÀM KHỞI TẠO DỰ ÁN
# ==========================================
def create_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Đã tạo file: {path}")


def main():
    print(f"🚀 Đang khởi tạo dự án {PROJECT_NAME}...")

    # 1. Tạo thư mục
    base_dirs = ["data", "src", ".streamlit"]
    for d in base_dirs:
        os.makedirs(d, exist_ok=True)
        print(f"📂 Đã tạo thư mục: {d}")

    # 2. Tạo file Data
    with open("data/diseases.json", "w", encoding="utf-8") as f:
        json.dump(DISEASES_DATA, f, ensure_ascii=False, indent=2)
    print("✅ Đã tạo Database: data/diseases.json (20 bệnh)")

    # 3. Tạo các file Source Code
    create_file("requirements.txt", REQUIREMENTS_CONTENT)
    create_file(".env.example", ENV_EXAMPLE_CONTENT)
    create_file("src/__init__.py", "")
    create_file("src/utils.py", UTILS_CONTENT)
    create_file("src/ai_service.py", AI_SERVICE_CONTENT)
    create_file("app.py", APP_CONTENT)

    # 4. Hướng dẫn sử dụng
    print("\n" + "=" * 50)
    print("🎉 KHỞI TẠO HOÀN TẤT! HÃY LÀM THEO BƯỚC SAU:")
    print("=" * 50)
    print("1. Đổi tên file '.env.example' thành '.env'")
    print("2. Mở file '.env' và dán Groq API Key vào.")
    print("3. Cài đặt thư viện: pip install -r requirements.txt")
    print("4. Chạy ứng dụng:     streamlit run app.py")
    print("=" * 50)


if __name__ == "__main__":
    main()
