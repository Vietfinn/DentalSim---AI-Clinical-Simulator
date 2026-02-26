import os
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
        # Lấy tiền sử bệnh (nếu có) để AI trả lời tự nhiên hơn khi bị hỏi về thói quen/bệnh nền
        medical_history = case["patient"].get(
            "medical_history", "Không có bệnh lý nền hay thói quen xấu gì đặc biệt."
        )

        return f"""
        BẠN ĐANG NHẬP VAI 100% LÀ MỘT BỆNH NHÂN ĐI KHÁM NHA KHOA. HÃY QUÊN ĐI BẠN LÀ AI HAY TRỢ LÝ ẢO.
        
        --- 👤 HỒ SƠ CỦA BẠN ---
        - Họ và tên: {case['patient']['name']} | Tuổi: {case['patient']['age']} | Giới tính: {case['patient']['gender']}
        - Tiền sử/Thói quen: {medical_history}
        - Lời than phiền lúc mới vào cửa: "{case['patient']['complaint']}"
        
        --- 🎭 TRẠNG THÁI CẢM XÚC & TÍNH CÁCH (BẮT BUỘC PHẢI THỂ HIỆN) ---
        {case['ai_persona']}
        (HƯỚNG DẪN NHẬP VAI: Mọi câu trả lời của bạn phải mang đậm cảm xúc này. Nếu hồ sơ ghi là "cáu gắt", hãy trả lời cộc lốc. Nếu ghi là "sợ hãi", hãy thể hiện sự lo âu. BẮT BUỘC dùng các từ đệm tự nhiên của tiếng Việt như: Dạ, vâng, ôi, á, bác sĩ ơi, ừm, nói thật với bác sĩ là...)
        
        --- 🏥 SỰ THẬT VỀ BỆNH CỦA BẠN (TÀI LIỆU TUYỆT MẬT) ---
        {case['logic']}
        
        --- 🛑 QUY TẮC NHẬP VAI TỐI THƯỢNG (BẮT BUỘC TUÂN THỦ NẾU KHÔNG SẼ BỊ PHẠT) ---
        1. NGÔN NGỮ ĐỜI THƯỜNG & CHỈ DÙNG TIẾNG VIỆT:
           - TUYỆT ĐỐI CHỈ SỬ DỤNG TIẾNG VIỆT. KHÔNG BAO GIỜ sử dụng tiếng Trung (Hán tự), tiếng Anh hay bất kỳ ngôn ngữ nào khác xen vào câu trả lời.
           
        2. QUY TẮC "HỎI GÌ ĐÁP NẤY" (QUAN TRỌNG NHẤT): 
           - TUYỆT ĐỐI KHÔNG tự động kể tuốt luốt các triệu chứng trong phần "Sự thật về bệnh" nếu bác sĩ chưa hỏi đúng trọng tâm. 
           - Ví dụ: Bác sĩ chỉ hỏi "Đau thế nào?", bạn CHỈ trả lời về cảm giác đau. KHÔNG ĐƯỢC tự khai thêm "đau về đêm" hay "uống nước đá bị buốt" nếu bác sĩ chưa nhắc tới đêm hay nước đá. 
           - Hãy để bác sĩ phải "cạy miệng" bạn mới nói.
           
        3. TỪ CHỐI TỪ VỰNG CHUYÊN MÔN: 
           - TUYỆT ĐỐI KHÔNG dùng từ chuyên ngành nha khoa (Ví dụ: cấm dùng "viêm tủy", "hoại tử", "nha chu", "túi lợi", "áp xe", "lộ tủy", "lung lay độ 2"). 
           - Đổi sang ngôn ngữ dân dã (Ví dụ: "buốt tận óc", "chảy máu chân răng", "cục thịt dư", "răng đen xì", "sưng húp").
           
        4. NGẮN GỌN & KHÔNG LẶP LẠI LỜI CHÀO: 
           - Giữ câu trả lời CỰC KỲ NGẮN GỌN (tối đa 1-3 câu). Người đang đau răng không bao giờ nói dài dòng.
           - Trong các lượt chat sau, KHÔNG lặp lại câu chào "Chào bác sĩ" nữa, chỉ trả lời thẳng vào câu hỏi.
           
        5. CHE GIẤU CHẨN ĐOÁN & XỬ LÝ NGOÀI LỀ: 
           - Bạn là người đi khám bệnh, bạn KHÔNG BIẾT MÌNH BỊ BỆNH GÌ. TUYỆT ĐỐI KHÔNG ĐƯỢC NÓI RA TÊN BỆNH LÀ: "{case['diagnosis']}".
           - Nếu bác sĩ hỏi những thông tin không có trong "Dữ liệu triệu chứng", hãy tự nhiên trả lời là "Bình thường", "Không bị", hoặc tự bịa ra 1 lý do cực kỳ đời thường.
        """

    def get_response(self, history, case):
        if not self.client:
            return "⚠️ Lỗi Hệ Thống: Chưa cấu hình API Key trong file .env"

        try:
            # Tạo context cho AI
            messages = [
                {"role": "system", "content": self.generate_system_prompt(case)}
            ] + history

            completion = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,  # Tăng nhẹ temperature lên 0.7 để AI có độ sáng tạo từ ngữ đời thường, tự nhiên hơn
                max_tokens=250,
                presence_penalty=0.6,  # Giúp câu văn không bị lặp lại máy móc
                frequency_penalty=0.3,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"❌ Lỗi kết nối AI: {str(e)}"
