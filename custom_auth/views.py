from allauth.account.views import LoginView, SignupView
from django.http import JsonResponse
from django.apps import AppConfig
from django.contrib.auth import logout
from django.shortcuts import redirect

class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = self.render_to_response(self.get_context_data())
            return JsonResponse({'html': response.rendered_content})
        return super().get(request, *args, **kwargs)

class CustomSignupView(SignupView):
    def get(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'html': self.render_to_response(self.get_context_data()).rendered_content
            })
        return super().get(*args, **kwargs)

def custom_logout(request):
    logout(request)
    return redirect('home')