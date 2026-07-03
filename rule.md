# Rule Viết Truyện Chung

Tài liệu này chứa quy tắc chung để viết và mở rộng nhiều loại truyện. Mỗi truyện cụ thể nên có thêm file `info.json` riêng trong thư mục truyện đó để lưu truyện liệu, nhân vật, cốt truyện, và timeline.

## 1. Nguyên tắc cốt lõi

### Nhất quán
- **Không thay đổi sự kiện đã viết:** Không sửa nội dung các chương đã hoàn thành trừ khi mở rộng.
- **Bảo toàn tính liên tục:** Nhân vật, số liệu, kỹ năng, điểm kinh nghiệm, timeline phải liên tục và không mâu thuẫn giữa các chương.
- **Không introduced mâu thuẫn:** Kiểm tra kỹ trước khi thêm chi tiết mới có xung đột với chương trước không.

### Chất lượng
- **Target word count:** ~3000 từ/chương (hoặc theo yêu cầu cụ thể của truyện).
- **Mô tả chi tiết:** Bối cảnh, cảm xúc, hành động, đối thoại.
- **Dialogue tự nhiên:** Phản ánh tính cách nhân vật, không máy móc.
- **Tránh lặp:** Không copy-paste các đoạn mẫu. Mỗi chương phải có chi tiết riêng.

### Tính nhất quán nhân vật
- Mỗi nhân vật có giọng nói, tính cách, và arc phát triển riêng.
- Nhân vật phát triển dần dần qua các chương, không đột ngột.
- Lưu lại tính cách và arc trong `info.json`.

## 2. Cấu trúc truyện

### Phân phần
- Mỗi truyện nên chia thành nhiều phần (Part), mỗi phần có chủ đề và mục tiêu riêng.
- Mỗi phần bắt đầu bằng chương giới thiệu, kết thúc bằng chương tổng kết.
- Cuối mỗi phần nên có phần thưởng/tổng kết để tạo cảm giác hoàn thành.

### Cấu trúc chương
Mỗi chương nên có:
1. **Mở:** Nhân vật chính thức dậy/bắt đầu ngày mới, suy nghĩ về kế hoạch.
2. **Hành động chính:** Hoạt động chính của chương (kinh doanh, chiến đấu, khám phá...).
3. **Dialogue:** Tương tác với nhân vật khác (nhân viên, đối tác, gia đình, bạn bè...).
4. **Kết quả:** Kết quả hành động, số liệu, phản ứng từ người khác.
5. **Gia đình/đồng đội:** Cảnh quay về nhà/nhóm, chia sẻ kết quả.
6. **Hệ thống/thông báo:** Nếu truyện có hệ thống, thông báo ở cuối hoặc giữa chương.
7. **Kết:** Nhân vật suy nghĩ về kế hoạch tiếp theo, câu kết tạo sự mong chờ.

### Mẫu chương theo loại

#### Chương "Mở" (bắt đầu lĩnh vực/arc mới)
1. Nhân vật chính thức dậy sớm.
2. Giới thiệu lĩnh vực/arc mới, bối cảnh lịch sử/thế giới.
3. Hành động: chuẩn bị, tuyển người, thiết kế quy trình.
4. Dialogue với nhân vật mới.
5. Kết quả ban đầu.
6. Về nhà/nhóm, chia sẻ, dialogue.
7. Hệ thống thông báo: phần thưởng + nhiệm vụ mới.
8. Kết chương.

#### Chương "Mở rộng"
1. Nhân vật chính thức dậy.
2. Tóm tắt tiến độ hiện tại, số lượng còn thiếu.
3. Mở rộng sang địa điểm/lĩnh vực mới.
4. Tuyển nhân viên/đồng đội mới, dialogue.
5. Kết quả, số lượng tăng lên.
6. Về nhà/nhóm, dialogue.
7. Hệ thống thông báo: tiến độ nhiệm vụ.
8. Kết chương.

#### Chương "Hoàn thành nhiệm vụ"
1. Nhân vật chính tập trung, tăng năng suất.
2. Mô tả quy trình tối ưu hóa, đồng đội đóng góp.
3. Đạt mục tiêu, tổng kết số lượng.
4. Cảm ơn/phản ứng từ người liên quan (dialogue).
5. Về nhà/nhóm, báo hoàn thành.
6. Hệ thống thông báo: hoàn thành + phần thưởng.
7. Giới thiệu arc/lĩnh vực tiếp theo.
8. Kết chương.

## 3. Hệ thống (System) - cho truyện có hệ thống

### Format thông báo
```
"Chủ nhân đã [hành động]. Nhận được [số] điểm kinh nghiệm."
"Điểm kinh nghiệm hiện tại: [số]."

"Nhiệm vụ mới: [tên nhiệm vụ] trong vòng [số] ngày"
- Mục tiêu: [mục tiêu]
- Phần thưởng: [phần thưởng]
- Thời gian: [số] ngày

"Chúc mừng chủ nhân đã hoàn thành nhiệm vụ!"
"Phần thưởng:"
- [số] điểm kinh nghiệm
- [tên kỹ năng] cấp [số]
"Điểm kinh nghiệm hiện tại: [số]."
```

### Quy tắc hệ thống
- Thông báo hệ thống phải nằm đúng chỗ (sau khi hoàn thành hành động), không gượng ép.
- Điểm kinh nghiệm phải tăng dần, không giảm (trừ khi có lý do plot).
- Kỹ năng nâng cấp theo cấp độ, mỗi cấp mạnh hơn cấp trước.
- Nhiệm vụ có mục tiêu rõ ràng, thời hạn, và phần thưởng.
- Tiến độ nhiệm vụ phải theo dõi chính xác (ví dụ: 7/10, 12/20).
- Khi hoàn thành phần, thêm phần thưởng lớn (điểm kinh nghiệm cao, mở rộng, kỹ năng đặc biệt).

