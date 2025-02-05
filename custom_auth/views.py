from allauth.account.views import LoginView, SignupView
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    """
    Custom login view that supports AJAX-based requests.

    **Models Used:**
    - `auth.User`: Handles authentication for users.

    **Templates Rendered:**
    - Uses the default template specified in `LoginView`.

    **Functionality:**
    - If the request is an AJAX request (`x-requested-with` header is set
      to `XMLHttpRequest`):
      - Renders the login form and returns it as a JSON response.
      - The response contains the rendered HTML of the login form.
    - If the request is a standard `GET` request:
      - Calls the default `get` method of `LoginView`, rendering the
        login page normally.

    **Returned Data (for AJAX Requests):**
    - A JSON response containing the rendered login form.

    **Use Case:**
    - Enables dynamically loading the login form via AJAX, allowing
      integration with modals or partial page updates without
      requiring a full page reload.
    """
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = self.render_to_response(self.get_context_data())
            return JsonResponse({'html': response.rendered_content})
        return super().get(request, *args, **kwargs)


class CustomSignupView(SignupView):
    """
    Custom signup view that supports AJAX-based requests.

    **Models Used:**
    - `auth.User`: Handles user registration.

    **Templates Rendered:**
    - Uses the default template specified in `SignupView`.

    **Functionality:**
    - If the request is an AJAX request (`x-requested-with` header is
      set to `XMLHttpRequest`):
      - Renders the signup form and returns it as a JSON response.
      - The response contains the rendered HTML of the signup form.
    - If the request is a standard `GET` request:
      - Calls the default `get` method of `SignupView`, rendering the
        signup page normally.

    **Returned Data (for AJAX Requests):**
    - A JSON response containing the rendered signup form:
      ```json
      {
          "html": "<form>...</form>"
      }
      ```

    **Use Case:**
    - Enables dynamically loading the signup form via AJAX, allowing
      integration with modals or partial page updates
      without requiring a full page reload.
    """
    def get(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'html': self.render_to_response(self.get_context_data())
                .rendered_content
            })
        return super().get(*args, **kwargs)


def custom_logout(request):
    """
    Handles user logout and redirects to the home page.

    **Models Used:**
    - `auth.User`: The currently authenticated user is logged out.

    **Functionality:**
    - Calls Django's `logout()` function to log out the currently
      authenticated user.
    - Redirects the user to the `'home'` page after logout.

    **Use Case:**
    - Provides a custom logout functionality that ensures users are redirected
      to the home page.
    """
    logout(request)
    return redirect('home')
