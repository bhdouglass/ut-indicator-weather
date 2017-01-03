#include <QDebug>
#include <QFile>
#include <QDir>
#include <QJsonDocument>
#include <QJsonObject>
#include <QFileInfo>

#include "settings.h"

Settings::Settings() {
    QFile config(m_configPath + "config.json");
    config.open(QFile::ReadOnly);

    QJsonDocument doc = QJsonDocument::fromJson(config.readAll());
    QJsonObject object = doc.object();

    m_provider = object.value("provider").toString().trimmed();
    m_darkSkyApiKey = object.value("api_key").toString().trimmed();
    m_owmApiKey = object.value("owm_api_key").toString().trimmed();
    m_lat = object.value("lat").toString().trimmed();
    m_lng = object.value("lng").toString().trimmed();
    m_unit = object.value("unit").toString().trimmed();

    if (m_provider != "open_weather_map" && m_provider != "dark_sky") {
        m_provider = "dark_sky";
    }

    if (m_unit != "f" && m_unit != "c" && m_unit != "k") {
        m_unit = "f";
    }

    Q_EMIT providerChanged(m_provider);
    Q_EMIT darkSkyApiKeyChanged(m_darkSkyApiKey);
    Q_EMIT owmApiKeyChanged(m_owmApiKey);
    Q_EMIT latChanged(m_lat);
    Q_EMIT lngChanged(m_lng);
    Q_EMIT unitChanged(m_unit);

    config.close();
}

void Settings::save() {
    QJsonObject object;
    object.insert("provider", QJsonValue(m_provider.trimmed()));
    object.insert("api_key", QJsonValue(m_darkSkyApiKey.trimmed()));
    object.insert("owm_api_key", QJsonValue(m_owmApiKey.trimmed()));
    object.insert("lat", QJsonValue(m_lat.trimmed()));
    object.insert("lng", QJsonValue(m_lng.trimmed()));
    object.insert("unit", QJsonValue(m_unit.trimmed()));

    QJsonDocument doc;
    doc.setObject(object);

    if (!QDir(m_configPath).exists()) {
        QDir().mkdir(m_configPath);
    }

    QFile config(m_configPath + "config.json");
    bool success = config.open(QFile::WriteOnly | QFile::Text | QFile::Truncate);
    config.write(doc.toJson());
    config.close();

    Q_EMIT saved(success);
}
