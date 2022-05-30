from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _


class InfiniteAdminLoginConfig(AppConfig):
    name = "libs.infinite_admin"

    def ready(self):
        self.replace_admin_login_form()

    def replace_admin_login_form(self):
        from django.contrib import admin
        from django.contrib.admin.forms import AdminAuthenticationForm

        from adminactions import actions
        from captcha.fields import CaptchaField
        from django_secure_password_input.fields import DjangoSecurePasswordInput

        class AdminSafeAuthenticationForm(AdminAuthenticationForm):
            password = DjangoSecurePasswordInput(label=_("Password"))
            captcha = CaptchaField(label=_("Captcha"))

        admin.site.login_form = AdminSafeAuthenticationForm

        admin.site.site_title = _("Django Infinity")
        admin.site.site_header = _("Infinite Admin")
        admin.site.index_title = _("Admin")

        # register all adminactions
        actions.add_to_site(admin.site)
