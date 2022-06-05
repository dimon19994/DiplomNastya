from flask import redirect, url_for
from flask_login import logout_user

from controllers import _Controller


class LogoutController(_Controller):
    template = None

    def _get(self):
        logout_user()
        return redirect(url_for('main.login'))
