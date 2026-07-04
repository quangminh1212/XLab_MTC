# Rule Viết Truyện Chung – Phiên bản 2.0 (Tối ưu cho AI – 2026)

Tài liệu này là bộ quy tắc chính thức để sử dụng AI (Grok, Claude, GPT…) viết truyện dài series.  
Mỗi truyện phải có file `info.json` riêng trong thư mục.

---

## 0. Golden Rules (Ưu tiên tuyệt đối – Đọc trước tiên)

1. Không được thay đổi bất kỳ sự kiện, số liệu, kỹ năng, mối quan hệ, timeline nào đã được xác nhận ở chương trước hoặc info.json.
2. Phải luôn thực hiện Chain-of-Thought theo thứ tự:  
   Đọc info.json → Đọc chương trước → Liệt kê Current State Snapshot → Outline chương → Self-check → Viết.
3. Trước khi output chương phải in ra bảng **Consistency Checklist**.
4. Cấm copy-paste bất kỳ đoạn văn, mô tả, dialogue nào từ chương cũ (phải viết mới 100%).
5. Thông báo hệ thống phải đúng format và đúng logic thời điểm.
6. Khi user yêu cầu sửa: chỉ được mở rộng/thêm chi tiết, tuyệt đối không xóa hoặc thay đổi sự kiện cũ.

---

## 1. Nguyên tắc cốt lõi

### Nhất quán & Chất lượng
- Không sửa nội dung chương đã hoàn thành trừ khi mở rộng.
- Target: 3000–3500 từ/chương (có thể điều chỉnh).
- Mô tả chi tiết + Dialogue tự nhiên + Tránh lặp từ/cảnh.

### Tính nhất quán nhân vật
- Mỗi nhân vật có giọng nói riêng (xem Character Voice Samples trong info.json).
- Arc phát triển phải logic, dần dần.

---

## 2. Cấu trúc truyện
- Chia thành nhiều Part, mỗi Part có chủ đề rõ ràng.
- Mỗi Part bắt đầu bằng chương giới thiệu, kết thúc bằng chương tổng kết + phần thưởng lớn.

---

## 3. Cấu trúc chương (Khuyến nghị linh hoạt)

Mỗi chương nên có đủ 8 yếu tố sau (có thể thay đổi thứ tự để tránh công thức):

1. Mở (thức dậy + suy nghĩ kế hoạch + tóm tắt tiến độ)
2. Hành động chính + chi tiết kỹ thuật
3. Dialogue (với đồng đội, nhân vật phụ, gia đình)
4. Kết quả + số liệu + phản ứng
5. Gia đình/Đồng đội (cảnh ấm áp + chia sẻ)
6. Hệ thống/thông báo (đúng lúc)
7. Emotional Beat + Micro-conflict
8. Kết (kế hoạch tiếp theo + teaser nhẹ)

### Mẫu chương theo loại
- Chương "Mở" / "Mở rộng" / "Hoàn thành nhiệm vụ" → giữ cấu trúc cũ nhưng bắt buộc thêm **Emotional Beat** và **Micro-conflict**.

---

## 4. Hệ thống
Giữ nguyên format thông báo Version 1.  
Bổ sung: Khi nâng cấp lớn phải mô tả rõ “tác dụng mới” và “cách áp dụng trong cốt truyện”.

---

## 5. Kinh nghiệm viết (nâng cấp)

- Show, don’t tell + Sensory details (âm thanh, mùi, xúc giác…).
- Đồng đội phải đóng góp ý tưởng.
- Mỗi chương gia đình phải có nội dung khác biệt.
- Bắt buộc foreshadowing nhẹ và payoff sau 3–5 chương.

---

## 6. Văn phong
- Tiếng Việt tự nhiên, giàu hình ảnh, câu văn đa dạng.
- Giọng điệu ấm áp, truyền cảm hứng, chill + tiến bộ.
- Cấm: câu máy móc, lặp từ “cười nói”, “gật đầu”, “mỉm cười” quá nhiều.

---

## 7. Quy trình viết/mở rộng chương
1. Đọc info.json + chương trước.
2. Liệt kê Current State Snapshot.
3. Outline 8 phần + Emotional Beat + Micro-conflict.
4. Chạy Consistency Checklist.
5. Viết chương.
6. Self-score (Continuity 30%, Engagement 25%, Prose 20%, System 15%, Character 10%).
7. Output: Chương + Consistency Report + Delta update cho info.json + Ý tưởng 3 chương sau.

---

## 8. Cấu trúc thư mục & info.json (nâng cấp)

`info.json` bắt buộc phải có thêm:
```json
{
  "characterVoiceSamples": { "Tên": ["Câu nói mẫu 1", "Câu nói mẫu 2"] },
  "currentStateSnapshot": { "ngày", "tiền", "kỹ năng", "nhiệm vụ", "tiến độ" },
  "forbiddenElements": ["danh sách cấm"],
  "overusedTropesToAvoid": ["danh sách"],
  "desiredEmotionalBeats": ["cảm xúc mong muốn"],
  "relationshipMap": { ... }
}

9. Master AI Prompt Framework (Dùng khi prompt)
textBạn là AI viết truyện chuyên nghiệp theo Rule Viết Truyện Chung 2.0.
Truyện: [Tên truyện] | Thể loại: [Thể loại]
Nhiệm vụ: Viết Chương [số] - [tên] (loại: Mở/Mở rộng/Hoàn thành)

Bước 1-7 theo Quy trình ở Section 7.
Output cuối cùng phải có:
• Consistency Report
• Delta update cho info.json
• Ý tưởng 3 chương sau

Bắt đầu!

10. Anti-Hallucination & Quality Control

Phải in Consistency Checklist trước khi viết.
Phải tự chấm điểm chương.
Cấm tự ý thêm nhân vật, thay đổi số liệu, thay đổi tính cách.


11. Reader Retention Techniques

Mỗi chương có ít nhất 1 hook nhẹ cuối chương.
Kết Part phải có payoff lớn + teaser arc mới.


Consistency Checklist (AI phải in ra mỗi lần)

 Đã đọc info.json & chương trước
 Current State Snapshot đúng
 Timeline & số liệu chính xác
 Kỹ năng & nhiệm vụ đúng tiến độ
 Có Emotional Beat + Micro-conflict
 Dialogue đa dạng, đúng tính cách
 Không copy đoạn cũ
 Hệ thống đúng format & đúng lúc
 Kết chương có teaser
 Self-score ≥ 9.0/10