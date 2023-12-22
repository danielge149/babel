from flask import Flask, render_template, session, request
from flask_babel import Babel, _ , format_datetime, format_decimal , format_currency, gettext
from babel import  dates
from datetime import datetime
import pytz

# Crea una instancia de la aplicación Flask
app = Flask(__name__)
# Crea una instancia de Babel y la asocia con la aplicación Flask
babel = Babel(app)
# Establece la clave secreta de la aplicación Flask (usada para sesiones)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# Define los idiomas que admitirá la aplicación
app.config['LANGUAGES'] = ['en', 'es', 'sv', 'fr', 'de', 'es_CO']


# Definir una tupla con las claves de los resultados
result_keys = ['num', 'date', 'currency']

# Decorador @babel.localeselector: registra la función como el selector de idioma
@babel.localeselector
def get_locale():
    # Obtiene el idioma almacenado en la sesión del usuario
    lang = session.get('lang')
    # Imprime el idioma seleccionado (esto puede ser útil para depuración)
    print(f"Idioma seleccionado: {lang}")
    # Devuelve el idioma obtenido de la sesión, o el idioma predeterminado si no está definido
    return lang



# Ruta para la página principal ('/') que maneja tanto solicitudes GET como POST
@app.route('/', methods=['GET', 'POST'])
def index():
    # Obtén el idioma seleccionado desde el formulario (por defecto, 'es' si no está presente)
    selected_lang = request.form.get('lang', 'es')
    # Almacena el idioma seleccionado en la sesión del usuario
    session['lang'] = selected_lang
    # Obtén los resultados actualizados según el idioma seleccionado
    results = get_updated_results(selected_lang)
    # Renderiza la plantilla 'index.html' y pasa los resultados y el idioma seleccionado
    return render_template('index.html', results=results, selected_lang=selected_lang, app=app)



def get_updated_results(selected_lang):
    # Obtener la fecha y hora actual
    
    # Mapeo de idiomas a zonas horarias
    idiomas_zonas = {
        'en': 'America/New_York',
        'es': 'Europe/Madrid',
        'sv': 'Europe/Stockholm',
        'fr': 'Europe/Paris',
        'de': 'Europe/Berlin',
        'es_CO': 'America/Bogota'
    }

    # Obtener la fecha y hora actual del país asociado al idioma
    selected_country = idiomas_zonas.get(selected_lang, 'America/New_York')


        # Obtener la zona horaria del país
    zona_horaria = pytz.timezone(selected_country)
        # Obtener la fecha y hora actual en la zona horaria del país
    fecha_hora_pais = datetime.now(zona_horaria)

        # Crear un diccionario para almacenar los resultados
    results = {}

    # Itera sobre las claves de result_keys
    for key in result_keys:
        # Llama a la función get_result_value para obtener el valor correspondiente a la clave actual
        value = get_result_value(key, selected_lang, fecha_hora_pais)
        # Asigna el valor al diccionario results utilizando la clave actual
        results[key] = value
    # Devuelve el diccionario actualizado
    return results


def get_currency_data(selected_lang):
    # Definir códigos de moneda y tasas de cambio según el código de país
    currency_data = {
        'en': {'code': 'USD', 'rate': 1.0},
        'es': {'code': 'EUR', 'rate': 0.85},
        'sv': {'code': 'SEK', 'rate': 8.50},
        'fr': {'code': 'EUR', 'rate': 0.85},
        'de': {'code': 'EUR', 'rate': 0.85},
        'es_CO': {'code': 'COP', 'rate': 4000.0},
    }

    # Obtener la información de la moneda correspondiente al código de país
    return currency_data.get(selected_lang, {'code': 'USD', 'rate': 1.0})


def get_result_value(key, selected_lang, fecha_hora_pais):
    # Verifica si la clave es 'num'
    if key == 'num':
        # Devuelve el valor formateado como un número decimal (16000 en este caso)
        return format_decimal(16000)
    # Verifica si la clave es 'date'
    elif key == 'date':
        # Formatea y muestra la fecha y hora según el idioma seleccionado
        return dates.format_datetime(fecha_hora_pais, locale=selected_lang)   
    # Verifica si la clave es 'currency'
    elif key == 'currency':
        # Obtiene datos relacionados con la moneda según el idioma seleccionado
        currency_data = get_currency_data(selected_lang) 
        # Cantidad (puedes ajustar este valor según tus necesidades)
        amount = 8
        # Obtiene información de la moneda, como el código y la tasa de cambio
        currency_codes = currency_data['code']
        exchange_rate = currency_data['rate']
        # Calcula el monto local utilizando la tasa de cambio
        local_amount = amount * exchange_rate
        # Devuelve el monto local formateado como moneda
        return format_currency(local_amount, currency_codes)

    
def get_currency_code(selected_lang):
    # Definir códigos de moneda según el idioma
    currency_codes = {'en': 'USD', 'es': 'EUR', 'sv': 'SEK', 'fr': 'EUR', 'de': 'EUR', 'es_CO': 'COP'}

    # Obtener el código de moneda correspondiente al idioma seleccionado
    return currency_codes.get(selected_lang, 'USD')

@app.context_processor
def utility_processor():
    def get_type_translation(selected_lang):
        translations = {
            'en': 'United States',
            'es': 'España',
            'sv': 'Svenska',
            'fr': 'Français',
            'de': 'Deutsch',
            'es_CO': 'Colombia',
        }
        return translations.get(selected_lang, 'English (US)')
    
    return dict(get_type_translation=get_type_translation)


        


if __name__ == '__main__':
    app.run(port=5000, debug=True)

