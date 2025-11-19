from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

app = Flask(
    __name__,
    static_folder="views/static",
    template_folder="views/templates"
    )
app.secret_key = "secretkey"  # dùng cho flash messages và form CSRF

# Tạo form login bằng Flask-WTF
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Demo check (thay bằng database)
        if username == "admin" and password == "123":
            flash("Login successful!", "success")
            return redirect(url_for("push_url"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)

class PushURLForm(FlaskForm):
    url = StringField("URL", validators=[DataRequired()])

@app.route("/push_url", methods=["GET", "POST"])
def push_url():
    form = PushURLForm()
    if form.validate_on_submit():
        url = form.url.data

        # Xử lý URL (lưu vào database, gọi API, ...)

        flash("URL pushed successfully!", "success")
        return redirect(url_for("loader"))
    return render_template("push_url.html", form=form)


@app.route("/main_page")
def main_page():
    return render_template("main_page.html")

@app.route("/loader")
def loader():
    return render_template("loader.html")


if __name__ == "__main__":
    app.run(debug=True)
