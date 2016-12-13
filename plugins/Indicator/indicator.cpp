#include <QDebug>
#include <QCoreApplication>
#include <QFileInfo>

#include "indicator.h"

Indicator::Indicator() :
    m_installProcess(),
    m_uninstallProcess()
{
    connect(&m_installProcess, SIGNAL(finished(int, QProcess::ExitStatus)), this, SLOT(onInstallFinished(int, QProcess::ExitStatus)));
    connect(&m_uninstallProcess, SIGNAL(finished(int, QProcess::ExitStatus)), this, SLOT(onUninstallFinished(int, QProcess::ExitStatus)));

    checkInstalled();
}

void Indicator::install() {
    //TODO don't hardcode this
    m_installProcess.start("bash /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/install.sh");
}

void Indicator::uninstall(QString password) {
    QString command = "bash /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/uninstall.sh"; //TODO don't hardcode this
    if (m_isInstalledSystem) {
        command = QString("bash -c \"echo %1 | sudo -S bash /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/uninstall-system.sh\"").arg(password);
    }

    m_uninstallProcess.start(command);
}

void Indicator::onInstallFinished(int exitCode, QProcess::ExitStatus exitStatus) {
    qDebug() << "install finished";
    qDebug() << "stdout" << m_installProcess.readAllStandardOutput();
    qDebug() << "stderr" << m_installProcess.readAllStandardError();
    qDebug() << "exit code" << exitCode << "exit status" << exitStatus;

    checkInstalled();
    Q_EMIT installed(exitCode == 0 && exitStatus == QProcess::NormalExit);
}

void Indicator::onUninstallFinished(int exitCode, QProcess::ExitStatus exitStatus) {
    qDebug() << "uninstall finished";

    if (!m_isInstalledSystem) { //Don't print out the password!
        qDebug() << "stdout" << m_uninstallProcess.readAllStandardOutput();
    }
    qDebug() << "stderr" << m_uninstallProcess.readAllStandardError();
    qDebug() << "exit code" << exitCode << "exit status" << exitStatus;

    checkInstalled();
    Q_EMIT uninstalled(exitCode == 0 && exitStatus == QProcess::NormalExit);
}

bool Indicator::checkInstalled() {
    QFileInfo systemSession("/usr/share/upstart/sessions/bhdouglass-indicator-weather.conf");
    QFileInfo systemIndicator("/usr/share/unity/indicators/com.bhdouglass.indicator.weather");
    QFileInfo session("/home/phablet/.config/upstart/bhdouglass-indicator-weather.conf");
    QFileInfo indicator("/home/phablet/.local/share/unity/indicators/com.bhdouglass.indicator.weather");

    m_isInstalled = (session.exists() && indicator.exists()) || (systemSession.exists() && systemIndicator.exists());
    m_isInstalledSystem = (systemSession.exists() && systemIndicator.exists());
    qDebug() << systemSession.exists() << systemIndicator.exists();
    Q_EMIT isInstalledChanged(m_isInstalled);
    Q_EMIT isInstalledSystemChanged(m_isInstalledSystem);

    return m_isInstalled;
}
