from django import forms


class VacancyForm(forms.Form):
    vacancy_name = forms.CharField(label="Vacancy name")
