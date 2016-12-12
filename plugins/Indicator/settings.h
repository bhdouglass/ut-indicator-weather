#ifndef SETTINGS_H
#define SETTINGS_H

#include <QObject>

class Settings: public QObject {
    Q_OBJECT

    Q_PROPERTY(QString apiKey MEMBER m_apiKey NOTIFY apiKeyChanged)
    Q_PROPERTY(QString lat MEMBER m_lat NOTIFY latChanged)
    Q_PROPERTY(QString lng MEMBER m_lng NOTIFY lngChanged)
    Q_PROPERTY(QString unit MEMBER m_unit NOTIFY unitChanged)

public:
    Settings();
    ~Settings() = default;

    Q_INVOKABLE void save();
    Q_INVOKABLE void install(QString password);
    Q_INVOKABLE void uninstall(QString password);

Q_SIGNALS:
    void saved(bool success);

    void apiKeyChanged(const QString &apiKey);
    void latChanged(const QString &lat);
    void lngChanged(const QString &lng);
    void unitChanged(const QString &unit);

private:
    QString m_configPath = "/home/phablet/.config/indicator-weather.bhdouglass/"; //TODO don't hardcode this

    QString m_apiKey;
    QString m_lat;
    QString m_lng;
    QString m_unit = "f";
};

#endif
