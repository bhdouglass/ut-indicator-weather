# Indicator Weather for Ubuntu Touch

A weather indicator for Ubuntu Touch. Indicator Weather uses data from
[Dark Sky](https://darksky.net/poweredby/) to provide a current weather outlook
on the Ubuntu Touch indicator bar.

## About the Indicator

The indicator itself is rather simle. It's a python script that exports a Gtk
menu over DBus. To start the script there is an Upstart config file located at
indicator/bhdouglass-indicator-weather.conf. This starts the indicator when
Unity starts the rest of the indicators. The other important file is
indicator/com.bhdouglass.indicator.weather. This file lets Unity know where to
find the indicator on DBus and where to place the indicator on the indicator bar.

If you are interested in creating your own indicator for Ubuntu Touch and have
questions, I would be glad to help. Just contact me via [my website](https://bhdouglass.com/contact.html).

## Building

The easiest way to compile and package indicator weather is via [clickable](https://github.com/bhdouglass/clickable).

## Logo

The logo is from the [weather icon icon font by Erik Flowers](https://erikflowers.github.io/weather-icons/).

## License

Copyright (C) 2016 [Brian Douglass](http://bhdouglass.com/)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 3, as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranties of MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
