from django import forms

# Choices for Water Demand Types
DEMAND_TYPE_CHOICES = [
    ('domestic', 'Domestic Demand'),
    ('floating', 'Floating Population Demand'),
    ('institutional', 'Institutional Demand'),
    ('firefighting', 'Fire Fighting Demand'),
    ('total', 'Total Demand'),
]

class WaterDemandForm(forms.Form):
    water_demand_type = forms.ChoiceField(
        choices=DEMAND_TYPE_CHOICES,
        label="Water Demand Estimation Type",
        required=True,
    )
    state = forms.ChoiceField(
        label="State",
        required=False,
        widget=forms.Select(attrs={'id': 'id_state'}),
    )
    district = forms.ChoiceField(
        label="District",
        required=False,
        widget=forms.Select(attrs={'id': 'id_district'}),
    )
    subdistrict = forms.ChoiceField(
        label="Subdistrict",
        required=False,
        widget=forms.Select(attrs={'id': 'id_subdistrict'}),
    )
    village = forms.MultipleChoiceField(
        label="Village",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_village'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize dropdowns with empty values
        self.fields['state'].choices = [('', '--- Select State ---')]
        self.fields['district'].choices = [('', '--- Select District ---')]
        self.fields['subdistrict'].choices = [('', '--- Select Subdistrict ---')]
        self.fields['village'].choices = []  # Villages will be dynamically populated
