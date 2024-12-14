#include "ApplicationWindow.h"
#include <QPropertyAnimation>
#include <QDate>


ApplicationWindow::ApplicationWindow(QWidget *parent) : QMainWindow(parent)
{
    setWindowTitle("Task Manager");
    resize(800, 600);
    initUI();
}


void ApplicationWindow::initUI()
{
    setupCentralWidget();
    createCalendarView();
    createButtons();
    createDigitalClock();
    createDateRangeLabel();
    layoutWidgets();
}


void ApplicationWindow::setupCentralWidget()
{
    centralWidget = new QWidget(this);
    setCentralWidget(centralWidget);
}


void ApplicationWindow::createCalendarView()
{
    calendarView = new CalendarView("day", this);
}


void ApplicationWindow::createButtons()
{
    btnDay = new QPushButton("Day View", this);
    btnWeek = new QPushButton("Week View", this);
    btnMonth = new QPushButton("Month View", this);

    connect(btnDay, &QPushButton::clicked, this, [this]() { switchView("day"); });
    connect(btnWeek, &QPushButton::clicked, this, [this]() { switchView("week"); });
    connect(btnMonth, &QPushButton::clicked, this [this]() { switchView("month"); });

    buttonLayout = new QHBoxLayout();
    buttonLayout->addWidget(btnDay);
    buttonLayout->addWidget(btnWeek);
    buttonLayout->addWidget(btnMonth);
}


void ApplicationWindow::createDigitalClock()
{
    digitalClock = new DigitalClock("HH:mm:ss:zzz", this);
    digitalClock->setStyleSheet("font-size: 16px; color: blue;");

    topLayout = new QHBoxLayout();
    topLayout->addWidget(ddigitalClock);
    topLayout->addStretch();
}


void ApplicationWindow::createDateRangeLabel()
{
    dateRangeLabel = new QLabel(this);
    dateRangeLabel->setAlignment(Qt::AlignCenter);
    dateRangeLabel->setStyleSheet("font-size: 14px; font-weight: bold;");
}


void ApplicationWindow::layoutWidgets()
{
    mainLayout = new QVBoxLayout(centralWidget);
    mainLayout->addLayout(topLayout);
    mainLayout->addLayout(buttonLayout);
    mainLayout->addWidget(dateRangeLabel);
    mainLayout->addWidget(calendarView);
}


void ApplicationWindow::updateDateRangeLabel(const QString &viewMode)
{
    if (viewMode == "week")
    {
        QDate startDate = calendarView->currentDate();
        QDate endDate = startDate.addDays(6);
        QString dateRange = startDate.toString("MMM dd") + " - " + endDate.toString("MMM dd");
        dateRangeLabel->setText(dateRange);
    } else
    {
        dateRangeLabel->clear();
    }
}


void ApplicationWindow::switchView(const QString &viewMode)
{
    QRect startRect = calendarView->geometry();
    QRect endRect = startRect.adjusted(0, 0, startRect.width() * 0.05, startRect.height() * 0.05);

    QPropertyAnimation *animation = new QPropertyAnimation(calendarView, "geometry", this);
    animation->setDuration(500);
    animation->setStartValue(startRect);
    animation->setEndValue(endRect);

    connect(animation, &QPropertyAnimation::finished, this, [this, viewMode]()
            {
            calendarView->setViewMode(viewMode);
            calendarView->initGrid();
            updateDateRangeLabel(viewMode);

            QRect startRect = calendarView->geometry();
            QRect endRect = startRect.adjusted(0, 0, -startRect.widt() * 0.05, -startRect.height() * 0.05);

            QPropertyAnimation *reverseAnimation = new QPropertyAnimation(calendarView, "geometry", this);
            reverseAnimation->setDuration(500);
            reverseAnimation->setStartValue(startRect);
            reverseAnimation->setEndValue(endRect);
            reverseAnimation->start(QAbstractAnimation::DeleteWhenStopped);
            });

    animation->start(QAbstractAnimation::DeleteWhenStopped);
}
