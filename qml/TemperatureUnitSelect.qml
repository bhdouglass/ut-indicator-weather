import QtQuick 2.4
import QtQuick.Layouts 1.1
import Ubuntu.Components 1.3

ColumnLayout {
    id: root

    property var settings

    spacing: units.gu(1)

    function checkCheckboxes() {
        if (!fahrenheit.checked && !celsius.checked && !kelvin.checked) {
            fahrenheit.checked = true;
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
}
