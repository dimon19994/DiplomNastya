from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from controllers import _Controller
from constants import DEFAULT_COEFFICIENT, USER_LIMIT, MIN_RESERVE, sale_priority, buy_priority
from eth import EthProtocol


class EditUserCoefficientController(_Controller):
    template = 'edit_user_sale_coefficient.html'

    def _post(self):
        coefficient = round(float(self.request_data.get("coefficient", 0)), 2)
        foreign_coefficient = round(float(self.request_data.get("foreign_coefficient", 0)), 2)

        if coefficient < 0:
            flash("Коефіціент повинен бути більше нуля")
        else:
            current_user.addons["user_sale_coefficient"] = coefficient
            current_user.addons["user_sale_foreign_coefficient"] = foreign_coefficient
            current_user.save()
            flash("Коефіціент успішно змінено")

        return redirect(url_for("main.profile"))

    def _get(self):
        coefficient = current_user.addons.get("user_sale_coefficient", DEFAULT_COEFFICIENT)
        foreign_coefficient = current_user.addons.get("user_sale_foreign_coefficient", DEFAULT_COEFFICIENT)
        return render_template(self.template, coefficient=coefficient, foreign_coefficient=foreign_coefficient)


class EditForeignUserCoefficientController(_Controller):
    template = 'edit_user_buy_coefficient.html'

    def _post(self):
        coefficient = round(float(self.request_data.get("coefficient", 0)), 2)
        foreign_coefficient = round(float(self.request_data.get("foreign_coefficient", 0)), 2)

        if coefficient < 0:
            flash("Коефіціент повинен бути більше нуля")
        else:
            current_user.addons["user_buy_coefficient"] = coefficient
            current_user.addons["user_buy_foreign_coefficient"] = foreign_coefficient
            current_user.save()
            flash("Коефіціент успішно змінено")

        return redirect(url_for("main.profile"))

    def _get(self):
        coefficient = current_user.addons.get("user_buy_coefficient", DEFAULT_COEFFICIENT)
        foreign_coefficient = current_user.addons.get("user_buy_foreign_coefficient", DEFAULT_COEFFICIENT)
        return render_template(self.template, coefficient=coefficient, foreign_coefficient=foreign_coefficient)


class EditUserLimitCoefficientController(_Controller):
    template = 'edit_user_limit_coefficient.html'

    def _post(self):
        coefficient = round(float(self.request_data.get("coefficient", 0)), 2)

        if coefficient < 0:
            flash("Ліміт повинен бути більше нуля")
        else:
            current_user.addons["user_limit"] = coefficient
            current_user.save()
            flash("Ліміт успішно змінено")

        return redirect(url_for("main.profile"))

    def _get(self):
        coefficient = current_user.addons.get("user_limit", USER_LIMIT)
        return render_template(self.template, coefficient=coefficient)


class EditMinReserveCoefficientController(_Controller):
    template = 'edit_min_reserve_coefficient.html'

    def _post(self):
        coefficient = round(float(self.request_data.get("coefficient", 0)), 2)

        if coefficient < 0:
            flash("Резерв повинен бути більше нуля")
        else:
            current_user.addons["min_reserve"] = coefficient
            current_user.save()
            flash("Резерв успішно змінено")

        return redirect(url_for("main.profile"))

    def _get(self):
        coefficient = current_user.addons.get("min_reserve", MIN_RESERVE)
        return render_template(self.template, coefficient=coefficient)


class EditUserSalePriorithyController(_Controller):
    template = 'edit_user_sale_priority.html'

    def _post(self):
        priority_1 = int(self.request_data.get("sale_priority_1", 1))
        priority_2 = int(self.request_data.get("sale_priority_2", 1))
        priority_3 = int(self.request_data.get("sale_priority_3", 1))

        current_user.addons["user_sale_priority"] = [priority_1, priority_2, priority_3]
        current_user.save()
        flash("Пріорітети успішно змінено")

        return redirect(url_for("main.profile"))

    def _get(self):
        priority = current_user.addons.get("user_sale_priority", [1, 2, 3])
        return render_template(self.template, coefficient=priority, values=sale_priority)


class EditUserBuyPriorithyController(_Controller):
    template = 'edit_user_buy_priority.html'

    def _post(self):
        priority_1 = int(self.request_data.get("buy_priority_1", 1))
        priority_2 = int(self.request_data.get("buy_priority_2", 1))
        priority_3 = int(self.request_data.get("buy_priority_3", 1))

        current_user.addons["user_buy_priority"] = [priority_1, priority_2, priority_3]
        current_user.save()
        flash("Пріорітети успішно змінено")

        return redirect(url_for("main.profile"))

    def _get(self):
        priority = current_user.addons.get("user_buy_priority", [1, 2, 3])
        return render_template(self.template, coefficient=priority, values=buy_priority)
