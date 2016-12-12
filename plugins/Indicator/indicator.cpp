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

void Indicator::install(QString password) {
    QString command = QString("bash -c \"echo %1 | sudo -S bash /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/install.sh\"").arg(password); //TODO don't hardcode this
    qDebug() << command;
    m_installProcess.start(command);
}

void Indicator::uninstall(QString password) {
    QString command = QString("bash -c \"echo %1 | sudo -S bash /opt/click.ubuntu.com/indicator-weather.bhdouglass/current/indicator/uninstall.sh\"").arg(password); //TODO don't hardcode this
    m_uninstallProcess.start(command);
}

void Indicator::onInstallFinished(int exitCode, QProcess::ExitStatus exitStatus) {
    qDebug() << "install finished";
    //This prints the password, so don't do it
    //qDebug() << "stdout" << m_installProcess.readAllStandardOutput();
    qDebug() << "stderr" << m_installProcess.readAllStandardError();
    qDebug() << "exit code" << exitCode << "exit status" << exitStatus;

    checkInstalled();
    Q_EMIT installed(exitCode == 0 && exitStatus == QProcess::NormalExit);
}

void Indicator::onUninstallFinished(int exitCode, QProcess::ExitStatus exitStatus) {
    qDebug() << "uninstall finished";
    //qDebug() << "stdout" << m_uninstallProcess.readAllStandardOutput();
    qDebug() << "stderr" << m_uninstallProcess.readAllStandardError();
    qDebug() << "exit code" << exitCode << "exit status" << exitStatus;

    checkInstalled();
    Q_EMIT uninstalled(exitCode == 0 && exitStatus == QProcess::NormalExit);
}

bool Indicator::checkInstalled() {
    QFileInfo session("/usr/share/upstart/sessions/bhdouglass-indicator-weather.conf");
    QFileInfo indicator("/usr/share/unity/indicators/com.bhdouglass.indicator.weather");

    qDebug() << session.exists() << indicator.exists();

    m_isInstalled = (session.exists() && indicator.exists());
    Q_EMIT isInstalledChanged(m_isInstalled);

    return m_isInstalled;
}
