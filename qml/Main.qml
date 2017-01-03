import QtQuick 2.4
import QtQuick.Layouts 1.1
import Ubuntu.Components 1.3
import Indicator 1.0

MainView {
    id: root
    objectName: 'mainView'
    applicationName: 'indicator-weather'
    automaticOrientation: true

    width: units.gu(45)
    height: units.gu(75)

    Settings {
        id:settings

        onSaved: {
            message.visible = true;
            if (success) {
                if (
                    (!settings.darkSkyApiKey && settings.provider == 'dark_sky') ||
                    (!settings.owmApiKey && settings.provider == 'open_weather_map')
                ) {
                    message.text = i18n.tr("Please specify an api key");
                    message.color = UbuntuColors.orange;
                }
                else if (!settings.lat) {
                    message.text = i18n.tr("Please specify the latitude");
                    message.color = UbuntuColors.orange;
                }
                else if (!settings.lng) {
                    message.text = i18n.tr("Please specify the longitude");
                    message.color = UbuntuColors.orange;
                }
                else {
                    message.text = i18n.tr("Saved the settings, please reboot");
                    message.color = UbuntuColors.green;
                }
            }
            else {
                message.text = i18n.tr("Failed to save the settings");
                message.color = UbuntuColors.red;
            }
        }
    }

    Page {
        header: PageHeader {
            id: header
            title: i18n.tr("Indicator Weather")
        }

        Flickable {
            anchors {
                top: header.bottom
                left: parent.left
                right: parent.right
                bottom: parent.bottom
            }

            clip: true
            contentHeight: contentColumn.height + units.gu(4)

            ColumnLayout {
                id: contentColumn
                anchors {
                    left: parent.left
                    top: parent.top
                    right: parent.right
                    margins: units.gu(2)
                }
                spacing: units.gu(1)

                WeatherProviderSelect {
                    settings: settings
                    Layout.fillWidth: true
                }

                Rectangle { // Spacer
                    Layout.preferredHeight: units.gu(1)
                }

                Image {
                    visible: settings.provider == 'dark_sky'
                    source: "../assets/darksky.png"

                    MouseArea {
                        anchors.fill: parent
                        onClicked: Qt.openUrlExternally('https://darksky.net/poweredby/')
                    }

                    Layout.preferredWidth: parent.width / 4
                    Layout.preferredHeight: width / 2
                }

                Label {
                    visible: settings.provider == 'dark_sky'
                    text: i18n.tr("Dark Sky API Key")
                    Layout.fillWidth: true
                }

                TextField {
                    visible: settings.provider == 'dark_sky'
                    id: darkSkyApiKey
                    text: settings.darkSkyApiKey

                    onTextChanged: {
                        settings.darkSkyApiKey = text;
                    }
                }

                Label {
                    visible: settings.provider == 'open_weather_map'
                    text: i18n.tr("OpenWeatherMap API Key")
                    Layout.fillWidth: true
                }

                TextField {
                    visible: settings.provider == 'open_weather_map'
                    id: owmApiKey
                    text: settings.owmApiKey

                    onTextChanged: {
                        settings.owmApiKey = text;
                    }
                }

                Label {
                    visible: settings.provider == 'open_weather_map'
                    text: i18n.tr("Click to signup for an API key")
                    color: 'blue'

                    MouseArea {
                        anchors.fill: parent
                        onClicked: Qt.openUrlExternally('https://openweathermap.org/appid')
                    }
                }

                Rectangle { // Spacer
                    Layout.preferredHeight: units.gu(1)
                }

                Label {
                    text: i18n.tr("Latitude")
                    Layout.fillWidth: true
                }

                TextField {
                    id: lat
                    text: settings.lat

                    onTextChanged: {
                        settings.lat = text;
                    }
                }

                Label {
                    text: i18n.tr("Longitude")
                    Layout.fillWidth: true
                }

                TextField {
                    id: lng
                    text: settings.lng

                    onTextChanged: {
                        settings.lng = text;
                    }
                }

                Rectangle { // Spacer
                    Layout.preferredHeight: units.gu(1)
                }

                TemperatureUnitSelect {
                    settings: settings
                    Layout.fillWidth: true
                }

                Rectangle { // Spacer
                    Layout.preferredHeight: units.gu(1)
                }

                Button {
                    text: i18n.tr("Save")
                    onClicked: {
                        message.visible = false;
                        settings.save();
                    }
                    color: UbuntuColors.orange
                }

                Button {
                    visible: !Indicator.isInstalled

                    text: i18n.tr("Install Indicator")
                    onClicked: {
                        message.visible = false;
                        Indicator.install();
                    }
                    color: UbuntuColors.green
                }

                Button {
                    visible: Indicator.isInstalled

                    text: i18n.tr("Uninstall Indicator")
                    onClicked: {
                        message.visible = false;
                        Indicator.uninstall();
                    }
                }

                Label {
                    id: message
                    visible: false
                }
            }
        }
    }

    Connections {
        target: Indicator

        onInstalled: {
            message.visible = true;
            if (success) {
                message.text = i18n.tr("Successfully installed, please reboot");
                message.color = UbuntuColors.green;
            }
            else {
                message.text = i18n.tr("Failed to install");
                message.color = UbuntuColors.red;
            }
        }

        onUninstalled: {
            message.visible = true;
            if (success) {
                message.text = i18n.tr("Successfully uninstalled, please reboot");
                message.color = UbuntuColors.green;
            }
            else {
                message.text = i18n.tr("Failed to uninstall");
                message.color = UbuntuColors.red;
            }
        }
    }
}
