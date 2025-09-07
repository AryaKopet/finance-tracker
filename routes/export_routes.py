from flask import Blueprint, render_template, request, send_file, session, flash, redirect, url_for
from database import SessionLocal
from models.transaction import Transaction
from models import User
from sqlalchemy import extract
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

export_bp = Blueprint("export", __name__, url_prefix="/export")


@export_bp.route("/", methods=["GET", "POST"])
def export():
    if "user_id" not in session:
        flash("Silakan login dulu", "error")
        return redirect(url_for("auth.login"))

    db = SessionLocal()
    user_id = session["user_id"]
    user = db.query(User).get(user_id)

    transactions = []
    if request.method == "POST":
        month = request.form.get("month", type=int)
        year = request.form.get("year", type=int)
        export_type = request.form.get("export_type")

        query = db.query(Transaction).filter_by(user_id=user_id)

        if month and year:
            query = query.filter(
                extract("month", Transaction.date) == month,
                extract("year", Transaction.date) == year
            )

        transactions = query.all()

        if not transactions:
            flash("Tidak ada transaksi pada periode ini!", "error")
            return redirect(url_for("export.export"))

        if export_type == "excel":
            return export_excel(transactions)
        elif export_type == "pdf":
            return export_pdf(transactions)

    db.close()
    return render_template("export.html", user=user)


# fungsi untuk export transaksi ke excel
def export_excel(transactions):
    data = [{
        "Tanggal": t.date.strftime("%d-%m-%Y"),
        "Jenis": "Pemasukan" if t.type == "income" else "Pengeluaran",
        "Nominal": t.amount,
        "Deskripsi": t.description or "",
    } for t in transactions]

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Transaksi")

    output.seek(0)
    return send_file(output,
                     as_attachment=True,
                     download_name=f"laporan_{datetime.now().strftime('%Y%m%d')}.xlsx",
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# fungsi untuk export transaksi ke pdf
def export_pdf(transactions):
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, height - 50, "Laporan Transaksi")

    y = height - 100
    c.setFont("Helvetica", 10)
    for trx in transactions:
        line = f"{trx.date.strftime('%d-%m-%Y')} | {'Pemasukan' if trx.type == 'income' else 'Pengeluaran'} | Rp {trx.amount:,.0f} | {trx.description or ''}"
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    output.seek(0)
    return send_file(output,
                     as_attachment=True,
                     download_name=f"laporan_{datetime.now().strftime('%Y%m%d')}.pdf",
                     mimetype="application/pdf")
