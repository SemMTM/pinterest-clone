from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['body'].widget.attrs['placeholder'] = 'Add a comment'
        self.fields['body'].widget.attrs['rows'] = '2'