from flask import Flask
import os
from dotenv import load_dotenv
from controllers.main_controller import main_bp
from controllers.video_controller import video_bp


load_dotenv()

app = Flask(
    __name__,
    template_folder="views/templates",  # <─ nơi chứa các file .html
    static_folder="views/static",      # <─ nơi chứa css, images
)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')   # BẮT BUỘC: session cần secret_key

from models.decryption import decrypt_file  
decrypt_file()  

from models.sheets import get_service_account_file
SERVICE_ACCOUNT_FILE = get_service_account_file()

app.register_blueprint(main_bp)
app.register_blueprint(video_bp)

if __name__ == "__main__":
    app.run(debug=True)
