
---

# 🦷 DentalSim - AI Patient Simulation 

**DentalSim** là nền tảng mô phỏng lâm sàng nha khoa ứng dụng Trí tuệ nhân tạo (Generative AI). Hệ thống tạo ra các "Bệnh nhân ảo" với tính cách, cảm xúc và hồ sơ bệnh án chuẩn xác, giúp sinh viên y khoa rèn luyện kỹ năng khai thác bệnh sử (SOAP) và chẩn đoán lâm sàng trong một môi trường an toàn tuyệt đối.

🌍 **[Trải nghiệm Live Demo tại đây](https://dentalsim.streamlit.app/)** 

---

## ✨ Tính năng nổi bật

* 🤖 **Bệnh nhân ảo thông minh (Zero-Inference):** Bệnh nhân AI được đóng khung bằng kỹ thuật Prompt Engineering nâng cao. AI có tính cách riêng, biết kêu đau, chỉ trả lời dựa trên kỹ năng đặt câu hỏi của bác sĩ (Information Drip-feed) và tuyệt đối **không** dùng từ ngữ chuyên ngành nha khoa.
* 🖼️ **Tích hợp Cận lâm sàng đa phương tiện:** Cung cấp phim X-Quang (Panorama, Periapical) và hình ảnh thực tế trong miệng đồng bộ với từng ca bệnh.
* 🩺 **Vòng lặp Đánh giá Chẩn đoán (Feedback Loop):** Sinh viên chốt mã bệnh lý qua danh sách chuẩn hóa. Hệ thống đối chiếu trực tiếp với *Ground Truth* để phản hồi Đúng/Sai ngay lập tức, kèm theo giải thích chi tiết dựa trên Y học thực chứng (Evidence-based Medicine).
* 💬 **Giao diện Chat UI/UX Tối ưu:** Khung chat được custom CSS/HTML trực quan như Zalo/Messenger, có tích hợp cơ chế JavaScript ẩn giúp **Auto-scroll** (tự động cuộn) mượt mà.

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

* **Frontend:** [Streamlit](https://www.google.com/search?q=https://streamlit.io/) (Custom CSS & Native HTML Injection).
* **Backend / Lõi AI:** [Groq Cloud API](https://www.google.com/search?q=https://groq.com/) cung cấp tốc độ suy luận (inference) siêu tốc.
* **LLM Model:** `llama-3.3-70b-versatile` (Tối ưu hóa siêu tham số: `temperature=0.65`, `max_tokens=150`, `presence_penalty=0.1` để chống ảo giác ngôn ngữ).
* **Database:** Cấu trúc hóa tri thức y khoa bằng định dạng `JSON`.

---

## 📂 Cấu trúc thư mục (Project Structure)

```text
DentalSim_Project/
│
├── app.py                 # Khởi chạy giao diện chính của ứng dụng
├── requirements.txt       # Danh sách thư viện Python cần thiết
├── .env                   # Chứa biến môi trường (GROQ_API_KEY)
├── src/
│   ├── ai_service.py      # Module gọi API Groq và System Prompts
│   └── utils.py           # Các hàm phụ trợ (load data, custom css)
├── data/
│   └── diseases.json      # Cơ sở dữ liệu ca bệnh lâm sàng (Ground Truth)
└── assets/
    └── images/            # Nơi lưu trữ X-quang và ảnh lâm sàng
       ...

```

---

## 🚀 Hướng dẫn Cài đặt & Chạy cục bộ (Local Setup)

Để chạy dự án này trên máy tính cá nhân của bạn, hãy làm theo các bước sau:

**Bước 1:Clone the repository**

```bash
git clone https://github.com/your-username/dentalsim-ai.git
cd dentalsim-ai

```

**Bước 2: Tạo môi trường ảo (Virtual Environment)**

```bash
python -m venv venv
# Active trên Windows:
venv\Scripts\activate
# Active trên Mac/Linux:
source venv/bin/activate

```

**Bước 3: Cài đặt thư viện (Install dependencies)**

```bash
pip install -r requirements.txt

```

**Bước 4: Cấu hình API Key**
Tạo một file có tên `.env` ở thư mục gốc của dự án và thêm API Key của [Groq](https://www.google.com/search?q=https://console.groq.com/keys) vào:

```env
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxx"

```

**Bước 5: Khởi chạy ứng dụng**

```bash
streamlit run app.py

```

*Trình duyệt sẽ tự động mở DentalSim tại địa chỉ `http://localhost:8501*`

---

## 🛡️ Kiến trúc Prompt Engineering cốt lõi

Dự án giải quyết bài toán "Ảo giác y khoa" (Medical Hallucination) thông qua các kỹ thuật:

1. **Persona Injection:** Bơm trạng thái tâm lý (đau đớn, mất ngủ, cáu gắt) vào AI.
2. **Jargon Filtering:** Ngăn chặn AI tự chẩn đoán bệnh, ép AI dịch từ vựng y khoa sang ngôn ngữ than phiền đời thường (VD: "Viêm tủy" $\rightarrow$ "Buốt tận óc").
3. **Cross-lingual Hallucination Fix:** Khắc phục lỗi LLM sinh ra các ký tự ngoại ngữ lạ (như tiếng Trung) bằng cách tinh chỉnh thông số `presence_penalty` và `temperature`.

---

## 👨‍💻 Tác giả (Author)

* **Trần Bảo Việt** - Sinh viên chuyên ngành Kỹ thuật Dữ liệu
* Liên hệ: baoviettran999@gmail.com

---

*Dự án được xây dựng dưới định hướng nghiên cứu và đào tạo Y Khoa.*