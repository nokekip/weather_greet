import requests
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def hello(request):
    """
    View function that returns a greeting message with the current temperature based on the visitor's IP address.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A Response object containing the requester's IP address, location, and greeting message.
    """

    visitor_name = request.GET.get('visitor_name', 'Guest')
    API_KEY = os.environ.get('WEATHER_API_KEY')

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    location = requests.get(f'https://ipapi.co/{ip}/json/').json()
    city = location['city']
    # country = location['country_name']
    # lon = location['longitude']
    # lat = location['latitude']

    weather_response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}').json()
    temperature = int(round(weather_response['main']['temp'] - 273))

    greeting = f'Hello {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'

    response = {
        'client_ip': ip,
        'location': city,
        'greeting': greeting
    }

    return Response(response)
