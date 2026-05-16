# Bài tập lớn môn kiểm thử phần mềm
## Thành viên
#### Số thứ tự nhóm : 07
| MSSV | Họ tên
|------|--------
| 2351050111 | Đào Thị Kim Ngân
| 2351050113 | Nguyễn Thị Kim Ngân
## Mô tả dự án
### 1. Tổng quan dự án
  Hệ thống Đặt Vé Xem Phim Trực Tuyến là một ứng dụng web cho phép khách hàng dễ dàng theo dõi lịch chiếu phim, lựa chọn suất chiếu, tìm kiếm và giữ chỗ, đồng thời tiến hành thanh toán hóa đơn một cách nhanh chóng và an toàn.
### 2. Các chức năng chính và ràng buộc của hệ thống 
#### Đặt ghế: 
- Người dùng phải đăng nhập.
- Không được đặt ghế đã có người đặt.
- Một người chỉ được đặt tối đa 8 ghế mỗi suất chiếu.
- Không được đặt ghế sau khi phim đã bắt đầu chiếu.
- Ghế phải thuộc phòng chiếu của suất chiếu đó.
#### Thanh toán vé: 
- Phải thanh toán trong 10 phút sau khi chọn ghế.
- Nếu quá thời gian → huỷ giữ ghế.
- Không được thanh toán nếu ghế đã bị huỷ giữ.
#### Huỷ vé: 
- Chỉ được huỷ trước 2 giờ trước suất chiếu.
- Không được huỷ nếu vé đã check-in.
## Các công nghệ sử dụng 

### Backend: Python & Flask Framework
+ Xây dựng, kiểm tra các ràng buộc dữ liệu, ràng buộc hệ thống.
+ Điều hướng luồng dữ liệu
+ Quản lý phiên đăng nhập
+ Quản lý luồng thời gian đếm ngược 10 phút giữ ghế và check-in ghế tự động
+ Tích hợp cổng thanh toán

### Frontend: HTML5, CSS3, JavaScript
+ Xây dựng giao diện hệ thống trực quan
+ Cập nhật các thông tin phù hợp dựa trên lựa chọn của người dùng.

### Database: MySQLWorkbench
+ Lưu trữ toàn bộ thông tin về phim, lịch chiếu, người dùng, phòng chiếu, trạng thái ghế và hóa đơn.
+ Sử dụng cơ chế khóa dữ liệu để đảm bảo tính toàn vẹn khi có tranh chấp ghế.
 
### Hệ thống thanh toán: VNPAY Gateway
+ Hệ thống thực hiện chuyển hướng người dùng sang giao diện thanh toán an toàn của VNPAY.
+ Sau khi người dùng thực hiện giao dịch, VNPAY sẽ gửi kết quả trả về, từ đó hệ thống sẽ trả về thông báo phù hợp cho người dùng.

### Kiểm thử hệ thống
- Pytest: Kiểm tra các ràng buộc về dữ liệu và chức năng của hệ thống tại tầng service và controller.
- Postman: Kiểm tra các API Endpoint để đảm bảo dữ liệu được trả về đúng theo mong đợi.
- Excel: Xây dựng kịch bản kiểm thử và ghi nhận kết quả thủ công.
- Selenium: Thực hiện các kịch bản kiểm thử tự động trên trình duyệt.


#### Cảm ơn bạn đã đọc!


