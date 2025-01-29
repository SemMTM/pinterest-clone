from django import forms
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