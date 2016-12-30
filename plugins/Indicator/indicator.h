#ifndef INDICATOR_H
#define INDICATOR_H

#include <QObject>
#include <QProcess>

class Indicator: public QObject {
    Q_OBJECT

    Q_PROPERTY(bool isInstalled MEMBER m_isInstalled NOTIFY isInstalledChanged)

public:
    Indicator();
    ~Indicator() = default;

    Q_INVOKABLE void install();
    Q_INVOKABLE void uninstall();

Q_SIGNALS:
    void installed(bool success);
    void uninstalled(bool success);

    void isInstalledChanged(const bool isInstalled);

private Q_SLOTS:
    void onInstallFinished(int exitCode, QProcess::ExitStatus exitStatus);
    void onUninstallFinished(int exitCode, QProcess::ExitStatus exitStatus);

private:
    Q_DISABLE_COPY(Indicator)

    bool checkInstalled();

    QProcess m_installProcess;
    QProcess m_uninstallProcess;
    bool m_isInstalled = false;
};

#endif
