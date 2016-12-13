#!/bin/bash

set -e

mkdir -p /home/phablet/.config/upstart/
mkdir -p /home/phablet/.local/share/unity/indicators/

cp -v /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/bhdouglass-indicator-weather.conf /home/phablet/.config/upstart/
cp -v /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/com.bhdouglass.indicator.weather /home/phablet/.local/share/unity/indicators/

echo "indicator-weather installed!"
