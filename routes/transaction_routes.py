from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory, current_app
from models.transaction import Transaction
from database import SessionLocal
from datetime import datetime
from models import User
import os

transaction_bp = Blueprint("transaction", __name__, url_prefix="/transactions")

# Tentukan folder upload (misalnya di dalam static/uploads/struks)
UPLOAD_FOLDER = os.path.join("static", "uploads","struks")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # buat folder jika belum ada


# List transaksi
@transaction_bp.route("/")
def list_transactions():
    if "user_id" not in session:
        flash("Silakan login dulu", "error")
        return redirect(url_for("auth.login"))

    db = SessionLocal()
    trans = db.query(Transaction).filter_by(user_id=session["user_id"]).all()
    user_id = session["user_id"]

    # 🔹 Ambil data user langsung dari database
    user = db.query(User).get(user_id)

    username = session.get("username")
    user_image = session.get("user_image")

    db.close()

    return render_template(
        "transactions.html",
        user=user,
        transactions=trans,
        username=username,
        user_image=user_image
    )

# Tambah transaksi
@transaction_bp.route("/add", methods=["GET", "POST"])
def add_transaction():
    if "user_id" not in session:
        flash("Silakan login dulu", "error")
        return redirect(url_for("auth.login"))

    db = SessionLocal()
    user_id = session["user_id"]
    user = db.query(User).get(user_id)  # 🔹 user selalu tersedia

    if request.method == "POST":
        t_type = request.form["type"]
        amount = request.form["amount"]
        description = request.form.get("description")
        date_str = request.form.get("date")

        # Konversi tanggal
        if date_str:
            try:
                trx_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                flash("Format tanggal tidak valid!", "error")
                db.close()
                return redirect(url_for("transaction.add_transaction"))
        else:
            trx_date = datetime.utcnow()

        # Upload bukti
        proof_file = None
        if "proof_file" in request.files:
            file = request.files["proof_file"]
            if file and file.filename != "":
                proof_file = file.filename
                filepath = os.path.join(UPLOAD_FOLDER, proof_file)
                file.save(filepath)

        # Simpan ke database
        trx = Transaction(
            user_id=user_id,
            type=t_type,
            amount=float(amount),
            description=description,
            date=trx_date,
            proof_file=proof_file,
        )
        db.add(trx)
        db.commit()

        if t_type == "income":
            flash("Berhasil mencatat pemasukan!", "income")
        elif t_type == "expense":
            flash("Berhasil mencatat pengeluaran!", "expense")
        else:
            flash("Transaksi berhasil ditambahkan!", "success")

        db.close()
        return redirect(url_for("transaction.list_transactions"))

    username = session.get("username")  
    user_image = session.get("user_image")

    db.close()
    return render_template(
        "add_transaction.html",
        user=user,
        username=username,
        user_image=user_image,
    )


# Lihat bukti transaksi
@transaction_bp.route("/uploads/struks/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
