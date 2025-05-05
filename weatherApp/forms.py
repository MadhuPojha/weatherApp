import requests
from django import forms
from .models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def clean_name(self):
        city_name = self.cleaned_data['name'].capitalize()

        # if already exists in the database
        if City.objects.filter(name=city_name).exists():
            raise forms.ValidationError(f"{city_name} is already in the database!")

        api_key = '8064cd1cd8a24596b87113943242108'  # Replace with your actual API key
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}'

        response = requests.get(url).json()
        if response.get('error'):
            error_message = response['error'].get('message', 'Unknown error')
            raise forms.ValidationError(f"Invalid city name: {city_name}. {error_message}")

        return city_name
