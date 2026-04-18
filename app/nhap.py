# @app.route("/payment/<int:bill_id>")
#     @login_required
#     def payment(bill_id):
#         try:
#             bill = dao.get_bill_by_id(bill_id)
#             txn_ref = f"{bill.id}_{int(time.time())}"
#             payment = dao.add_payment(bill_id=bill_id, txn_ref=txn_ref, amount=bill.total_amount)
#             payment_url = build_payment_url(amount=payment.amount, txn_ref=txn_ref)
#             return redirect(payment_url)
#
#         except Exception as e:
#             return jsonify({"success": False, "error": str(e)})
#
#     @app.route("/vnpay_return")
#     def vnpay_return():
#         res_code = request.args.get("vnp_ResponseCode")
#         trans_id = request.args.get("vnp_TransactionNo")
#         txn_ref = request.args.get("vnp_TxnRef")
#
#         print("Kết quả trả về từ VNPAY")
#         print(res_code)
#         print(trans_id)
#         print(txn_ref)
#
#         payment = Payment.query.filter_by(txn_ref=txn_ref).first()
#
#         if not payment:
#             return "Không tìm thấy thông tin thanh toán!"
#
#         if payment.status != PaymentStatus.PENDING:
#             return "Đã xử lý trước đó"
#
#         payment.vnp_transaction_id = trans_id
#         bill = Payment.query.filter_by(txn_ref=txn_ref).first().bill
#
#         for ticket in bill.tickets:
#             seat = ticket.screening_seat
#             if seat.status != SeatStatus.HOLDING:
#                 dao.pay_fail(payment, bill)
#                 return "Ghế đã bị huỷ trong khi thanh toán!"
#             if seat.hold_expired_at < datetime.now():
#                 dao.pay_fail(payment, bill)
#                 return "Ghế đã hết hạn! Vui lòng đặt mới và thanh toán trong thời gian quy định!"
#
#         if res_code != '00':
#             dao.pay_fail(payment, bill)
#             flash('Thanh toán thất bại!', 'fail')
#             return redirect(url_for('index'))
#
#         dao.pay_success(payment, bill)
#         flash('Đặt vé thành công!', 'success')
#         return redirect(url_for('index'))