from app import db, app
from app.models import *
from datetime import datetime, timedelta
import hashlib

def seed_data():
    admin = Customer(
        full_name="Admin",
        username='admin',
        password=hashlib.md5("123".encode("utf-8")).hexdigest(),
        email='admin@gmail.com',
        phone_number='0357899304',
        role=UserRole.ADMIN
    )
    user = Customer(
        full_name="Kim Ngân",
        username='user123',
        password=hashlib.md5("Pass@123".encode("utf-8")).hexdigest(),
        email='user123@gmail.com',
        phone_number='0357899305',
        role=UserRole.CUSTOMER,
        birthday=datetime(2004, 1, 22).date()
    )
    db.session.add_all([admin, user])
    db.session.commit()

    movies = [
        Movie(id=1, title='PHÍ PHÔNG: QUỶ MÁU RỪNG THIÊNG',
              description='Phí Phông, loài quỷ khát máu trong truyền thuyết dân gian của đồng bào miền núi gây ám ảnh bao đời nay. Phim xoay quanh Còn (Kiều Minh Tuấn) và Dương (Minh Anh), hai pháp sư tập sự lên núi cứu người mẹ đang bị lời nguyền Phí Phông đánh gục. Cùng lúc đó, trong bản sâu cũng xảy ra nhiều cái chết ghê rợn. Mọi nghi ngờ đổ dồn về hai mẹ con Mon (Diệp Bảo Ngọc) và Lua (Nina Nutthacha), những người mang đặc tính y hệt Phí Phông. Thế nhưng, vẫn còn những bí mật động trời bị chôn vùi trong chốn rừng thiêng nước độc, cuốn hai anh em Còn và Dương vào cuộc truy lùng “Phí Phông” không hồi kết.',
              age_limit=16, duration=120, release_date=datetime(2026, 4, 24),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777039627/lws5grkuf0z5vgmh21cp.jpg',
              active=True),
        Movie(id=2, title='HẸN EM NGÀY NHẬT THỰC',
              description='Năm 1995, khi đang đứng trước một quyết định quan trọng của cuộc đời, Ân bất ngờ bị kéo trở lại quá khứ bởi những bức thư tình chưa từng trao tay. Hành trình tìm gặp Thiên - mối tình đầu từng khắc sâu trong tim - đưa cô về lại thôn xóm Trà Mây năm xưa, nơi những ký ức ngọt ngào xen lẫn tổn thương vẫn chưa hề nguôi ngoai. Trong khoảnh khắc định mệnh khi hai người bất ngờ chạm mặt, những bí mật bị che giấu suốt nhiều năm dần hé lộ, buộc Ân phải đối diện với sự thật và lựa chọn con đường cho riêng mình. “Hẹn Em Ngày Nhật Thực” là câu chuyện tình yêu đầy cảm xúc về những điều chưa nói, về tình yêu vĩnh cửu và câu hỏi day dứt: nếu còn cơ hội, ta có dám tin vào trái tim mình một lần nữa?',
              age_limit=16, duration=118, release_date=datetime(2026, 3, 30),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038566/pjmobd3it3dc3ued3ilh.jpg',
              active=True),
        Movie(id=3, title='DỊCH VỤ GIAO HÀNG CỦA PHÙ THỦY KIKI',
              description='Theo truyền thống, khi tròn 13 tuổi, con gái của các phù thủy phải rời xa quê hương để học cách tự lập . Kiki cũng thế, cô lên đường cùng chú mèo đen Jiji, bay đến thị trấn ven biển Koriko xa lạ. Tại đây, cô được một bà chủ tiệm bánh tốt bụng cưu mang và bắt đầu làm phụ tá cho bà, đồng thời cũng bắt đầu mở dịch vụ giao hàng mới bằng chổi bay. Cuộc sống mới mang đến cho Kiki những niềm vui, thất bại và thử thách đầu đời. Xen giữa hành trình ấy là tình bạn với Tombo - cậu bé có đam mê mãnh liệt với máy bay chạy bằng sức người. Tất cả đã giúp Kiki từng bước trưởng thành và hòa nhập với thị trấn biển đầy gió này.',
              age_limit=3, duration=103, release_date=datetime(2026, 4, 24),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038624/g74kqncjkadfdwhv5rem.jpg',
              active=True),
        Movie(id=4, title='DƯỚI BÓNG ĐIỆN HẠ',
              description='Lấy mốc năm 1457 dưới triều đại Joseon, Dưới Bóng Điện Hạ khắc họa số phận nghiệt ngã của vua Danjong - vị quân vương thứ sáu của triều đại (Park Ji-hoon thủ vai). Lên ngôi khi tuổi đời còn non trẻ, Danjong nhanh chóng trở thành quân cờ trong vòng xoáy quyền lực tàn khốc. Bị chính người chú lật đổ, phế truất và đày đến vùng Cheongnyeongpo heo hút, cuộc đời của vị vua trẻ rẽ sang một ngã rẽ đầy u uất. Tại chốn lưu đày, ông gặp trưởng làng Eom Heung Do (Yoo Hai-jin thủ vai) - người đã chủ động biến ngôi làng nghèo thành nơi giam giữ nhà vua, đổi lại hy vọng cứu vãn sinh kế cho dân làng. Từ hai thân phận tưởng chừng đối lập, một cựu đế vương và một thường dân, bộ phim dần hé mở mối liên kết lặng lẽ nhưng sâu sắc - nơi lòng trung thành, sự che chở âm thầm và những phận người nhỏ bé cùng trôi dạt giữa cơn sóng lớn của lịch sử.',
              age_limit=16, duration=115, release_date=datetime(2026, 4, 15),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038671/jsu7f3kdmffpood2vpe9.jpg',
              active=True),
        Movie(id=5, title='CÚ SỐC',
              description='Chuyện tình hoàn hảo của Emma (Zendaya) và Charlie (Robert Pattinson) bỗng vỡ vụn ngay trước thềm đám cưới. Một biến cố đen tối đột ngột ập đến bóc trần những dối trá kinh hoàng, đẩy cả hai vào mê cung của sự hoang mang và nghi kỵ. Khi sự thật được phơi bày, ranh giới giữa người "bạn đời" lý tưởng và một "kẻ xa lạ" đáng sợ trở nên mỏng manh hơn bao giờ hết.',
              age_limit=18, duration=105, release_date=datetime(2026, 4, 1),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038719/aoh4smbvyp6fm5snotvw.jpg',
              active=True),
        Movie(id=6, title='THOÁT KHỎI TẬN THẾ',
              description='Ryland Grace một giáo viên khoa học nhận ra anh chính là hy vọng cuối cùng của Trái Đất. Nhiệm vụ của anh: cứu lấy Mặt Trời khỏi một sinh thể bí ẩn đang hút cạn năng lượng ánh sáng, đẩy cả hệ Mặt Trời vào bóng tối vĩnh viễn. Nếu thất bại, sự sống trên Trái Đất sẽ lụi tàn theo ánh sáng cuối cùng của mặt trời. Giữa không gian vũ trụ cô độc và áp lực của thời gian đang cạn dần, mọi phép tính, mọi quyết định của anh đều gánh trên vai số phận của toàn nhân loại. Nhưng trong hành trình tưởng chừng chỉ có một mình giữa khoảng không vô tận ấy, một tình bạn bất ngờ với một sinh vật ngoài hành tinh đã xuất hiện. Và có lẽ, để cứu Trái Đất, anh sẽ không phải chiến đấu một mình.',
              age_limit=13, duration=155, release_date=datetime(2026, 4, 12),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038756/aodqkzxm0tharlx4y3cm.jpg',
              active=True),
        Movie(id=7, title='CÔ BÉ CORALINE',
              description='Khi gia đình chuyển đến một lâu đài cổ, Coraline vô tình mở ra cánh cửa dẫn tới một thế giới song song, nơi mọi thứ rực rỡ và hoàn hảo một cách đáng ngờ. Nhưng càng đắm mình trong sự “hoàn hảo” ấy, cô càng nhận ra phía sau lớp vỏ dịu dàng là một vực sâu nguy hiểm đang chực chờ nuốt chửng tất cả. Thế giới kia không phải phép màu, mà là chiếc bẫy được giăng bằng những bí mật đen tối. Để cứu gia đình và chính mình, Coraline buộc phải đối diện với thực thể tà ác đang ẩn sau vẻ ngoài rực rỡ và đôi mắt trống rỗng vô hồn.',
              age_limit=13, duration=99, release_date=datetime(2026, 4, 20),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038801/niaq7eyvvgwzupqwpkpt.jpg',
              active=True),
        Movie(id=8, title='CÚ NHẢY KỲ DIỆU',
              description='Hoppers xoay quanh Mabel, một cô gái yêu động vật, vô tình tiếp cận công nghệ cho phép chuyển ý thức con người vào cơ thể robot động vật. Nhờ đó, Mabel “nhảy” vào thế giới tự nhiên dưới hình dạng một con hải ly và có thể giao tiếp trực tiếp với các loài khác. Trong hành trình này, cô dần khám phá cách động vật nhìn nhận con người, đồng thời phát hiện những mối nguy đang đe dọa môi trường sống của chúng. Tận dụng công nghệ Nhảy, Mabel đã trở thành cầu nối, mang lại cuộc sống cân bằng cho cả con người và động vật.',
              age_limit=3, duration=105, release_date=datetime(2026, 5, 1),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777038878/d7zvwbsd9zylug68sdyq.jpg',
              active=True),
        Movie(id=9, title='TÀI',
              description='Tài bất ngờ rơi vào vòng xoáy nguy hiểm vì một khoản nợ tiền khổng lồ. Bị dồn vào đường cùng, Tài buộc phải dấn thân vào những lựa chọn sai lầm khiến gia đình trở thành mục tiêu bị đe dọa. Đằng sau những hành động liều lĩnh ấy là nỗi ám ảnh về người mẹ mà Tài luôn muốn bảo vệ và bù đắp bằng mọi giá. Khi ranh giới giữa đúng và sai ngày càng mong manh, Tài phải đối mặt với câu hỏi lớn nhất của đời mình: liệu lòng hiếu thảo có đủ để biện minh cho con đường anh đang đi.',
              age_limit=16,
              duration=101, release_date=datetime(2026, 4, 18),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777039001/dqxxfowt3ow2ib8aahzq.jpg',
              active=True),
        Movie(id=10, title='SHIN - CẬU BÉ BÚT CHÌ',
              description='Bộ phim xoay quanh một vương quốc lơ lửng mang tên Rakuga, tồn tại nhờ nguồn năng lượng đến từ những nét vẽ của con người. Nhưng khi thế giới loài người dần đánh mất sự sáng tạo, Rakuga đứng bên bờ sụp đổ. Giữa thời khắc hỗn loạn, Shin vô tình nắm giữ cây bút chì màu kỳ diệu – có thể biến mọi hình vẽ thành hiện thực. Từ những nét vẽ ngây ngô nhất, bốn “vị anh hùng bất ổn” ra đời, đồng hành cùng cậu trong chuyến phiêu lưu vừa hài hước vừa kịch tính. Khi ranh giới giữa tưởng tượng và thực tại bị xóa nhòa, Shin không chỉ chiến đấu để cứu một vương quốc, mà còn để bảo vệ điều quý giá nhất: khả năng mơ mộng và sáng tạo của trẻ em.',
              age_limit=3, duration=104, release_date=datetime(2026, 1, 5),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777039309/phakoqey0pwilxjehcgy.jpg',
              active=True),
        Movie(id=11, title='YÊU NỮ THÍCH HÀNG HIỆU 2',
              description='Hai mươi năm sau màn hóa thân kinh điển vào các vai diễn Miranda, Andy, Emily và Nigel — Meryl Streep, Anne Hathaway, Emily Blunt và Stanley Tucci sẽ chính thức trở lại với những con phố thời thượng của New York và văn phòng sang trọng của Tạp chí Runway trong "The Devil Wears Prada 2" (Yêu Nữ Thích Hàng Hiệu 2). Đây là phần phim tiếp theo cực kỳ được mong đợi từ 20th Century Studios, kế thừa sức hút từ hiện tượng điện ảnh năm 2006 từng định hình phong cách cho cả một thế hệ. Bộ phim được đạo diễn bởi David Frankel, kịch bản bởi Aline Brosh McKenna, sản xuất bởi Wendy Finerman, điều hành sản xuất bởi Michael Bederman, Karen Rosenfelt và Aline Brosh McKenna.',
              age_limit=13, duration=119, release_date=datetime(2026, 4, 24),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777039377/kjqzbg4ljhbgnd5clbqw.jpg',
              active=True),
        Movie(id=12, title='NOBITA VÀ LÂU ĐÀI DƯỚI ĐÁY BIỂN',
              description='Bước vào kì nghỉ hè, Nobita và các bạn tranh cãi chí chóe về địa điểm cắm trại. Theo đề xuất của Doraemon, cả nhóm quyết định cắm trại giữa lòng đại dương! Sử dụng bảo bối thần kì “xe Buggy chạy dưới nước” và “đèn pin thích nghi”, 5 bạn nhỏ tận hưởng chuyến cắm trại dưới đáy biển, gặp gỡ vô vàn sinh vật lí thú trên đường đi. Sau khi phát hiện một chiếc tàu đắm, nhóm bạn đã gặp chàng thanh niên bí ẩn El. Thật bất ngờ, anh ta lại là cư dân đáy biển, sống tại “liên bang Mu”, một vùng biển rộng lớn! Vốn căm ghét người mặt đất, cư dân đáy biển không thể nào tin tưởng Nobita và các bạn. Đúng lúc đó, lời thông báo “lâu đài quỷ... đã bắt đầu phục sinh!!” được truyền tới. “Lâu đài quỷ” khiến cư dân đáy biển khiếp sợ, rốt cuộc là gì? Đặt trọn niềm tin vào bè bạn trong lồng ngực, chuyến phiêu lưu vĩ đại quyết định số phận của trái đất, bắt đầu!',
              age_limit=3, duration=116, release_date=datetime(2026, 4, 24),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777039591/i1xfshdejmbpkjdymopb.jpg',
              active=True),
        Movie(id=13, title='MOANA',
              description='Nữ anh hùng biển cả quay trở lại. Moana từ Disney sẽ khơi dậy một làn sóng mới, để sự dũng cảm, lòng vị tha và âm nhạc hòa chung một nhịp chảy.',
              age_limit=12, duration=90, release_date=datetime(2026, 4, 30),
              poster='https://res.cloudinary.com/dimiharka/image/upload/v1777039512/ajupp8vku7tl0pib5xth.jpg',
              active=True)
    ]
    db.session.add_all(movies)
    db.session.commit()

    types = [
        MovieType(id=1, name='Kinh dị'),
        MovieType(id=2, name='Tâm lý'),
        MovieType(id=3, name='Tình cảm'),
        MovieType(id=4, name='Hoạt hình'),
        MovieType(id=5, name='Phiêu lưu'),
        MovieType(id=6, name='Gia đình'),
        MovieType(id=7, name='Hành động'),
        MovieType(id=8, name='Khoa học viễn tưởng'),
        MovieType(id=9, name='Hài hước'),
        MovieType(id=10, name='Chính kịch'),
        MovieType(id=11, name='Kỳ ảo'),
        MovieType(id=12, name='Siêu nhiên')
    ]
    db.session.add_all(types)
    db.session.commit()

    movie_details = [
        MovieTypeDetail(movie_id=1, type_id=1), MovieTypeDetail(movie_id=1, type_id=11),
        MovieTypeDetail(movie_id=2, type_id=3), MovieTypeDetail(movie_id=2, type_id=2),
        MovieTypeDetail(movie_id=3, type_id=4), MovieTypeDetail(movie_id=3, type_id=5),
        MovieTypeDetail(movie_id=4, type_id=10), MovieTypeDetail(movie_id=4, type_id=2),
        MovieTypeDetail(movie_id=5, type_id=2), MovieTypeDetail(movie_id=5, type_id=3),
        MovieTypeDetail(movie_id=6, type_id=8), MovieTypeDetail(movie_id=6, type_id=7),
        MovieTypeDetail(movie_id=7, type_id=4), MovieTypeDetail(movie_id=7, type_id=1),
        MovieTypeDetail(movie_id=7, type_id=11),
        MovieTypeDetail(movie_id=8, type_id=4), MovieTypeDetail(movie_id=8, type_id=5),
        MovieTypeDetail(movie_id=8, type_id=6),
        MovieTypeDetail(movie_id=9, type_id=7), MovieTypeDetail(movie_id=9, type_id=2),
        MovieTypeDetail(movie_id=9, type_id=6),
        MovieTypeDetail(movie_id=10, type_id=4), MovieTypeDetail(movie_id=10, type_id=9),
        MovieTypeDetail(movie_id=10, type_id=5),
        MovieTypeDetail(movie_id=11, type_id=9), MovieTypeDetail(movie_id=11, type_id=2),
        MovieTypeDetail(movie_id=12, type_id=4), MovieTypeDetail(movie_id=12, type_id=5),
        MovieTypeDetail(movie_id=12, type_id=8),
        MovieTypeDetail(movie_id=13, type_id=4), MovieTypeDetail(movie_id=13, type_id=5),
        MovieTypeDetail(movie_id=13, type_id=6)
    ]
    db.session.add_all(movie_details)
    db.session.commit()


    rt1 = RoomType(name='Phòng IMAX', active=True)
    rt2 = RoomType(name='Phòng 4DX', active=True)
    rt3 = RoomType(name='Phòng thường', active=True)
    rt4 = RoomType(name='Phòng VIP', active=True)
    db.session.add_all([rt1, rt2, rt3, rt4])
    db.session.commit()

    rooms = [
        Room(room_type_id=1, number=101, image='default.png'),
        Room(room_type_id=1, number=102, image='default.png'),
        Room(room_type_id=2, number=103, image='default.png'),
        Room(room_type_id=2, number=104, image='default.png'),
        Room(room_type_id=3, number=201, image='default.png'),
        Room(room_type_id=3, number=202, image='default.png'),
        Room(room_type_id=3, number=203, image='default.png'),
        Room(room_type_id=4, number=204, image='default.png'),
        Room(room_type_id=4, number=301, image='default.png'),
        Room(room_type_id=4, number=302, image='default.png'),
        Room(room_type_id=4, number=303, image='default.png')
    ]
    db.session.add_all(rooms)
    db.session.commit()

    for r in rooms:
        for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']:
            for number in range(1, 11):
                seat = Seat(row=row, number=number, room=r, active=True)
                db.session.add(seat)
    db.session.commit()

    now = datetime.now()
    print(now)
    movies_screening=[
        MovieScreening(start_time=now + timedelta(days=1),base_price=100000,room_id=1,movie_id=1),
        MovieScreening(start_time=now + timedelta(minutes=20), base_price=100000, room_id=2, movie_id=2),
        MovieScreening(start_time=now + timedelta(hours=2) + timedelta(seconds=30), base_price=100000, room_id=3, movie_id=3),
        MovieScreening(start_time=now + timedelta(hours=3), base_price=100000, room_id=4, movie_id=13),
        MovieScreening(start_time=now + timedelta(minutes=30), base_price=100000, room_id=4, movie_id=13),
        MovieScreening(start_time=now + timedelta(minutes=9), base_price=100000, room_id=5, movie_id=13),
        MovieScreening(start_time=now + timedelta(hours=3), base_price=100000, room_id=5, movie_id=12),
        MovieScreening(start_time=now + timedelta(minutes=1), base_price=100000, room_id=2, movie_id=13),
    ]
    db.session.add_all(movies_screening)
    db.session.commit()

    ss1=[]
    ss2=[]
    ss3=[]
    ss4=[]
    ss5=[]
    ss6=[]
    for i in range(1,91):
        s = ScreeningSeat(
            seat_id=i,
            screening_id=4,
            status=SeatStatus.AVAILABLE,
            holding_user_id= None
        )
        ss1.append(s)
    for i in range(1,91):
        s = ScreeningSeat(
            seat_id=i,
            screening_id=5,
            status=SeatStatus.AVAILABLE,
            holding_user_id= None
        )
        ss2.append(s)
    for i in range(1, 91):
        s = ScreeningSeat(
            seat_id=i,
            screening_id=6,
            status=SeatStatus.AVAILABLE,
            holding_user_id=None
        )
        ss3.append(s)
    for i in range(1, 91):
        s = ScreeningSeat(
            seat_id=i,
            screening_id=7,
            status=SeatStatus.AVAILABLE,
            holding_user_id=None
        )
        ss4.append(s)
    for i in range(1, 91):
        s = ScreeningSeat(
            seat_id=i,
            screening_id=3,
            status=SeatStatus.AVAILABLE,
            holding_user_id=None
        )
        ss5.append(s)
    for i in range(1, 91):
        s = ScreeningSeat(
            seat_id=i,
            screening_id=8,
            status=SeatStatus.AVAILABLE,
            holding_user_id=None
        )
        ss6.append(s)
    db.session.add_all(ss1)
    db.session.add_all(ss2)
    db.session.add_all(ss3)
    db.session.add_all(ss4)
    db.session.add_all(ss5)
    db.session.add_all(ss6)
    db.session.commit()

    # TẠO DỮ LIỆU ĐỂ TEST HỦY VÉ
    bill1 = Bill(total_amount=100000, status=PaymentStatus.SUCCESS, customer_id=2)
    bill2 = Bill(total_amount=100000, status=PaymentStatus.SUCCESS, customer_id=2)
    bill3 = Bill(total_amount=100000, status=PaymentStatus.SUCCESS, customer_id=2)
    bill4 = Bill(total_amount=100000, status=PaymentStatus.PENDING, customer_id=2)
    db.session.add_all([bill1, bill2, bill3, bill4])
    db.session.commit()

    s3 = ScreeningSeat.query.filter_by(screening_id=3).order_by(ScreeningSeat.id).all()
    s5 = ScreeningSeat.query.filter_by(screening_id=5).order_by(ScreeningSeat.id).all()
    s7 = ScreeningSeat.query.filter_by(screening_id=7).order_by(ScreeningSeat.id).all()

    ss_1 = s7[30]
    ss_2 = s3[30]
    ss_3 = s5[30]
    ss_4 = s7[31]
    ss_5 = s7[50]
    ss_5.status = SeatStatus.HOLDING
    ss_5.holding_user_id = 2
    ss_5.hold_expired_at = datetime.now() + timedelta(seconds=15)
    db.session.commit()
    for ss in [ss_1, ss_2, ss_3, ss_4]: ss.status = SeatStatus.BOOKED
    db.session.commit()

    ticket1 = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=ss_1.id,
        bill_id=bill1.id
    )
    ticket2 = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=ss_2.id,
        bill_id=bill2.id
    )
    ticket3 = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=ss_3.id,
        bill_id=bill3.id
    )
    ticket4 = Ticket(
        price=100000,
        status=TicketStatus.PAID,
        screening_seat_id=ss_4.id,
        bill_id=bill1.id
    )
    ticket5 = Ticket(
        price=100000,
        status=TicketStatus.HOLDING,
        screening_seat_id=ss_5.id,
        bill_id=bill4.id
    )
    db.session.add_all([ticket1, ticket2, ticket3, ticket4, ticket5])
    db.session.commit()

    payments = [
        Payment(
            bill_id=bill1.id,
            amount=200000,
            status=PaymentStatus.SUCCESS,
            txn_ref=f"TEST_{bill1.id}"
        ),
        Payment(
            bill_id=bill2.id,
            amount=100000,
            status=PaymentStatus.SUCCESS,
            txn_ref=f"TEST_{bill2.id}"
        ),
        Payment(
            bill_id=bill3.id,
            amount=100000,
            status=PaymentStatus.SUCCESS,
            txn_ref=f"TEST_{bill3.id}"
        )
    ]
    db.session.add_all(payments)
    db.session.commit()

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_data()
    print("Tạo dữ liệu thành công!")