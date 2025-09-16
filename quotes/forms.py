from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
        labels = {
            'text': 'Текст цитаты',
            'source': 'Источник',
            'weight': 'Вес (1-10)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.all()


