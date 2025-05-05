from django.shortcuts import render
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm

def index(request):
    cities = City.objects.all() 
    weather_data = []

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            form.save()  
            #messages.success(request, f"{new_city} has been added to the database!")
        else:
            for error in form.errors.get('name', []):
                messages.error(request, error)

    form = CityForm()
    
    for city in cities:
        api_key = '8064cd1cd8a24596b87113943242108'  
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city.name}'

        response = requests.get(url).json()
        
        if 'error' not in response:  
            weather = {
                'city': city.name,
                'temperature': response['current']['temp_c'],
                'description': response['current']['condition']['text']
            }
            weather_data.append(weather)
        else:
            messages.error(request, f"Error fetching weather for {city.name}.")

    context = {
        'weather_data': weather_data,
        'form': form
    }

    return render(request, 'weather/index.html', context)