### Bảng kỹ năng
Mỗi truyện nên có bảng kỹ năng trong `info.json`:
- Tên kỹ năng
- Cấp độ
- Nguồn (chương nhận)
- Mô tả tác dụng

## 4. Kinh nghiệm viết truyện

### Dialogue
1. **Đa dạng hóa:** Mỗi chương cần dialogue riêng, không lặp lại. Thay đổi nội dung, thêm chi tiết cụ thể.
2. **Nhân vật phụ:** Thêm dialogue từ người ngoài (khách hàng, dân làng, đối tác...) để thế giới sống động.
3. **Phản ánh tính cách:** Mỗi nhân vật nói khác nhau - người kiên định, người lo lắng, người hào hứng, người nghiêm nghị.

### Mô tả
4. **Chi tiết kỹ thuật:** Mô tả quy trình cụ thể (sản xuất, xây dựng, y tế...), không chung chung.
5. **Bối cảnh địa phương:** Mỗi địa điểm có đặc điểm riêng (khí hậu, văn hóa, kinh tế...).
6. **Cảm xúc:** Mô tả cảm xúc nhân vật qua hành động, ánh mắt, giọng nói - không chỉ kể.

### Phát triển nhân vật
7. **Arc rõ ràng:** Mỗi nhân vật có hướng phát triển (từ yếu → mạnh, từ nghèo → giàu, từ nhút nhát → tự tin).
8. **Cho đồng đội đóng góp ý tưởng:** Không chỉ nhân vật chính, đồng đội cũng đề xuất giải pháp, thể hiện sự trưởng thành.
9. **Quan hệ gia đình/nhóm:** Cảnh gia đình/nhóm mỗi chương nên có nội dung khác nhau, phát triển dần.

### Pacing
10. **Tiến độ rõ ràng:** Theo dõi số lượng chính xác để người đọc thấy tiến trình.
11. **Kỹ năng mới:** Mô tả tác dụng của kỹ năng/phần thưởng mới, giúp gì cho cốt truyện.
12. **Kết chương:** Câu kết tạo sự mong chờ chương tiếp (kế hoạch mới, thách thức mới).

### Số liệu
13. **Số tiền/giá cả:** Phải hợp lý với bối cảnh (thời đại, địa điểm).
14. **Phân chia lợi nhuận:** Nếu nhân vật chia lợi nhuận cho gia đình/nhóm, tỷ lệ nên nhất quán.
15. **Timeline:** Ngày/tháng/năm phải liên tục, không nhảy lùi trừ khi có lý do.

## 5. Văn phong

- **Ngôn ngữ:** Tiếng Việt (hoặc theo yêu cầu truyện).
- **Ngôi kể:** Ngôi thứ ba (hoặc ngôi thứ nhất tùy truyện).
- **Giọng điệu:** Kể chuyện, chi tiết, đối thoại tự nhiên.
- **Tránh:** Lặp từ, câu mẫu máy móc, mô tả chung chung.
- **Khuyến khích:** Hình ảnh so sánh, miêu tả cảm xúc qua hành động, dialogue ngắn gọn súc tích.

## 6. Quy trình mở rộng chương

1. **Đọc chương gốc** để hiểu nội dung, sự kiện, số liệu.
2. **Xóa file gốc** (nếu ghi đè).
3. **Viết phiên bản mở rộng** (~3000 từ hoặc theo yêu cầu) với:
   - Thêm chi tiết bối cảnh, đối thoại, mô tả.
   - Thêm dialogue từ nhân vật phụ.
   - Thêm chi tiết kỹ thuật/lĩnh vực.
   - Phát triển nhân vật (đồng đội, gia đình).
   - Giữ nguyên sự kiện, số liệu, kỹ năng, timeline.
4. **Lưu file mới.**
5. **Tiếp tục chương tiếp theo.**

## 7. Cấu trúc thư mục truyện

Mỗi truyện nên có:
```
[Tên truyện]/
├── info.json          # Truyện liệu: nhân vật, cốt truyện, timeline, kỹ năng
├── Chương 1 - ....txt
├── Chương 2 - ....txt
├── ...
└── Chương N - ....txt
```

### info.json nên chứa:
- **title, genre, setting:** Thông tin chung.
- **characters:** Nhân vật chính và phụ, tính cách, arc phát triển.
- **system:** Hệ thống (nếu có) - không gian, điểm kinh nghiệm, kỹ năng, format thông báo.
- **parts:** Cấu trúc phần, mỗi phần có chapters và plot chính.
- **timeline:** Lịch trình sự kiện theo chương.
- **recurringCharacters:** Nhân vật xuất hiện nhiều chương.
- **writingRules:** Quy tắc riêng của truyện (nếu có).

## 8. Checklist trước khi viết chương

- [ ] Đã đọc `info.json` để hiểu nhân vật, cốt truyện, số liệu hiện tại.
- [ ] Đã đọc chương trước để đảm bảo liên tục.
- [ ] Biết mục tiêu của chương này (mở/mở rộng/hoàn thành).
- [ ] Kiểm tra số liệu: điểm kinh nghiệm, tiến độ nhiệm vụ, kỹ năng.
- [ ] Kiểm tra timeline: chương này xảy ra khi nào, sau chương trước bao lâu.
- [ ] Chuẩn bị dialogue đa dạng, không lặp.
- [ ] Chuẩn bị chi tiết kỹ thuật/bối cảnh cụ thể.
