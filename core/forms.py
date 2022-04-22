from django import forms

from .constants import OPERATIONS
from .fields import TextFileField
from .models import Elector, Campaign, VoteOffice


class UploadFileForm(forms.Form):
    picture = TextFileField()
    operation = forms.TypedChoiceField(choices=OPERATIONS, required=False)


class HaveVoteForm(forms.Form):
    matricule = forms.ModelChoiceField(queryset=Elector.objects.all(), to_field_name="matricule")
    campaign = forms.ModelChoiceField(queryset=Campaign.objects.filter(enabled=True, deleted=False))


class AddVoteOffice(forms.Form):
    voteOffice = forms.ModelChoiceField(queryset=VoteOffice.objects.filter(enabled=True, deleted=False))
