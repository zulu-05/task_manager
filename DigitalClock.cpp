#include "DigitalClock.h"
#include <QTime>

DigitalClock::DigitalClock(const QString &format, QWidget *parent)
    : QLabel(parent), timeFormat(format)
{
    timer = new QTimer(this);
    connect(timer, &QTimer::timeout, this, &DigitalClock::updateTime);
    timer->start(1000);
    updateTime();
}

void DigitalClock::updateTime()
{
    setText(QTime::currentTime().toString(timeFormat));
}
