import os
import platform
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pytest
from app import db
from app.schedule import start_scheduler as scheduler
from app.seed import seed_data
from app.test.base_test import create_app


@pytest.fixture(scope="session")
def sel_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, "selenium_test.db")

    app = create_app(db_uri="sqlite:///" + db_path)

    def run():
        app.run(
            host="0.0.0.0",
            port=5005,
            debug=False,
            use_reloader=False
        )

    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()
    time.sleep(3)

    yield app

@pytest.fixture()
def driver(sel_app):
    options = Options()

    if os.getenv('GITHUB_ACTIONS'):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        options.add_argument("--window-size=1366,768")

    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--timezone=Asia/Ho_Chi_Minh')

    try:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        driver_name = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
        driver_path = os.path.join(base, ".venv", driver_name)
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    except Exception as e:
        print(e)
        driver = webdriver.Chrome(options=options)

    driver.execute_script("return new Date().getTimezoneOffset();")

    yield driver
    driver.quit()

def reset_selenium_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        seed_data()

@pytest.fixture(autouse=True)
def reset_database(sel_app):
    with sel_app.app_context():
        print("RESET DB")
        reset_selenium_database(sel_app)
    yield
    reset_selenium_database(sel_app)

@pytest.fixture(autouse=True)
def mock_cloudinary_upload(monkeypatch):
    monkeypatch.setattr(
        'cloudinary.uploader.upload',
        lambda file: {'secure_url': 'https://res.cloudinary.com/test/avatar-cute-3.jpg'}
    )

@pytest.fixture(autouse=True, scope="session")
def start_scheduler(sel_app):
    from app import db
    os.environ["WERKZEUG_RUN_MAIN"] = "true"
    scheduler(sel_app, db)
    print('Scheduler start')
    yield

