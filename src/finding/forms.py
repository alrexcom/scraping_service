from django import forms
from .models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=False,
                                  widget=forms.Select(
                                      attrs={
                                          'class': 'form-select '
                                      }),
                                  label='',
                                  empty_label='Выберете расположение'
                                  )
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name='slug',
                                      required=False,
                                      widget=forms.Select(
                                          attrs={'class': 'form-select mx-3'}),
                                      empty_label='Язык программирования',
                                      label=''
                                      )
