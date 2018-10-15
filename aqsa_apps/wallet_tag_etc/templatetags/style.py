# Author of Aqsa: Yulay Musin
from django import template
from django import forms
register = template.Library()


@register.filter(name='form_control')
def form_control(field):
    return field.as_widget(attrs={'class': 'form-control'})


@register.filter(name='textarea')
def textarea(field):
    return field.as_textarea(
        attrs={'class': 'form-control', 'maxlength': field.field.max_length, 'cols': '50', 'rows': '5'})


@register.filter(name='chosen_select')
def chosen_select(field):
    return field.as_widget(attrs={'class': 'form-control chosen-select'})


@register.filter(name='input_type_date')
def input_type_date(field):
    return field.as_widget(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
