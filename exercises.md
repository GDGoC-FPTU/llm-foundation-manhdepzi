# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Câu trả lời của bạn*
Khi temperature thấp (0.0), câu trả lời ổn định, ngắn gọn và ít thay đổi giữa các lần gọi. Khi tăng temperature lên 0.5 và 1.0, phản hồi trở nên đa dạng và sáng tạo hơn. Ở mức 1.5, mô hình thường tạo ra câu trả lời rất ngẫu nhiên, đôi khi lan man hoặc kém chính xác hơn.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Câu trả lời của bạn*
Tôi sẽ chọn temperature khoảng 0.2–0.5 vì chatbot hỗ trợ khách hàng cần câu trả lời ổn định, chính xác và nhất quán. Temperature thấp giúp giảm khả năng trả lời sai hoặc quá sáng tạo không cần thiết.
---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> *Câu trả lời của bạn*
Với 10.000 người dùng/ngày × 3 request × 350 token ≈ 10,5 triệu token mỗi ngày. Dựa trên bảng giá API phổ biến, GPT-4o thường đắt hơn khoảng 5–10 lần so với GPT-4o-mini tùy input/output token.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> *Câu trả lời của bạn*
GPT-4o phù hợp cho các tác vụ cần chất lượng cao như trợ lý phân tích tài liệu, viết nội dung chuyên sâu hoặc xử lý logic phức tạp. GPT-4o-mini phù hợp cho chatbot FAQ, phân loại dữ liệu hoặc các tác vụ đơn giản cần tối ưu chi phí và tốc độ.
---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Câu trả lời của bạn*
Streaming quan trọng nhất trong các ứng dụng chat thời gian thực vì người dùng thấy phản hồi xuất hiện ngay lập tức, tạo cảm giác hệ thống nhanh và tự nhiên hơn, đặc biệt với câu trả lời dài. Nó cũng giúp giảm cảm giác chờ đợi và cải thiện trải nghiệm người dùng. Ngược lại, non-streaming phù hợp khi cần xử lý hoàn chỉnh trước khi hiển thị, ví dụ như tạo JSON, xuất báo cáo hoặc các tác vụ cần kết quả đầy đủ và chính xác trước khi trả về.

## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
