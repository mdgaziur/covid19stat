from flask import Blueprint, render_template, flash
import requests, json
from app.main.form import CountryFinderForm

main = Blueprint('main',__name__)

@main.route("/", methods=['GET','POST'])
@main.route("/home", methods=['GET','POST'])
def home():
    form = CountryFinderForm()
    json_link = "https://api.covid19api.com/summary"
    json_data = requests.get(json_link).text
    json_data.replace('\n','')
    loaded_json = json.loads(json_data)
    global_data = loaded_json['Global']
    loaded_json = sorted(loaded_json['Countries'], key=lambda x: x['TotalConfirmed'],reverse=True)
    countries = loaded_json
    countries_separated = {}
    for country in countries:
        countries_separated[country['Country']] = country
    countries = []
    countries_capitalized = list(countries_separated.keys())
    for country in countries_capitalized:
        countries.append(country.lower())
    if form.validate_on_submit():
        icountry = form.country_field.data.lower()
        if icountry in countries:
            country_index = countries.index(icountry)
            capname = countries_capitalized[country_index]
            user_country = {}
            user_country['country'] = capname
            user_country['totalconfirmed'] = countries_separated[capname]['TotalConfirmed']
            user_country['newconfirmed'] = countries_separated[capname]['NewConfirmed']
            user_country['totalrecovered'] = countries_separated[capname]['TotalRecovered']
            user_country['newrecovered'] = countries_separated[capname]['NewRecovered']
            user_country['totaldeaths'] = countries_separated[capname]['TotalDeaths']
            user_country['newdeaths'] = countries_separated[capname]['TotalDeaths']
            user_country['totalactive'] = (user_country['totalconfirmed']-user_country['totalrecovered']-user_country['totaldeaths'])
            position = country_index
            percent_active = ((user_country['totalconfirmed']-user_country['totalrecovered']-user_country['totaldeaths'])*100)/user_country['totalconfirmed']
            percent_recovered = (user_country['totalrecovered']*100)/user_country['totalconfirmed']
            percent_death = (user_country['totaldeaths']*100)/user_country['totalconfirmed']
            return render_template('main.html',
                                   global_data = global_data,
                                   user_country = user_country,
                                   form = form,
                                   position=position+1,
                                   percent_active=round(percent_active,2),
                                   percent_recovered=round(percent_recovered,2),
                                   percent_death=round(percent_death,2))
        else:
            flash(f"No such country '{form.country_field.data}'!")
    user_country = {}
    fcountry = list(countries_separated.keys())[0]
    user_country['country'] = fcountry
    user_country['totalconfirmed'] = countries_separated[fcountry]['TotalConfirmed']
    user_country['newconfirmed'] = countries_separated[fcountry]['NewConfirmed']
    user_country['totalrecovered'] = countries_separated[fcountry]['TotalRecovered']
    user_country['newrecovered'] = countries_separated[fcountry]['NewRecovered']
    user_country['totaldeaths'] = countries_separated[fcountry]['TotalDeaths']
    position = countries.index(fcountry.lower())
    percent_active = ((int(user_country['totalconfirmed'])-int(user_country['totalrecovered'])-int(user_country['totaldeaths']))*100)/int(user_country['totalconfirmed'])
    percent_recovered = (user_country['totalrecovered']*100)/user_country['totalconfirmed']
    percent_death = (user_country['totaldeaths']*100)/user_country['totalconfirmed']
    return render_template('main.html',
                           global_data = global_data,
                           user_country = user_country,
                           form = form,
                           position=position+1,
                           percent_active=round(percent_active,2),
                           percent_recovered=round(percent_recovered,2),
                           percent_death=round(percent_death,2))
