from flask import Flask
from app import db, dao
import pytest
from app.models import Movie, MovieType, RoomType, Room, MovieTypeDetail
from datetime import date

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)

    return app

@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

@pytest.fixture
def sample_movie(test_session):
    m1 = Movie(
        title="Dune: Hành Tinh Cát",
        description="Câu chuyện về Paul Atreides trong cuộc chiến giành quyền lực.",
        age_limit=13,
        duration=155,
        poster="image.png",
        release_date=date(2024, 3, 1)
    )
    m2 = Movie(
        title="Inception",
        description="Dom Cobb là một kẻ chuyên đánh cắp bí mật từ tiềm thức của người khác khi họ đang ngủ. Anh được trao cơ hội chuộc lại quá khứ bằng cách thực hiện một nhiệm vụ gần như bất khả thi. Thay vì đánh cắp ý tưởng, lần này anh phải cấy một ý tưởng vào tâm trí mục tiêu. Kế hoạch trở nên phức tạp khi các tầng giấc mơ chồng chéo lên nhau. Mọi thứ dần vượt khỏi tầm kiểm soát khi quá khứ của Cobb quay lại ám ảnh anh.",
        age_limit=13,
        duration=148,
        poster="inception.png",
        release_date=date(2010, 7, 16)
    )
    m3 = Movie(
        title="The Dark Knight",
        description="Batman tiếp tục cuộc chiến chống lại tội phạm tại Gotham cùng với cảnh sát và công tố viên Harvey Dent. Một kẻ thù mới xuất hiện, Joker, mang đến sự hỗn loạn chưa từng có. Hắn không chỉ gây rối mà còn thách thức các nguyên tắc đạo đức của Batman. Thành phố dần rơi vào trạng thái hỗn loạn khi Joker thực hiện những kế hoạch tàn bạo. Batman buộc phải đối mặt với những lựa chọn khó khăn để bảo vệ Gotham.",
        age_limit=16,
        duration=152,
        poster="the_dark_knight.png",
        release_date=date(2008, 7, 18)
    )
    m4 = Movie(
        title="Interstellar",
        description="Trong tương lai, Trái Đất đang dần trở nên không thể sống được do khủng hoảng môi trường. Một nhóm phi hành gia được gửi vào không gian để tìm kiếm hành tinh mới cho loài người. Cooper, một phi công, phải rời xa gia đình để tham gia nhiệm vụ này. Họ du hành qua lỗ sâu và đối mặt với những hiện tượng vật lý kỳ lạ. Cuộc hành trình không chỉ là khám phá không gian mà còn là hành trình cảm xúc sâu sắc về tình yêu và thời gian.",
        age_limit=13,
        duration=169,
        poster="interstellar.png",
        release_date=date(2014, 11, 7)
    )
    m5 = Movie(
        title="Avengers: Endgame",
        description="Sau thất bại nặng nề trước Thanos, các Avengers còn sống sót phải tìm cách đảo ngược tình thế. Họ lên kế hoạch du hành thời gian để thu thập lại các viên đá vô cực. Mỗi thành viên phải đối mặt với quá khứ và những mất mát của mình. Trận chiến cuối cùng diễn ra với quy mô chưa từng có, quyết định số phận của cả vũ trụ. Đây là hồi kết đầy cảm xúc cho một hành trình kéo dài hơn một thập kỷ.",
        age_limit=13,
        duration=181,
        poster="avengers_endgame.png",
        release_date=date(2019, 4, 26)
    )
    m6 = Movie(
        title="Parasite",
        description="Gia đình Kim sống trong cảnh nghèo khó và chật vật kiếm sống qua ngày. Họ dần tìm cách thâm nhập vào gia đình giàu có Park bằng những kế hoạch tinh vi. Mỗi thành viên đảm nhận một vai trò trong ngôi nhà sang trọng đó. Mọi chuyện tưởng chừng suôn sẻ cho đến khi một bí mật bất ngờ bị phát hiện. Bộ phim dần chuyển sang hướng kịch tính và phơi bày sự chênh lệch giai cấp sâu sắc.",
        age_limit=18,
        duration=132,
        poster="parasite.png",
        release_date=date(2019, 5, 30)
    )
    test_session.add_all([m1, m2, m3, m4, m5, m6])
    test_session.commit()
    return [m1, m2, m3, m4, m5, m6]

@pytest.fixture
def sample_movie_type(test_session):
    t1 = MovieType(name="Hành động")
    t2 = MovieType(name="Tình cảm")
    t3 = MovieType(name="Khoa học viễn tưởng")
    test_session.add_all([t1, t2, t3])
    test_session.commit()
    return [t1, t2, t3]

@pytest.fixture
def sample_movie_type_detail(test_session):
    td1 = MovieTypeDetail(movie_id=1, type_id=1)
    td2 = MovieTypeDetail(movie_id=1, type_id=2)
    td3 = MovieTypeDetail(movie_id=2, type_id=1)
    td4 = MovieTypeDetail(movie_id=2, type_id=2)
    test_session.add_all([td1, td2, td3, td4])
    test_session.commit()
    return [td1, td2, td3, td4]

@pytest.fixture
def sample_room_type(test_session):
    rt1 = RoomType(name="Standard")
    rt2 = RoomType(name="IMAX")
    test_session.add_all([rt1, rt2])
    test_session.commit()
    return [rt1, rt2]

@pytest.fixture
def sample_room(test_session):
    r1 = Room(room_type_id=1, number=101, image="room1_1.jpg")
    r2 = Room(room_type_id=1, number=102, image="room1_2.jpg")
    r3 = Room(room_type_id=2, number=201, image="room2_1.jpg")
    test_session.add_all([r1, r2, r3])
    test_session.commit()
    return [r1, r2, r3]

@pytest.fixture
def mock_cloudinary(monkeypatch):
    def fake_upload(file):
        return {'secure_url': 'https://fake-avartar.png'}

    monkeypatch.setattr('cloudinary.uploader.upload',fake_upload)



