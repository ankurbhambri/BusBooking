from django import forms
from booking.models import Query


class QueryForm(forms.ModelForm):
    """
        Query form
    """
    source = forms.TypedChoiceField(
        coerce=int,
        initial='',
        empty_value=None,
        error_messages={'required': 'Select the appropriate.'},
        widget=forms.Select(
            attrs={"class": "selectpicker", "data-width": "310px"}
        )
    )

    destination = forms.TypedChoiceField(
        coerce=int,
        initial='',
        empty_value=None,
        error_messages={'required': 'Select the appropriate.'},
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    passengers = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", 'rows': 1, 'cols': 20})
    )
    
    date = forms.DateField(
        required=False,
        error_messages={'required': 'Select the date.'},

    )

    class Meta:
        model = Query
        fields = ('attrs',)

    # def clean(self):
    #     if self.has_changed():
    #         cleaned_data = self.cleaned_data
    #         if cleaned_data.get("inspection_status") == InspectionStatus.NOTRECOMMENDED and not cleaned_data.get('remarks'):
    #             self.add_error("remarks", "Please write reason for rejection.")
    #         return cleaned_data