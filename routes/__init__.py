from .auth_routes import init_auth_routes
from .transaction_routes import transaction_bp

def init_routes(app, db):
    # Panggil fungsi untuk inisialisasi semua route autentikasi
    init_auth_routes(app, db)

def init_app(app):
    app.register_blueprint(transaction_bp)