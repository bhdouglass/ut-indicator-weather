import QtQuick 2.4
import QtQuick.Layouts 1.1
import Ubuntu.Components 1.3

ColumnLayout {
    id: root

    property var settings

    spacing: units.gu(1)

    function checkCheckboxes() {
        if (!dark_sky.checked && !open_weather_map.checked) {
            dark_sky.checked = true;
        }
    }

    Label {
        text: i18n.tr("Weather Provider")
        Layout.fillWidth: true
    }

    RowLayout {
        Layout.fillWidth: true

        CheckBox {
            id: dark_sky
            checked: settings.provider == 'dark_sky'
            onCheckedChanged: {
                if (checked) {
                    settings.provider = 'dark_sky';
                    dark_sky.checked = true;
                    open_weather_map.checked = false;
                }

                root.checkCheckboxes();
            }
        }

        Label {
            text: i18n.tr("Dark Sky")

            MouseArea {
                anchors.fill: parent
                onClicked: dark_sky.checked = true;
            }
        }
    }

    RowLayout {
        Layout.fillWidth: true

        CheckBox {
            id: open_weather_map
            checked: settings.provider == 'open_weather_map'
            onCheckedChanged: {
                if (checked) {
                    settings.provider = 'open_weather_map';
                    dark_sky.checked = false;
                    open_weather_map.checked = true;
                }

                root.checkCheckboxes();
            }
        }

        Label {
            text: i18n.tr("OpenWeatherMap")

            MouseArea {
                anchors.fill: parent
                onClicked: open_weather_map.checked = true;
            }
        }
    }
}
