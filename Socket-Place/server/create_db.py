import json

out_file = open('db.json', 'w')

places = []
# template: a = { 'id': '', 'name': '', 'coordinate': ( ), 'description': '', 'avatar': '', 'images': [] }
binh_duong = { 'id': 'BID', 'name': 'Bình Dương', 'coordinate': ( 10.9804, 106.6519), 'description': 'Bình Dương là một tỉnh thuộc vùng Đông Nam Bộ, Việt Nam. Tỉnh lỵ của Bình Dương là thành phố Thủ Dầu Một, cách trung tâm của Thành phố Hồ Chí Minh 30 km theo đường Quốc lộ 13. Đây là tỉnh có dân số đông thứ 6 trong tổng số 63 tỉnh thành và cũng là tỉnh có tỷ lệ gia tăng dân số cơ học rất cao do có nhiều người nhập cư, hơn 50% dân số của tỉnh Bình Dương là dân nhập cư.', 'avatar': '../images/BID/avt.jpg', 'images': ['../images/BID/img1.jpg', '../images/BID/img2.jpg', '../images/BID/img3.jpg', '../images/BID/img4.jpg', '../images/BID/img5.jpg', '../images/BID/img6.jpg', '../images/BID/img7.jpg', '../images/BID/img8.jpg', '../images/BID/img9.jpg'] }
places.append(binh_duong)

con_dao = { 'id': 'CDA', 'name': 'Côn Đảo', 'coordinate': (8.68916391, 106.6056642 ), 'description': 'Côn Đảo là một quần đảo ở ngoài khơi bờ biển Nam Bộ và cũng là đơn vị hành chính cấp huyện trực thuộc tỉnh Bà Rịa – Vũng Tàu. Quần đảo cách thành phố Vũng Tàu 97 hải lý theo đường biển. Nơi gần Côn Đảo nhất trên đất liền là xã Vĩnh Hải, Vĩnh Châu, Sóc Trăng, cách 40 hải lý. Côn Đảo từng được biết đến là nơi giam giữ và lưu đày tù nhân lớn nhất Đông Dương trước năm 1975. Ngày nay, Côn Đảo là điểm du lịch nghỉ dưỡng và tham quan với các bãi tắm và khu bảo tồn thiên nhiên Vườn quốc gia Côn Đảo.', 'avatar': '../images/CDA/avt.jpg', 'images': ['../images/CDA/img1.jpg', '../images/CDA/img2.jpg', '../images/CDA/img3.jpg', '../images/CDA/img4.jpg', '../images/CDA/img5.jpg', '../images/CDA/img6.jpg', '../images/CDA/img7.jpg', '../images/CDA/img8.jpg', '../images/CDA/img9.jpg'] }
places.append(con_dao)

da_nang = { 'id': 'DAN', 'name': 'Đà Nẵng', 'coordinate': ( 16.06778, 108.22083), 'description': 'Đà Nẵng là một thành phố trực thuộc trung ương, nằm trong vùng Duyên hải Nam Trung Bộ Việt Nam, là thành phố trung tâm và lớn nhất khu vực miền Trung - Tây Nguyên. ', 'avatar': '../images/DAN/avt.jpg', 'images': ['../images/DAN/img1.jpg', '../images/DAN/img2.jpg', '../images/DAN/img3.jpg', '../images/DAN/img4.jpg', '../images/DAN/img5.jpg', '../images/DAN/img6.jpg', '../images/DAN/img7.jpg', '../images/DAN/img8.jpg', '../images/DAN/img9.jpg'] }
places.append(da_nang)

