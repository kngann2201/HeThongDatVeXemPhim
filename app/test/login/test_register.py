from app.dao import add_user
from app.test.base_test import test_session,test_app, mock_cloudinary
import hashlib
import pytest
from app.models import Customer
def test_success(test_app,test_session):
    add_user(username='a1'*4, password='Abcd123@', name='admin', avatar=None)
    u=Customer.query.filter(Customer.username.__eq__('a1'*4)).first()
    assert u is not None
    assert u.name=='admin'
    assert u.password==str(hashlib.md5(('1a'*4).encode('utf-8')).hexdigest())
@pytest.mark.parametrize('password',[
    '1a'*3+'1', '12'*4, 'a'*8
])

def test_invalid_password(password):
    with pytest.raises(ValueError):
        add_user(username='a1'*4,password=password,name='admin',avatar=None)

@pytest.mark.parametrize('username',[
    '1a'*2
])
def test_invalid_username(username):
    with pytest.raises(ValueError):
        add_user(username=username,password='1a'*4,name='admin',avatar=None)

def test_exist_username(test_session,mock_cloudinary):
    add_user(username='a1' * 4, password='1a' * 4, name='admin', avatar='abc')
    with pytest.raises(ValueError):
        add_user(username='a1'*4,password='1a'*4,name='admin',avatar='abc')