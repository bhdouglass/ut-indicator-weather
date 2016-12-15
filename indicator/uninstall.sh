#!/bin/bash

set -e

rm /home/phablet/.config/upstart/bhdouglass-indicator-weather.conf
rm /home/phablet/.local/share/unity/indicators/com.bhdouglass.indicator.weather

echo "indicator-weather uninstalled"
