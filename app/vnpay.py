import hmac
import urllib.parse
import hashlib
from datetime import datetime, timedelta
from flask import request
from app import app


VNPAY_TMN_CODE = app.config["VNPAY_TMN_CODE"]
VNPAY_HASH_SECRET = app.config["VNPAY_HASH_SECRET"]

VNPAY_RETURN_URL = "http://127.0.0.1:5000/vnpay_return"
VNPAY_PAYMENT_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"

# def get_client_ip():
#     return request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]

def build_payment_url(amount, txn_ref, order_info = 'Movie Ticket Payment'):
    vnpay_amount = int(amount*100)
    expire_date = datetime.now() + timedelta(minutes=7)
    str_txn_ref = str(txn_ref)[:20]

    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": VNPAY_TMN_CODE,
        "vnp_Amount": str(vnpay_amount),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": str_txn_ref,
        "vnp_OrderInfo": order_info,
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": VNPAY_RETURN_URL,
        "vnp_IpAddr": request.remote_addr,
        "vnp_CreateDate": datetime.now().strftime('%Y%m%d%H%M%S'),
        "vnp_ExpireDate": expire_date.strftime('%Y%m%d%H%M%S')
    }
    sorted_param = sorted(params.items())
    hash_data = '&'.join(
        f"{k}={urllib.parse.quote_plus(str(v))}" if v is not None else f"{k}="
        for k, v in sorted_param
    )
    print("Các thông số thanh toán đã hash: ", hash_data)

    secure_hash = hmac.new(
        VNPAY_HASH_SECRET.encode(),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    query_string = urllib.parse.urlencode(sorted_param, quote_via=urllib.parse.quote)

    return f"{VNPAY_PAYMENT_URL}?{query_string}&vnp_SecureHash={secure_hash}"