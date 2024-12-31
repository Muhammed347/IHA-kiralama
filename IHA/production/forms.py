from django import forms
from .models import WingPart, BodyPart, TailPart, AvionicsPart, AirCraft


class BasePartForm(forms.ModelForm):
    class Meta:
        model = None  # Set dynamically for different part models
        fields = ['aircraftname', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #Set status to 'unused' by default
        self.fields['status'].initial = 'unused'


# Extend for each part type
class WingPartForm(BasePartForm):
    class Meta(BasePartForm.Meta):
        model = WingPart

class BodyPartForm(BasePartForm):
    class Meta(BasePartForm.Meta):
        model = BodyPart

class TailPartForm(BasePartForm):
    class Meta(BasePartForm.Meta):
        model = TailPart

class AvionicsPartForm(BasePartForm):
    class Meta(BasePartForm.Meta):
        model = AvionicsPart


class AirCraftForm(forms.ModelForm):
    class Meta:
        model = AirCraft
        fields = ['aircraftname', 'wing', 'body', 'tail', 'avionics']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter each part field to show only unused parts
        self.fields['wing'].queryset = WingPart.objects.filter(status='unused')
        self.fields['body'].queryset = BodyPart.objects.filter(status='unused')
        self.fields['tail'].queryset = TailPart.objects.filter(status='unused')
        self.fields['avionics'].queryset = AvionicsPart.objects.filter(status='unused')
    
    def clean(self):
        cleaned_data = super().clean()
        aircraftname = cleaned_data.get('aircraftname')
        wing = cleaned_data.get('wing')
        body = cleaned_data.get('body')
        tail = cleaned_data.get('tail')
        avionics = cleaned_data.get('avionics')

        # Ensure parts are compatible with the selected aircraft
        if wing and wing.aircraftname != aircraftname:
            self.add_error('wing', 'Selected wing is not compatible with the selected aircraft.')
        if body and body.aircraftname != aircraftname:
            self.add_error('body', 'Selected body is not compatible with the selected aircraft.')
        if tail and tail.aircraftname != aircraftname:
            self.add_error('tail', 'Selected tail is not compatible with the selected aircraft.')
        if avionics and avionics.aircraftname != aircraftname:
            self.add_error('avionics', 'Selected avionics is not compatible with the selected aircraft.')

        return cleaned_data