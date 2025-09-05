import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

UPLOAD_FOLDER = "static/uploads/avatars"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@profile_bp.route("/", methods=["GET", "POST"])
def profile():
    db: Session = SessionLocal()
    user_id = session.get("user_id")

    if not user_id:
        flash("Silakan login dulu.", "danger")
        return redirect(url_for("auth.login"))

    user = db.query(User).filter(User.id == user_id).first()

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        avatar = request.files.get("avatar")

        # Update name & email
        user.name = name
        user.email = email

        # Update password jika diisi
        if password:
            user.password = generate_password_hash(password)

        # Update avatar jika ada
        if avatar and allowed_file(avatar.filename):
            filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(UPLOAD_FOLDER, filename)
            avatar.save(avatar_path)
            user.image = f"uploads/avatars/{filename}"

        db.commit()
        flash("Profil berhasil diperbarui!", "success")
        return redirect(url_for("profile.profile"))

    return render_template("profile.html", user=user)
