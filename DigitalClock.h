#ifndef DIGITAL_CLOCK_H
#define DIGITAL_CLOCK_H

#include <QLabel>
#include <QTimer>

class DigitalClock : public QLabel
{
    Q_OBJECT

    public:
        explicit DigitalClock(const QString &format = "HH:mm:ss:zzz", QWidget *parent = nullptr);

    private slots:
        void updateTime();

    private:
        QString timeFormat;
        QTimer *timer;
};

#endif
