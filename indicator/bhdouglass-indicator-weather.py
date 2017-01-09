import sys
import os
import json
import urllib.request
import subprocess
import shlex
import logging

from gi.repository import Gio
from gi.repository import GLib

import gettext
t = gettext.translation('indicator-weather', fallback=True, localedir='/opt/click.ubuntu.com/indicator-weather.bhdouglass/current/share/locale/')  # TODO don't hardcode this
_ = t.gettext

BUS_NAME = 'com.bhdouglass.indicator.weather'
BUS_OBJECT_PATH = '/com/bhdouglass/indicator/weather'
BUS_OBJECT_PATH_PHONE = BUS_OBJECT_PATH + '/phone'

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class WeatherIndicator(object):
    ROOT_ACTION = 'root'
    CURRENT_ACTION = 'open-current-app'
    FORECAST_ACTION = 'open-forecast-app'
    SETTINGS_ACTION = 'settings'
    MAIN_SECTION = 0
    ERROR_ICON = 'sync-error'

    RAIN = 'weather-chance-of-rain'
    SNOW = 'weather-chance-of-snow'
    CHANCE_STORM = 'weather-chance-of-storm'
    CHANCE_WIND = 'weather-chance-of-wind'
    CLEAR_NIGHT = 'weather-clear-night-symbolic'
    CLEAR = 'weather-clear-symbolic'
    CLOUDY_NIGHT = 'weather-clouds-night-symbolic'
    CLOUDY = 'weather-clouds-symbolic'
    PARTLY_CLOUDY_NIGHT = 'weather-few-clouds-night-symbolic'
    PARTLY_CLOUDY = 'weather-few-clouds-symbolic'
    FLURRIES = 'weather-flurries-symbolic'
    FOG = 'weather-fog-symbolic'
    HAZY = 'weather-hazy-symbolic'
    OVERCAST = 'weather-overcast-symbolic'
    SEVERE = 'weather-severe-alert-symbolic'
    SCATTERED_SHOWERS = 'weather-showers-scattered-symbolic'
    SHOWERS = 'weather-showers-symbolic'
    SLEET = 'weather-sleet-symbolic'
    HAIL = 'weather-sleet-symbolic'
    SNOW = 'weather-snow-symbolic'
    STORM = 'weather-storm-symbolic'

    dark_sky_condition_icon_map = {
        'clear-day': CLEAR,
        'clear-night': CLEAR_NIGHT,
        'rain': RAIN,
        'snow': SNOW,
        'sleet': SLEET,
        'wind': CHANCE_WIND,
        'fog': FOG,
        'cloudy': CLOUDY,
        'partly-cloudy-day': CLOUDY,
        'partly-cloudy-night': CLOUDY_NIGHT,
        'hail': HAIL,
        'thunderstorm': STORM,
        'tornado': SEVERE,
    }

    config_file = "/home/phablet/.config/indicator-weather.bhdouglass/config.json"  # TODO don't hardcode this
    provider = 'dark_sky'
    dark_sky_api_key = ''
    owm_api_key = ''
    lat = ''
    lng = ''
    unit = 'f'
    retry_timeout = 1
    owm_city_id = ''

    def __init__(self, bus):
        self.get_config()

        self.bus = bus
        self.action_group = Gio.SimpleActionGroup()
        self.menu = Gio.Menu()
        self.sub_menu = Gio.Menu()

        self.current_condition_icon = self.CLEAR
        self.current_condition_text = 'Clear'
        self.current_temperature = 75
        self.error = 'No weather data yet'

    def get_config(self):
        with open(self.config_file, 'r') as f:
            config_json = {}
            try:
                config_json = json.load(f)
            except:
                logger.warning('Failed to load the config file: {}'.format(str(sys.exc_info()[1])))

            if 'provider' in config_json:
                self.provider = config_json['provider'].strip()

            if 'api_key' in config_json:
                self.dark_sky_api_key = config_json['api_key'].strip()

            if 'owm_api_key' in config_json:
                self.owm_api_key = config_json['owm_api_key'].strip()

            if 'lat' in config_json:
                self.lat = config_json['lat'].strip()

            if 'lng' in config_json:
                self.lng = config_json['lng'].strip()

            if 'unit' in config_json:
                self.unit = config_json['unit'].strip()

        if self.unit != 'f' and self.unit != 'c' and self.unit != 'k':
            self.unit = 'f'

    def get_translation(self, condition):
        text = ''

        if self.provider == 'dark_sky':
            condition_text_map = {
                'clear-day': _('Clear'),
                'clear-night': _('Clear'),
                'rain': _('Rainy'),
                'snow': _('Snowy'),
                'sleet': _('Sleet'),
                'wind': _('Windy'),
                'fog': _('Foggy'),
                'cloudy': _('Cloudy'),
                'partly-cloudy-day': _('Cloudy'),
                'partly-cloudy-night': _('Cloudy'),
                'hail': _('Hail'),
                'thunderstorm': _('Stormy'),
                'tornado': _('Tornado'),
            }

            if condition in condition_text_map:
                text = condition_text_map[condition]
        else:
            if condition == 800 or condition == 951:  # Clear/Calm
                text = _('Clear')
            elif condition > 800 and condition < 900:  # Clouds
                text = _('Cloudy')
            elif condition >= 700 and condition < 800:  # Atmosphere (mist, fog, etc)
                text = _('Foggy')
            elif condition >= 300 and condition < 400:  # Drizzle
                text = _('Rainy')
            elif condition >= 500 and condition < 600:  # Rain
                text = _('Rainy')
            elif condition >= 200 and condition < 300:  # Thunderstorm
                text = _('Stormy')
            elif condition >= 600 and condition < 700:  # Snow
                text = _('Snowy')
            elif condition == 906:  # Hail
                text = _('Hail')
            elif condition >= 907 and condition < 957:  # Wind
                text = _('Windy')
            elif condition == 905 or (condition >= 957 and condition < 1000):  # Extreme Wind
                text = _('Windy')
            elif condition == 900:  # Tornado
                text = _('Tornado')
            elif condition == 901 or condition == 902 or condition == 962:  # Hurricane
                text = _('Hurricane')
            elif condition == 903:  # Extreme cold
                text = _('Extreme Cold')
            elif condition == 904:  # Extreme heat
                text = _('Extreme Heat')

        return text

    def get_icon(self, condition):
        icon = self.ERROR_ICON
        if self.provider == 'dark_sky':
            if condition in self.dark_sky_condition_icon_map:
                icon = self.dark_sky_condition_icon_map[condition]
        else:
            if condition == 800 or condition == 951:  # Clear/Calm
                icon = self.CLEAR
            elif condition > 800 and condition < 900:  # Clouds
                icon = self.CLOUDY
            elif condition >= 700 and condition < 800:  # Atmosphere (mist, fog, etc)
                icon = self.FOG
            elif condition >= 300 and condition < 400:  # Drizzle
                icon = self.RAIN
            elif condition >= 500 and condition < 600:  # Rain
                icon = self.RAIN
            elif condition >= 200 and condition < 300:  # Thunderstorm
                icon = self.STROM
            elif condition >= 600 and condition < 700:  # Snow
                icon = self.SNOW
            elif condition == 906:  # Hail
                icon = self.HAIL
            elif condition >= 907 and condition < 957:  # Wind
                icon = self.CHANCE_WIND
            elif condition == 905 or (condition >= 957 and condition < 1000):  # Extreme Wind
                icon = self.CHANCE_WIND
            elif condition == 900:  # Tornado
                icon = self.SEVERE
            elif condition == 901 or condition == 902 or condition == 962:  # Hurricane
                icon = self.SEVERE
            elif condition == 903:  # Extreme cold
                icon = self.SEVERE
            elif condition == 904:  # Extreme heat
                icon = self.SEVERE

        return icon

    def current_action_activated(self, action, data):
        logger.debug('current_action_activated')
        subprocess.Popen(shlex.split('ubuntu-app-launch webbrowser-app https://darksky.net/forecast/{},{}'.format(self.lat, self.lng)))

    def forecast_action_activated(self, action, data):
        logger.debug('forecast_action_activated')

        url = ''
        if self.provider == 'dark_sky':
            url = 'https://darksky.net/forecast/{},{}'.format(self.lat, self.lng)
        else:
            if self.owm_city_id:
                url = 'http://openweathermap.org/city/{}'.format(self.owm_city_id)
            else:
                url = 'http://openweathermap.org/'

        subprocess.Popen(shlex.split('ubuntu-app-launch webbrowser-app {}'.format(url)))

    def settings_action_activated(self, action, data):
        logger.debug('settings_action_activated')
        # For some reason ubuntu-app-launch hangs without the version, so let cmake set it for us
        subprocess.Popen(shlex.split('ubuntu-app-launch indicator-weather.bhdouglass_indicator-weather_@VERSION@'))

    def _setup_actions(self):
        root_action = Gio.SimpleAction.new_stateful(self.ROOT_ACTION, None, self.root_state())
        self.action_group.insert(root_action)

        current_action = Gio.SimpleAction.new(self.CURRENT_ACTION, None)
        current_action.connect('activate', self.current_action_activated)
        self.action_group.insert(current_action)

        current_action = Gio.SimpleAction.new(self.FORECAST_ACTION, None)
        current_action.connect('activate', self.forecast_action_activated)
        self.action_group.insert(current_action)

        settings_action = Gio.SimpleAction.new(self.SETTINGS_ACTION, None)
        settings_action.connect('activate', self.settings_action_activated)
        self.action_group.insert(settings_action)

    def _create_section(self):
        section = Gio.Menu()

        current_menu_item = Gio.MenuItem.new(self.current_state(), 'indicator.{}'.format(self.CURRENT_ACTION))
        icon = Gio.ThemedIcon.new_with_default_fallbacks(self.current_icon())
        current_menu_item.set_attribute_value('icon', icon.serialize())
        section.append_item(current_menu_item)

        settings_menu_item = Gio.MenuItem.new(_('Forecast'), 'indicator.{}'.format(self.FORECAST_ACTION))
        section.append_item(settings_menu_item)

        settings_menu_item = Gio.MenuItem.new(_('Weather Settings'), 'indicator.{}'.format(self.SETTINGS_ACTION))
        section.append_item(settings_menu_item)

        return section

    def _setup_menu(self):
        self.sub_menu.insert_section(self.MAIN_SECTION, 'Weather', self._create_section())

        root_menu_item = Gio.MenuItem.new('Weather', 'indicator.{}'.format(self.ROOT_ACTION))
        root_menu_item.set_attribute_value('x-canonical-type', GLib.Variant.new_string('com.canonical.indicator.root'))
        root_menu_item.set_submenu(self.sub_menu)
        self.menu.append_item(root_menu_item)

    def _update_menu(self):
        self.sub_menu.remove(self.MAIN_SECTION)
        self.sub_menu.insert_section(self.MAIN_SECTION, 'Weather', self._create_section())

    def update_weather(self, setup_retry=True):  # TODO see if the network status can be checked/watched
        logger.debug('Updating weather using provider: {}'.format(self.provider))
        self.error = ''

        self.get_config()

        units = 'us'
        if self.unit == 'c' or self.unit == 'k':
            units = 'si'

        if (not self.dark_sky_api_key and self.provider == 'dark_sky') or (not self.owm_api_key and self.provider == 'open_weather_map'):
            self.error = _('Please specify an api key')
            logger.error('no api key')
        elif not self.lat:
            self.error = _('Please specify the latitude')
            logger.error('no latitude')
        elif not self.lng:
            self.error = _('Please specify the longitude')
            logger.error('no longitude')
        else:
            if self.provider == 'dark_sky':
                units = 'us'
                if self.unit == 'c' or self.unit == 'k':
                    units = 'si'

                url = 'https://api.darksky.net/forecast/{}/{},{}?units={}'.format(self.dark_sky_api_key, self.lat, self.lng, units)
                response = None
                try:
                    response = urllib.request.urlopen(url)
                except:
                    self.error = _('Error fetching weather')
                    logger.exception('Failed to get response from the api: {}'.format(str(sys.exc_info()[1])))

                if response:
                    if response.status == 200:
                        data = None
                        try:
                            data = json.loads(response.readall().decode('utf-8'))
                        except ValueError:
                            self.error = _('Error fetching weather')
                            logger.exception('response is not valid json')
                            data = None

                        if data:
                            self.current_temperature = int(data['currently']['temperature'])
                            self.current_condition_icon = self.get_icon(data['currently']['icon'])
                            self.current_condition_text = self.get_translation(data['currently']['icon'])

                            if self.unit == 'k':
                                self.current_temperature += 273

                    else:
                        self.error = _('Error fetching weather')
                        logger.error('unexpected http status code {}'.format(response.status))

                else:
                    self.error = _('Error fetching weather')
                    logger.error('no response')

            else:
                units = ''
                if self.unit == 'f':
                    units = 'imperial'
                elif self.unit == 'c':
                    units = 'metric'

                url = 'http://api.openweathermap.org/data/2.5/weather?APPID={}&lat={}&lon={}&units={}'.format(self.owm_api_key, self.lat, self.lng, units)
                response = None
                try:
                    response = urllib.request.urlopen(url)
                except:
                    self.error = _('Error fetching weather')
                    logger.exception('Failed to get response from the api: {}'.format(str(sys.exc_info()[1])))

                if response:
                    if response.status == 200:
                        data = None
                        try:
                            data = json.loads(response.readall().decode('utf-8'))
                        except ValueError:
                            self.error = _('Error fetching weather')
                            logger.exception('response is not valid json')
                            data = None

                        if data:
                            self.current_temperature = int(data['main']['temp'])
                            self.current_condition_icon = self.get_icon(data['weather'][0]['id'])
                            self.current_condition_text = self.get_translation(data['weather'][0]['id'])
                            self.owm_city_id = data['id']

                    else:
                        self.error = _('Error fetching weather')
                        logger.error('unexpected http status code {}'.format(response.status))

                else:
                    self.error = _('Error fetching weather')
                    logger.error('no response')

        logger.debug('Updated state to: {}'.format(self.current_state()))
        # TODO figure out why this gives off a warning
        self.action_group.change_action_state(self.ROOT_ACTION, self.root_state())
        self.action_group.change_action_state(self.CURRENT_ACTION, GLib.Variant.new_string(self.current_state()))
        self._update_menu()

        if self.error and setup_retry:
            self.retry_timeout = 1
            GLib.timeout_add_seconds(60 * self.retry_timeout, self.retry)

        return True  # Make sure we keep running the timeout

    def retry(self):
        logger.debug('retrying weather update after an error, retry timeout: {}'.format(self.retry_timeout))

        self.update_weather(setup_retry=False)  # Don't create a bunch of timeouts, could get ugly
        if self.error:
            self.retry_timeout += 1

            if self.retry_timeout >= 15:
                self.retry_timeout = 15

            GLib.timeout_add_seconds(60 * self.retry_timeout, self.retry)

        return False  # Don't let the timeout continue to run as we do an incremental backoff

    def run(self):
        self._setup_actions()
        self._setup_menu()

        self.bus.export_action_group(BUS_OBJECT_PATH, self.action_group)
        self.menu_export = self.bus.export_menu_model(BUS_OBJECT_PATH_PHONE, self.menu)

        GLib.timeout_add_seconds(60 * 30, self.update_weather)  # TODO allow this to be configurable
        self.update_weather()

    def root_state(self):
        vardict = GLib.VariantDict.new()
        vardict.insert_value('visible', GLib.Variant.new_boolean(True))
        vardict.insert_value('title', GLib.Variant.new_string('Weather'))

        temperature = str(self.current_temperature) + '°'
        if self.error:
            temperature = ''

        vardict.insert_value('label', GLib.Variant.new_string(temperature))
        icon = Gio.ThemedIcon.new(self.current_icon())
        vardict.insert_value('icon', icon.serialize())

        return vardict.end()

    def current_state(self):
        # TRANSLATORS You must ensure that both {condition} and {temperature} remain intact as they are used for replacing with the actual values. For example: Clear and 75°
        template = _('{condition} and {temperature}°')
        if '{condition}' not in template or '{temperature}' not in template:
            template = '{condition} and {temperature}°'  # Ensure that a bad translation doesn't throw us off

        state = template.format(condition=self.current_condition_text, temperature=self.current_temperature)
        if self.error:
            state = self.error

        return state

    def current_icon(self):
        icon = self.current_condition_icon
        if self.error:
            icon = self.ERROR_ICON

        return icon


if __name__ == '__main__':
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    proxy = Gio.DBusProxy.new_sync(bus, 0, None, 'org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus', None)
    result = proxy.RequestName('(su)', BUS_NAME, 0x4)
    if result != 1:
        logger.critical('Error: Bus name is already taken')
        sys.exit(1)

    wi = WeatherIndicator(bus)
    wi.run()

    logger.debug('Weather Indicator startup completed')
    GLib.MainLoop().run()
