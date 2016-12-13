#!/bin/bash

set -e

rm /home/phablet/.local/share/upstart/sessions/bhdouglass-indicator-weather.conf
rm /home/phablet/.local/share/unity/indicators/com.bhdouglass.indicator.weather

echo "indicator-weather uninstalled"
