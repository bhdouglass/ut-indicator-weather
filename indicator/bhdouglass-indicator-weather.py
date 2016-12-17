import sys
import os
import json
import urllib.request
import subprocess
import shlex

from gi.repository import Gio
from gi.repository import GLib

BUS_NAME = 'com.bhdouglass.indicator.weather'
BUS_OBJECT_PATH = '/com/bhdouglass/indicator/weather'
BUS_OBJECT_PATH_PHONE = BUS_OBJECT_PATH + '/phone'

# TODO setup logger with timestamps


class WeatherIndicator(object):
    ROOT_ACTION = 'root'
    CURRENT_ACTION = 'open-current-app'
    FORECAST_ACTION = 'open-forecast-app'
    SETTINGS_ACTION = 'settings'
    MAIN_SECTION = 0

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
    SNOW = 'weather-snow-symbolic'
    STORM = 'weather-storm-symbolic'

    condition_icon_map = {
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
        'hail': SLEET,
        'thunderstorm': STORM,
        'tornado': SEVERE,
    }

    condition_text_map = {
        'clear-day': 'Clear',
        'clear-night': 'Clear',
        'rain': 'Rainy',
        'snow': 'Snowy',
        'sleet': 'Sleet',
        'wind': 'Windy',
        'fog': 'Foggy',
        'cloudy': 'Cloudy',
        'partly-cloudy-day': 'Cloudy',
        'partly-cloudy-night': 'Cloudy',
        'hail': 'Hail',
        'thunderstorm': 'Stormy',
        'tornado': 'Tornado',
    }

    api_key = ''
    lat = ''
    lng = ''
    unit = 'f'

    def __init__(self, bus):
        self.bus = bus
        self.action_group = Gio.SimpleActionGroup()
        self.menu = Gio.Menu()
        self.sub_menu = Gio.Menu()

        self.current_condition_icon = self.CLEAR
        self.current_condition_text = 'Clear'
        self.current_temperature = 75

        config_file = "/home/phablet/.config/indicator-weather.bhdouglass/config.json"  # TODO don't hardcode this
        with open(config_file, 'r') as f:
            config_json = {}
            try:
                config_json = json.load(f)
            except:
                print('Failed to load the config file: {}'.format(str(sys.exc_info()[0])))

            if 'api_key' in config_json:
                self.api_key = config_json['api_key'].strip()

            if 'lat' in config_json:
                self.lat = config_json['lat'].strip()

            if 'lng' in config_json:
                self.lng = config_json['lng'].strip()

            if 'unit' in config_json:
                self.unit = config_json['unit'].strip()

        if self.unit != 'f' and self.unit != 'c' and self.unit != 'k':
            self.unit = 'f'

    def current_action_activated(self, action, data):
        print('current_action_activated')
        subprocess.Popen(shlex.split('ubuntu-app-launch webbrowser-app https://darksky.net/forecast/{},{}'.format(self.lat, self.lng)))
        print('end')

    def forecast_action_activated(self, action, data):
        print('forecast_action_activated')
        subprocess.Popen(shlex.split('ubuntu-app-launch webbrowser-app https://darksky.net/forecast/{},{}'.format(self.lat, self.lng)))
        print('end')

    def settings_action_activated(self, action, data):
        print('settings_action_activated')
        subprocess.Popen(shlex.split('ubuntu-app-launch indicator-weather.bhdouglass_indicator-weather_@VERSION@'))
        print('end')

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
        icon = Gio.ThemedIcon.new_with_default_fallbacks(self.current_condition_icon)
        current_menu_item.set_attribute_value('icon', icon.serialize())
        section.append_item(current_menu_item)

        settings_menu_item = Gio.MenuItem.new('Forecast', 'indicator.{}'.format(self.FORECAST_ACTION))
        section.append_item(settings_menu_item)

        settings_menu_item = Gio.MenuItem.new('Weather Settings', 'indicator.{}'.format(self.SETTINGS_ACTION))
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

    def update_weather(self):
        print('Updating weather')

        units = 'us'
        if self.unit == 'c' or self.unit == 'k':
            units = 'si'

        url = 'https://api.darksky.net/forecast/{}/{},{}?units={}'.format(self.api_key, self.lat, self.lng, units)
        response = urllib.request.urlopen(url)
        if response:
            data = None
            try:
                data = json.loads(response.readall().decode('utf-8'))
            except ValueError:
                data = None

            if data:
                self.current_temperature = int(data['currently']['temperature'])
                self.current_condition_icon = self.condition_icon_map[data['currently']['icon']]
                self.current_condition_text = self.condition_text_map[data['currently']['icon']]

                if self.unit == 'k':
                    self.current_temperature += 273

                print('Updated state to: {}'.format(self.current_state()))

                # TODO figure out why this gives off an error
                self.action_group.change_action_state(self.ROOT_ACTION, self.root_state())
                self.action_group.change_action_state(self.CURRENT_ACTION, GLib.Variant.new_string(self.current_state()))
                self._update_menu()

        else:
            pass  # TODO error handling

        return True  # Make sure we keep running the timeout

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
        vardict.insert_value('label', GLib.Variant.new_string(str(self.current_temperature) + '°'))

        icon = Gio.ThemedIcon.new(self.current_condition_icon)
        vardict.insert_value('icon', icon.serialize())

        return vardict.end()

    def current_state(self):
        return '{} and {}°'.format(self.current_condition_text, self.current_temperature)


if __name__ == '__main__':
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    proxy = Gio.DBusProxy.new_sync(bus, 0, None, 'org.freedesktop.DBus', '/org/freedesktop/DBus', 'org.freedesktop.DBus', None)
    result = proxy.RequestName('(su)', BUS_NAME, 0x4)
    if result != 1:
        print('Error: Bus name is already taken')
        sys.exit(1)

    wi = WeatherIndicator(bus)
    wi.run()

    print('Weather indicator started')
    GLib.MainLoop().run()
