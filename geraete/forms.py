from django import forms
from .models import Geraet

class GeraetForm(forms.ModelForm):
    class Meta:
        model = Geraet
        fields = "__all__"
        #"bezeichnung", "identifikation", "seriennummer", "barcode", "kategorie", "status", "fahrzeug", "geraeteraum", "bemerkung"  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Standard-Input-Klassen setzen
            css_class = "form-control"

            # Checkboxen und Radios brauchen Bootstrap-eigene Klassen
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                css_class = "form-check-input"
            
            field.widget.attrs.update({"class": css_class})