from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, Post, ImageTags

# Comment Form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['body'].widget.attrs['placeholder'] = 'Add a comment'
        self.fields['body'].widget.attrs['rows'] = '2'


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=ImageTags.objects.all(),
        required=False,
        widget=forms.MultipleHiddenInput, 
        help_text="Select up to 3 tags."
    )

    class Meta:
        model = Post
        fields = ['image', 'title', 'description']

    def clean_tags(self):
        # Ensure no more than 3 tags are selected
        selected_tags = self.cleaned_data.get('tags', [])
        if len(selected_tags) > 3:
            raise forms.ValidationError("You can select a maximum of 3 tags.")
        return selected_tags
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        max_size = 20 * 1024 * 1024  # 20MB in bytes

        if image and image.size > max_size:
            raise ValidationError("The uploaded image exceeds the maximum file size of 20MB.")