#!/bin/bash

cp -v /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/bhdouglass-indicator-weather.conf /usr/share/upstart/sessions/
cp -v /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/com.bhdouglass.indicator.weather /usr/share/unity/indicators/

echo "indicator-weather installed!"
