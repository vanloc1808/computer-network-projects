# Kịch bản giao tiếp của chương trình
## Giao thức trao đổi giữa client và server: UDP
## Cấu trúc của thông điệp (tổng cộng 1024 bytes cho 1 thông điệp):

### Đối với thông điệp từ server có 2 loại: 
- Thông điệp gửi số lượng thông điệp cần nhận cho data: | padding | len  |
    - len: kiểu `str`, thể hiện số lượng thông điệp (tối đa 3 bytes)
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte
- Thông điệp gửi từng phân data: |  ID  |   data   |  hash  |
    - ID: Kiểu `str` gồm 3 ký tự thể hiện số trong đoạn [000; 999] (3 bytes)
    - data: Kiểu `byte`, gồm 981 (1024 - 43) ký tự (981 bytes)
    - hash: Kiểu `str`, gồm 40 ký tự (40 bytes) được tạo khi hash `data` bằng thuật toán `SHA1` để kiểm lỗi

### Đối với thông điệp từ client có 6 loại:
- Thông điệp xác nhận số lượng: |  specifier  |  len  |  padding  |
    - specifier: kiểu `str`, là chuỗi ký tự "ACK_LEN_" (8 bytes)
    - len: kiểu `str`, là số lượng thông điệp đã nhận từ server, gồm 3 ký tự thể hiện số trong đoạn [000; 999] (3 bytes)
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte

- Thông điệp xác nhận phần data: |  specifier  |  id  |  padding  |
    - specifier: kiểu `str`, là chuỗi ký tự "ACK_" (4 bytes)
    - id: kiểu `str`, là thứ tự của thông điệp nhận từ server, gồm 3 ký tự thể hiện số trong đoạn [000; 999] (3 bytes)
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte

- Thông điệp yêu cầu thông tin toàn bộ địa điểm: |  command  |  padding  |
    - command: kiểu `str`, là chuỗi ký tự "GIV_ALL" (7 bytes)
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte

- Thông điệp yêu cầu thông tin chi tiết 1 địa điểm: |  command  |  id  |  padding  |
    - command: kiểu `str`, là chuỗi ký tự "GIV_DETAIL_" (11 bytes)
    - id: kiểu `str`, thể hiện id của địa điểm cần lấy
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte

- Thông điệp yêu cầu ảnh đại diện 1 địa điểm: |  command  |  id  |  padding  |
    - command: kiểu `str`, là chuỗi ký tự "GIV_AVT_" (8 bytes)
    - id: kiểu `str`, thể hiện id của địa điểm cần lấy
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte

- Thông điệp yêu cầu ảnh tại 1 địa điểm: |  command  |  position  |  separator  |  id  |  padding  |
    - command: kiểu `str`, là chuỗi ký tự "GIV_IMG_" (8 bytes)
    - id: kiểu `str`, thể hiện id của địa điểm cần lấy
    - separator: kiểu `char`, là ký tự '_'
    - position: kiểu `str`, là thứ tự trong danh sách ảnh cần lấy, gồm 3 ký tự thể hiện số trong đoạn [000; 999] (3 bytes)
    - padding: kiểu `byte`, gồm các null byte (`\x00`) sao cho toàn bộ thông điệp đủ  `1024` byte

## Cách tổ chức cơ sở dữ liệu
<L's part>

## Quá trình truyền từ server đến client
1. Đoạn dữ liệu ban đầu sẽ được xử lý thành danh sách các thông điệp kích thước 1024
2. Server gửi số lượng thông điệp cho client và chờ `ACK`
3. Sử dụng thuật toán `Sliding window` với kích thước 5 để truyền:

Phía server
```
tds = danh sách thông điệp cần truyền
l_tds = độ dài danh sách
size = kích thước cửa sổ = 5
i = 0
while i < l_tds:
    struyen = số lượng truyền = min(size, l_tds - i)
    kt = mảng đánh dấu kích thước struyen
    while kt chưa được đánh dấu hết:
        truyền lần lượt toàn bộ cửa sổ hiện tại (i -> i + struyen)
        thực hiện nhận ACK struyen lần, đánh dấu ID vào kt
        nếu quá giờ nhận ACK, coi như gói bị mất và truyền lại
    i = i + size (dịch tới cửa sổ tiếp theo)
```

Phía client:
```
l_tds = độ dài danh sách
size = kích thước cửa sổ = 5
i = 0
result = thông điệp được truyền
while i < l_tds:
    snhan = số lượng nhận = min(size, l_tds - i)
    buffer = bộ nhớ tạm để lưu cửa sổ với kích thước snhan
    while buffer chưa đầy hết:
        với mỗi phần tử, thực hiện nhận và kiểm lỗi, sau đó đưa vào buffer
    sắp xếp lại gói tin trong buffer, tách phần data và nối vào result
    i = i + size (dịch tới cửa sổ tiếp theo)
```
