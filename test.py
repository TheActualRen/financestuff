import sys
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtChart import QCandlestickSeries, QChart, QChartView, QBarCategoryAxis, QValueAxis, QCandlestickSet

def main():
    # Example data (replace with your actual data)
    dates = [1638316800000, 1638403200000, 1638489600000]  # Epoch timestamps in milliseconds
    open = [100, 105, 102]
    high = [110, 108, 106]
    low = [95, 98, 100]
    close = [108, 102, 105]

    app = QApplication(sys.argv)

    # Create a candlestick series
    acme_series = QCandlestickSeries()
    acme_series.setName("Acme Ltd")
    acme_series.setIncreasingColor(QColor(Qt.green))
    acme_series.setDecreasingColor(QColor(Qt.red))

    # Populate the series with data
    categories = []
    for i in range(len(dates)):
        candlestick_set = QCandlestickSet()
        candlestick_set.setTimestamp(dates[i])  # Set the timestamp
        candlestick_set.setOpen(open[i])        # Set the open value
        candlestick_set.setHigh(high[i])        # Set the high value
        candlestick_set.setLow(low[i])          # Set the low value
        candlestick_set.setClose(close[i])      # Set the close value
        acme_series.append(candlestick_set)     # Add the set to the series

        # Add the date to the categories for the X-axis
        categories.append(QDateTime.fromMSecsSinceEpoch(dates[i]).toString("dd"))

    # Create the chart
    chart = QChart()
    chart.addSeries(acme_series)
    chart.setTitle("Acme Ltd Historical Data (July 2015)")
    chart.setAnimationOptions(QChart.SeriesAnimations)

    # Create and configure the X-axis (categories)
    axis_x = QBarCategoryAxis()
    axis_x.append(categories)
    chart.createDefaultAxes()
    chart.setAxisX(axis_x, acme_series)

    # Create and configure the Y-axis (values)
    axis_y = QValueAxis()
    axis_y.setMax(max(high) * 1.01)  # Add a small margin to the max value
    axis_y.setMin(min(low) * 0.99)   # Add a small margin to the min value
    chart.setAxisY(axis_y, acme_series)

    # Configure the legend
    chart.legend().setVisible(True)
    chart.legend().setAlignment(Qt.AlignBottom)

    # Create the chart view and enable antialiasing
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)

    # Create the main window and set the chart view as the central widget
    window = QMainWindow()
    window.setCentralWidget(chart_view)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