ha_noi = { 'id': 'HAN', 'name': 'Hà Nội', 'coordinate': ( 21.0245, 105.84117), 'description': 'Hà Nội là thủ đô, thành phố trực thuộc trung ương và là một đô thị loại đặc biệt của Việt Nam. Hà Nội là thành phố trực thuộc trung ương có diện tích lớn nhất Việt Nam, đồng thời cũng là thành phố đông dân thứ hai và có mật độ dân số cao thứ hai trong 63 đơn vị hành chính cấp tỉnh của Việt Nam.', 'avatar': '../images/HAN/avt.jpg', 'images': ['../images/HAN/img1.jpg', '../images/HAN/img2.jpg', '../images/HAN/img3.jpg', '../images/HAN/img4.jpg', '../images/HAN/img5.jpg', '../images/HAN/img6.jpg', '../images/HAN/img7.jpg', '../images/HAN/img8.jpg', '../images/HAN/img9.jpg'] }
places.append(ha_noi)

nha_trang = { 'id': 'NHT', 'name': 'Nha Trang', 'coordinate': ( 12.24507, 109.19432 ), 'description': 'Nha Trang là một thành phố ven biển và là trung tâm chính trị, kinh tế, văn hóa, khoa học kỹ thuật và du lịch của tỉnh Khánh Hòa, Việt Nam. Nha Trang được mệnh danh là hòn ngọc của biển Đông, Viên ngọc xanh vì giá trị thiên nhiên, vẻ đẹp cũng như khí hậu của nó.', 'avatar': '../images/NHT/avt.jpg', 'images': ['../images/NHT/img1.jpg', '../images/NHT/img2.jpg', '../images/NHT/img3.jpg', '../images/NHT/img4.jpg', '../images/NHT/img5.jpg', '../images/NHT/img6.jpg', '../images/NHT/img7.jpg', '../images/NHT/img8.jpg', '../images/NHT/img9.jpg'] }
places.append(nha_trang)

tra_vinh = { 'id': 'TRV', 'name': 'Trà Vinh', 'coordinate': ( 9.94719, 106.34225), 'description': 'Trà Vinh là một tỉnh ven biển thuộc vùng Đồng bằng sông Cửu Long, Việt Nam. Trà Vinh cách Thành phố Hồ Chí Minh 200km đi bằng quốc lộ 53 qua tỉnh Vĩnh Long, khoảng cách rút ngắn thời gian chỉ còn 130km nếu đi bằng quốc lộ 60 qua tỉnh Bến Tre, cách thành phố Cần Thơ 50km. Được bao bọc bởi sông Tiền, sông Hậu với 02 cửa Cung Hầu và Định An nên giao thông đường thủy có điều kiện phát triển.', 'avatar': '../images/TRV/avt.jpg', 'images': ['../images/TRV/img1.jpg', '../images/TRV/img2.jpg', '../images/TRV/img3.jpg', '../images/TRV/img4.jpg', '../images/TRV/img5.jpg', '../images/TRV/img6.jpg', '../images/TRV/img7.jpg', '../images/TRV/img8.jpg', '../images/TRV/img9.jpg'] }
places.append(tra_vinh)

vung_tau = { 'id': 'VTA', 'name': 'Vũng Tàu', 'coordinate': (10.34599, 107.08426), 'description': 'Vũng Tàu là một thành phố thuộc tỉnh Bà Rịa – Vũng Tàu, vùng Đông Nam Bộ, Việt Nam. Sở hữu nhiều bãi biển đẹp và cơ sở hạ tầng được đầu tư hoàn chỉnh, Vũng Tàu là một địa điểm du lịch nổi tiếng tại miền Nam.', 'avatar': '../images/VTA/avt.jpg', 'images': ['../images/VTA/img1.jpg', '../images/VTA/img2.jpg', '../images/VTA/img3.jpg', '../images/VTA/img4.jpg', '../images/VTA/img5.jpg', '../images/VTA/img6.jpg', '../images/VTA/img7.jpg', '../images/VTA/img8.jpg', '../images/VTA/img9.jpg'] }
places.append(vung_tau)

json.dump(places, out_file, indent=4)

out_file.close()

in_file = open('db.json',)
data = json.load(in_file)
for i in data:
    print(i['name'])
in_file.close()
