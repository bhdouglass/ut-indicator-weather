import QtQuick 2.4
import QtQuick.Layouts 1.1
import Ubuntu.Components 1.3
import Indicator 1.0
import com.ubuntu.PamAuthentication 0.1

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
                message.text = i18n.tr("Saved the settings, please reboot");
                message.color = UbuntuColors.green;
            }
            else {
                message.text = i18n.tr("Failed to save the settings");
                message.color = UbuntuColors.red;
            }
        }
    }

    function checkCheckboxes() {
        if (!fahrenheit.checked && !celsius.checked && !kelvin.checked) {
            fahrenheit.checked = true;
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

                Image {
                    source: "../assets/darksky.png"

                    MouseArea {
                        anchors.fill: parent
                        onClicked: Qt.openUrlExternally('https://darksky.net/poweredby/')
                    }

                    Layout.preferredWidth: parent.width / 4
                    Layout.preferredHeight: width / 2
                }

                Label {
                    text: i18n.tr("Dark Sky API Key")
                    Layout.fillWidth: true
                }

                TextField {
                    id: apiKey
                    text: settings.apiKey

                    onTextChanged: {
                        settings.apiKey = text;
                    }
                }

                Label {
                    text: i18n.tr("Click to signup for an API key")
                    color: 'blue'

                    MouseArea {
                        anchors.fill: parent
                        onClicked: Qt.openUrlExternally('https://darksky.net/dev/')
                    }
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

                Label {
                    text: i18n.tr("Temperature Unit")
                    Layout.fillWidth: true
                }

                RowLayout {
                    Layout.fillWidth: true

                    CheckBox {
                        id: fahrenheit
                        checked: settings.unit == 'f'
                        onCheckedChanged: {
                            if (checked) {
                                settings.unit = 'f';
                                fahrenheit.checked = true;
                                celsius.checked = false;
                                kelvin.checked = false;
                            }

                            root.checkCheckboxes();
                        }
                    }

                    Label {
                        text: i18n.tr("Fahrenheit")

                        MouseArea {
                            anchors.fill: parent
                            onClicked: fahrenheit.checked = true;
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true

                    CheckBox {
                        id: celsius
                        checked: settings.unit == 'c'
                        onCheckedChanged: {
                            if (checked) {
                                settings.unit = 'c';
                                fahrenheit.checked = false;
                                celsius.checked = true;
                                kelvin.checked = false;
                            }

                            root.checkCheckboxes();
                        }
                    }

                    Label {
                        text: i18n.tr("Celsius")

                        MouseArea {
                            anchors.fill: parent
                            onClicked: celsius.checked = true;
                        }
                    }
                }

                RowLayout {
                    Layout.fillWidth: true

                    CheckBox {
                        id: kelvin
                        checked: settings.unit == 'k'
                        onCheckedChanged: {
                            if (checked) {
                                settings.unit = 'k';
                                fahrenheit.checked = false;
                                celsius.checked = false;
                                kelvin.checked = true;
                            }

                            root.checkCheckboxes();
                        }
                    }

                    Label {
                        text: i18n.tr("Kelvin")

                        MouseArea {
                            anchors.fill: parent
                            onClicked: kelvin.checked = true;
                        }
                    }
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

                        if (Indicator.isInstalledSystem) {
                            pam.displayLoginDialog();
                        }
                        else {
                            Indicator.uninstall();
                        }
                    }
                }

                Label {
                    id: message
                    visible: false
                }
            }
        }
    }

    AuthenticationService {
        id: pam
        serviceName: 'indicator-weather'
        onDenied: Qt.quit();
        onGranted: {
            Indicator.uninstall(pam.password);
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
