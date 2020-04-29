from flask import Blueprint, render_template, flash
import requests, json
from app.main.form import CountryFinderForm

main = Blueprint('main',__name__)

@main.route("/", methods=['GET','POST'])
@main.route("/home", methods=['GET','POST'])
def home():
    form = CountryFinderForm()
    link = "https://coronavirus-19-api.herokuapp.com/countries"
    json_data = requests.get(link).text
    global_data = json.loads(json_data)[0]
    countries = json.loads(json_data)[1:]
    countries_separated = {}
    for country in countries:
        countries_separated[country['country']] = country
    countries_sorted = sorted(countries_separated, key= lambda x: countries_separated[x]['cases'],reverse=True)
    countries = []
    countries_capitalized = list(countries_sorted)
    for country in countries_sorted:
        countries.append(country.lower())
    if form.validate_on_submit():
        icountry = form.country_field.data.lower()
        if icountry in countries:
            country_index = countries.index(icountry)
            capname = countries_sorted[country_index]
            user_country = {}
            user_country['country'] = capname
            user_country['totalconfirmed'] = countries_separated[capname]['cases']
            user_country['newconfirmed'] = countries_separated[capname]['todayCases']
            user_country['totalrecovered'] = countries_separated[capname]['recovered']
            user_country['totaldeaths'] = countries_separated[capname]['deaths']
            user_country['newdeaths'] = countries_separated[capname]['todayDeaths']
            user_country['totalactive'] = countries_separated[capname]['active']
            position = country_index
            if user_country['totalactive']:
                percent_active = (user_country['totalactive']*100)/user_country['totalconfirmed']
            else:
                percent_active = 0
            if user_country['totalrecovered']:
                percent_recovered = (user_country['totalrecovered']*100)/user_country['totalconfirmed']
            else:
                percent_recovered = 0
            if user_country['totaldeaths']:
                percent_death = (user_country['totaldeaths']*100)/user_country['totalconfirmed']
            else:
                percent_death = 0
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
    fcountry = list(countries_sorted)[0]
    user_country['country'] = fcountry
    user_country['totalconfirmed'] = countries_separated[fcountry]['cases']
    user_country['newconfirmed'] = countries_separated[fcountry]['todayCases']
    user_country['totalrecovered'] = countries_separated[fcountry]['recovered']
    user_country['totaldeaths'] = countries_separated[fcountry]['deaths']
    user_country['totalactive'] = countries_separated[fcountry]['active']
    position = 0
    if user_country['totalactive']:
        percent_active = (user_country['totalactive']*100)/user_country['totalconfirmed']
    else:
        percent_active = 0
    if user_country['totalrecovered']:
        percent_recovered = (user_country['totalrecovered']*100)/user_country['totalconfirmed']
    else:
        percent_recovered = 0
    if user_country['totaldeaths']:
        percent_death = (user_country['totaldeaths']*100)/user_country['totalconfirmed']
    else:
        percent_death = 0
    return render_template('main.html',
                           global_data = global_data,
                           user_country = user_country,
                           form = form,
                           position=position+1,
                           percent_active=round(percent_active,2),
                           percent_recovered=round(percent_recovered,2),
                           percent_death=round(percent_death,2))
