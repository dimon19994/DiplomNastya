from flask import render_template, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import check_password_hash

from controllers import _Controller
from models import User


class LoginController(_Controller):
    template = 'login.html'

    def _post(self):
        email = self.request_data.get('email')
        password = self.request_data.get('password')
        remember = True if self.request_data.get('remember') else False

        user = User.select().where(User.email == email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('main.login'))

        login_user(user, remember=remember)

        return redirect(url_for('main.profile'))

    def _get(self):
        return render_template(self.template)
