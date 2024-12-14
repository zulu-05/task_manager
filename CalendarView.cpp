#include "CalendarView.h"
#include <QGraphicsTextItem>
#include <QPen>
#include <QFont>


CalendarView::CalendarView(const QString &viewMode, QWidget *parent)
    : QGraphicsView(parent), m_viewMode(viewMode), m_currentDate(QDate::currentDate())
{
    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOn);
    setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setDragMode(QGraphicsView::ScrollHandDrag);

    scene = new QGraphicsScene(this);
    setScene(scene);

    initGrid();
}


void CalendarView::initGrid()
{
    scene->clear();

    int totalHours = (m_viewMode == "day") ? 24 : 24;
    int days = (m_viewMode == "day") ? 1 : (m_viewMode == "week") ? 7 : m_currentDate.daysInMonth();
    double intervalHours = (m_viewMode == "day") ? 0.5 : (m_viewMode == "week") ? 6 : 24;

    drawGrid(totalHours, days, intervalHours);
}


void CalendarView::setViewMode(const QString &mode)
{
    m_viewMode = mode;
}


void CalendarView::drawGrid(int totalHours, int days, double intervalHours)
{
    intervalsPerDay = static_cast<int>(totalHours / intervalHours);
    int intervalWidth = 100;
    int dayWidth = intervalWidth * intervalsPerDay;
    int dayHeight = 400;
    int labelPadding = 20;
    scene->setSceneRect(0, -labelPadding, days * dayWidth, dayHeight + labelPadding);

    QFont font("Arial", 10);
    font.setBold(true);

    for (int day = 0, day < days, ++day)
    {
        int dayX = day * dayWidth;
        QDate date = m_currentDate.addDays(day);
        drawDayLines(dayX, dayHeight, date);
        drawLabels(dayX, dayWidth, labelPadding, date);
        drawIntervals(dayX, intervalsPerDay, intervalWidth, dayHeight);
    }

    drawHorizontalLines(dayHeight, days * dayWidth);
}


void CalendarView::drawDayLines(int dayX, int dayHeight, const QDate &date)
{
    QPen penDay(Qt::SolidLine);
    penDay.setWidth(2);
    penDay.setColor((m_viewMode == "week") ? Qt::blue : Qt::red);

    scene->addLine(dayX, 0, dayX, dayHeight, penDay);
}


void CalendarView::drawLabels(int dayX, int dayWidth, int labelPadding, const QDate &date)
{
    QString labelText;
    if (m_viewMode == "week")
    {
        labelText = date.toString("ddd");
    } else if (m_viewMode == "month") 
    {
        labelText = QString::number(date.day());
    }

    QGraphicsTextItem *label = new QGraphicsTextItem(labelText);
    QFont font("Arial", 10);
    font.setBold(true);
    label->setFont(font);
    int labelWidth = static_cast<int>(label->boundingRect().width());
    label->setPos(dayX + dayWidth / 2 - labelWidth / 2, -labelPadding);
    scene->addItem(label);
}


void CalendarView::drawHorizontalLines(int dayHeight, int totalWidth)
{
    int numHorizontalLines = 10;
    int horizontalSpacing = dayHeight / numHorizontalLines;

    for (int j = 0; j <= numHorizontalLines; ++j)
    {
        int y = j * horizontalSpacing;
        QPen pen(Qt::DotLine);
        pen.setWidth(1);
        scene->addLine(0, y, totalWidth, y, pen);
    }
}
