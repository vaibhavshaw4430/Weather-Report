import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
	weather_key = ''
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=ce42751eb1ac79149c0c11c35ea3d09d'
	err_msg=''
	msg=''
	msg_class=''
	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(name=new_city).count()
			if existing_city_count==0:
				r = requests.get(url.format(new_city)).json()
				if r['cod'] == 200:
					form.save()
				else:
					err_msg = 'CITY does not exist'
			else:
				err_msg = 'CITY already exists!!'

	if err_msg:
		msg=err_msg
		msg_class = 'is-danger'
	else:
		msg = "City added "
		err_msg= 'is-success'

	form=CityForm()

	
	cities = City.objects.all()
	weather_data = []
	for city in cities:
		response = requests.get(url.format(city)).json()
		
		city_weather = {
			'city' : city.name ,
			'temperature' : response['main']['temp'],
			'description' : response['weather'][0]['description'],
			'icon' : response['weather'][0]['icon']
		}
		weather_data.append(city_weather)

	
	context = {
	'weather_data' : weather_data, 
	'form' : form ,
	'msg' : msg,
	'msg_class' : msg_class
	}
	return render(request,'weather/weather.html',context)