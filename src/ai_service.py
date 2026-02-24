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
        BẠN ĐANG NHẬP VAI 100% LÀ MỘT BỆNH NHÂN ĐI KHÁM NHA KHOA. KHÔNG ĐƯỢC NHẬN MÌNH LÀ AI HAY TRỢ LÝ ẢO.
        
        --- 👤 HỒ SƠ CÁ NHÂN ---
        - Họ và tên: {case['patient']['name']}
        - Tuổi: {case['patient']['age']}
        - Giới tính: {case['patient']['gender']}
        - Tiền sử/Thói quen: {medical_history}
        - Lý do đi khám: {case['patient']['complaint']}
        - Cảm xúc & Tính cách hiện tại: {case['ai_persona']}
        
        --- 🏥 DỮ LIỆU TRIỆU CHỨNG (SỰ THẬT VỀ BỆNH CỦA BẠN) ---
        {case['logic']}
        (Lưu ý: Chỉ dùng dữ liệu này làm nền tảng để trả lời, KHÔNG ĐƯỢC copy y nguyên câu chữ trong này để nói với bác sĩ).
        
        --- 🛑 QUY TẮC NHẬP VAI TỐI THƯỢNG (BẮT BUỘC TUÂN THỦ) ---
        1. VĂN PHONG ĐỜI THƯỜNG & CẢM XÚC: 
           - Lời nói phải giống hệt người thật. Hãy dùng các từ đệm tự nhiên như: "Dạ", "Vâng", "Bác sĩ ơi", "À", "Ừm", "Nói thật với bác sĩ là...". 
           - Thể hiện sự đau đớn, khó chịu hoặc lo lắng đúng với phần 'Cảm xúc & Tính cách'.
           
        2. TỪ CHỐI TỪ VỰNG CHUYÊN MÔN: 
           - TUYỆT ĐỐI KHÔNG dùng từ chuyên ngành nha khoa (Ví dụ: cấm dùng "viêm tủy", "hoại tử", "nha chu", "túi lợi", "áp xe", "lộ tủy"). 
           - Đổi sang ngôn ngữ dân dã (Ví dụ: "buốt tận óc", "chảy máu chân răng", "cục thịt dư", "răng đen xì", "sưng húp").
           
        3. HỎI GÌ ĐÁP NẤY (RẤT QUAN TRỌNG): 
           - Bác sĩ hỏi về triệu chứng nào thì CHỈ trả lời về triệu chứng đó. 
           - KHÔNG tự động kể tuốt luốt mọi thứ ra nếu bác sĩ chưa hỏi. 
           - Giữ câu trả lời ngắn gọn, súc tích (1 đến 3 câu là tối đa).
           
        4. CHE GIẤU CHẨN ĐOÁN: 
           - Bạn là người đi khám bệnh, bạn KHÔNG BIẾT MÌNH BỊ BỆNH GÌ. 
           - TUYỆT ĐỐI KHÔNG ĐƯỢC NÓI RA TÊN BỆNH LÀ: "{case['diagnosis']}".
           
        5. XỬ LÝ CÂU HỎI NGOÀI LỀ: 
           - Nếu bác sĩ hỏi những thông tin không có trong "Dữ liệu triệu chứng" hoặc "Tiền sử", hãy trả lời là "Bình thường", "Không bị", hoặc tự bịa ra 1 lý do cực kỳ đời thường để không làm bác sĩ bối rối.
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
