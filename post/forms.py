from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Add a comment",
                    'rows': 2,}
        ),
    )

    class Meta:
        model = Comment
        fields = ('body',)