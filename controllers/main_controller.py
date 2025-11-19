from functools import wraps
import os

from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash
)

from models.forms import LoginForm, URLForm
import models.youtube_stream as yt  # yt.extract_video_id, yt.global_video_id

import re

USERNAME = os.getenv("APP_USERNAME", "admin")
PASSWORD = os.getenv("APP_PASSWORD", "123456")

main_bp = Blueprint("main", __name__)

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def url_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'url_entered' not in session:
            return redirect(url_for('main.passfunc'))
        return f(*args, **kwargs)
    return decorated_function

# LOGIN
@main_bp.route("/", methods=["GET", "POST"])
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    # Nếu đã login rồi mà vào / hoặc /login thì cho sang nhập URL luôn
    if session.get("logged_in"):
        return redirect(url_for("main.enter_url"))

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("main.enter_url"))
        else:
            flash("Sai username hoặc password", "danger")

    # GET hoặc validate lỗi: hiển thị form đăng nhập
    return render_template("login.html", form=form)

# Redirect to URL entry if logged in
@main_bp.route('/e')
@login_required
def passfunc():
    session.pop('_flashes', None)
    return redirect(url_for('main.enter_url'))


# Enter video URL
# home
@main_bp.route('/enter_url', methods=['GET', 'POST'])
@login_required
def enter_url():
    try:
      form = URLForm()
      return render_template('push_url.html', form=form)
    except Exception as e:
        return render_template('error_page.html', message=str(e) + " From: /enterurl"), 500


# Submit URL
@main_bp.route("/submit_url", methods=["POST"])
@login_required
def submit_url():
    try:
        form = URLForm()
        if form.validate_on_submit():
            input_url = form.url.data.strip()

            youtube_regex = r'^https?://(www\.)?(youtube\.com/(watch\?v=|live/)|youtu\.be/)[\w-]{11}(&t=\d+s)?$'
            ip_stream_regex = r'^(http:\/\/|rtsp:\/\/).+'

            if re.match(youtube_regex, input_url):
                video_id = yt.extract_video_id(input_url)
                if video_id:
                    yt.global_video_id = video_id
                    yt.global_stream_url = None
                    session["url_entered"] = True
                    return redirect(url_for('main.dashboard'))
                else:
                    flash("❌ Invalid YouTube URL", "danger")
                    return redirect(url_for('main.enter_url'))

            # IP stream URL
            elif re.match(ip_stream_regex, input_url):
                yt.global_stream_url = input_url
                yt.global_video_id = None
                session["url_entered"] = True
                return redirect(url_for('main.dashboard'))

            else:
                # This should not occur if validation works correctly
                flash("❌ Unsupported Webcam URL format", "danger")
                return redirect(url_for('main.enter_url'))

        else:
            flash("❌ Invalid URL!", "danger")
            flash("💡 Use the default or enter a valid YouTube or IP stream URL", "suggestion")
            return redirect(url_for('main.enter_url'))

    except Exception as e:
        return render_template('error_page.html', message=str(e) + " From: /submit"), 500


# -------------------------
# Dashboard (tạm thời: chỉ để không bị lỗi redirect)
# -------------------------
@main_bp.route("/index")
@login_required
@url_required
def dashboard():
    # Tạm in ra URL/ID đã chọn, sau này bạn thay bằng logic detection
    return render_template(
        "index.html",
        video_id=yt.global_video_id,
        stream_url=yt.global_stream_url,
        username=session.get("username")
    )

