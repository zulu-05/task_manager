#include <QApplication>
#include "ApplicationWindow.h"


int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    ApplicationWindow window;
    window.show();

    return app.exec();
}
