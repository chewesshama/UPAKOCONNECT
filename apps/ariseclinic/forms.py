from django import forms
from mtaa import tanzania
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate region choices
        self.fields['delivery_place_region'].choices = [(r, r) for r in list(tanzania)]

        # Dynamically load districts based on selected region
        if 'delivery_place_region' in self.data:
            region = self.data.get('delivery_place_region')
            if region and region in list(tanzania):
                self.fields['delivery_place_district'].choices = [(d, d) for d in list(tanzania.get(region).districts)]
