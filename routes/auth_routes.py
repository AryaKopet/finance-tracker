from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from models import Transaction
from database import SessionLocal
from sqlalchemy import extract

def init_auth_routes(app, db):
    # =========================
    # REGISTER
    # =========================
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()

            # Validasi input kosong
            if not username:
                flash("Username tidak boleh kosong!", "error")
                return redirect(url_for("register"))
            if not email:
                flash("Email tidak boleh kosong!", "error")
                return redirect(url_for("register"))
            if not password:
                flash("Password tidak boleh kosong!", "error")
                return redirect(url_for("register"))

            # Validasi panjang password
            if len(password) < 8:
                flash("Password harus minimal 8 karakter!", "error")
                return redirect(url_for("register"))

            db_session = SessionLocal()
            existing_user = db_session.query(User).filter_by(email=email).first()
            if existing_user:
                flash("Email sudah terdaftar, coba lagi!", "error")
                db_session.close()
                return redirect(url_for("register"))

            hashed_password = generate_password_hash(password)
            new_user = User(name=username, email=email, password=hashed_password)
            db_session.add(new_user)
            db_session.commit()
            db_session.close()

            flash("Registrasi berhasil! Silakan login.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    # =========================
    # LOGIN
    # =========================
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()

            # === Validasi input kosong ===
            if not email:
                flash("Email tidak boleh kosong!", "error")
                return redirect(url_for("login"))

            if not password:
                flash("Password tidak boleh kosong!", "error")
                return redirect(url_for("login"))

            # === Query user berdasarkan email ===
            db_session = SessionLocal()
            user = db_session.query(User).filter_by(email=email).first()
            db_session.close()

            # === Validasi user dan password ===
            if not user or not check_password_hash(user.password, password):
                flash("Email atau password salah!", "error")
                return redirect(url_for("login"))

            # === Login berhasil ===
            session["user_id"] = user.id
            session["username"] = user.name
            flash(f"Selamat datang, {user.name}!", "success")
            return redirect(url_for("dashboard"))

        return render_template("login.html")

    # =========================
    # DASHBOARD
    # =========================
    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu!", "error")
            return redirect(url_for("login"))

        db = SessionLocal()
        user_id = session["user_id"]
        
        # 🔹 Ambil data user langsung dari database
        user = db.query(User).get(user_id)

        # Ambil filter bulan & tahun dari query params
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)

        query = db.query(Transaction).filter_by(user_id=user_id)

        if month and year:
            query = query.filter(
                extract("month", Transaction.date) == month,
                extract("year", Transaction.date) == year
            )

        transactions = query.all()

        # Hitung total pemasukan & pengeluaran
        total_income = sum([t.amount for t in transactions if t.type == "income"])
        total_expense = sum([t.amount for t in transactions if t.type == "expense"])
        total_balance = total_income - total_expense

        db.close()

        return render_template(
            "index.html",
            user=user,
            username=session.get("username"),
            user_image=session.get("user_image"),
            total_income=total_income,
            total_expense=total_expense,
            total_balance=total_balance,
            selected_month=month,
            selected_year=year,
        )

    # =========================
    # LOGOUT
    # =========================
    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        session.pop("username", None)
        flash("Kamu telah logout.", "error")
        return redirect(url_for("login"))
