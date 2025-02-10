from django import forms
from .models import Profile
from pathlib import Path


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'first_name', 'last_name', 'profile_image']

        def clean_profile_image(self):
            """ Ensure profile image validation only 
            applies to new uploads. """
            image = self.cleaned_data.get("profile_image")

            # If no new image is uploaded, return existing value
            if not image or isinstance(image,
                                       str) or hasattr(image, "public_id"):
                return image

            # Validate file extension
            extension = Path(image.name).suffix[1:].lower()
            allowed_extensions = ["jpg", "jpeg", "png", "webp"]
            if extension not in allowed_extensions:
                raise forms.ValidationError(
                    f"Invalid file type: {extension}. Allowed: {', '.join(
                        allowed_extensions)}")

            # Validate file size
            max_file_size_mb = 2  # Set max file size
            file_size_mb = image.size / (1024 * 1024)  # Convert bytes to MB
            if file_size_mb > max_file_size_mb:
                raise forms.ValidationError(
                    f"File size exceeds {max_file_size_mb}MB limit.")

            return image
