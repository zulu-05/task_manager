#ifndef APPLICATION_WINDOW_H
#define APPLICATION_WINDOW_H

#include <QMainWindow>
#include <QWidget>

#include <QHBoxLayout>
#include <QVBoxLayout>

#include <QPushButton>
#include <QLabel>

#include "CalendarView.h"
#include "DigitalClock.h"

class ApplicationWindow : public QMainWindow
{
    Q_OBJECT

    public:
        ApplicationWindow(QWidget *parent = nullptr);

    private:
        void initUI();
        void setupCentralWidget();
        void createCalendarView();
        void createButtons();
        void createDigitalClock();
        void createDateRangeLabel();
        void layoutWidgets();
        void updateDateRangeLabel(const QString &viewMode);
        void switchView(const QString &viewMode);

        QWidget *centralWidget;
        CalendarView *calendarView;
        DigitalClock *digitalClock;
        QLabel *dateRangeLabel;

        QVBoxLayout *mainLayout;
        QHBoxLayout *topLayout;
        QHBoxLayout &buttonLayout;

        QPushButton *btnDay;
        QPushButton *btnWeek;
        QPushButton *btnMonth;
};

#endif 
