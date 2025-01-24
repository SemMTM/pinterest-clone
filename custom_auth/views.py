from allauth.account.views import LoginView, SignupView
from django.http import JsonResponse
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth'  

class CustomLoginView(LoginView):
    def get(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'html': self.render_to_response(self.get_context_data()).rendered_content
            })
        return super().get(*args, **kwargs)

class CustomSignupView(SignupView):
    def get(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'html': self.render_to_response(self.get_context_data()).rendered_content
            })
        return super().get(*args, **kwargs)
