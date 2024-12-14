#ifndef CALENDAR_VIEW_H
#define CALENDAR_VIEW_H

#include <QGraphicsView>
#include <QGraphicsScene>
#include <QDate>

class CalendarView : public QGraphicsView
{
    Q_OBJECT

    public:
        explicit CalendarView(const QString &viewMode = "day", QWidget *parent = nullptr);

        void initGrid();
        void setViewMode(const QString &mode);
        QDate currentDate() const { return m_currentDate; }

    private:
        QString m_viewMode;
        QDate m_currentDate;
        QGraphicsScene *scene;

        void drawGrid(int totalHours, int days, double intervalHours);
        void drawDayLines(int dayX, int dayHeight, const QDate &date);
        void drawLabels(int dayX, int dayWidth, int labelPadding, const QDate &date);
        void drawIntervals(int dayX, int intervalsPerDay, int intervalWidth, int dayHeight);
        void drawHorizontalLines(int dayHeight, int totalWidth);
};

#endif
