from flask import Flask
from controllers.main_controller import main_bp

app = Flask(
    __name__,
    template_folder="views/templates",  # <─ nơi chứa các file .html
    static_folder="views/static",      # <─ nơi chứa css, images
)
app.secret_key = "your-secret-key"   # BẮT BUỘC: session cần secret_key

app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
