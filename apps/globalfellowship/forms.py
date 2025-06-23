from django import forms
from .models import FellowshipMember

class FellowshipMemberForm(forms.ModelForm):
    class Meta:
        model = FellowshipMember
        fields = "__all__"
