import yfinance as yf

import sys
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView, QDateTimeAxis, QValueAxis
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QApplication

class Stock:
    def __init__(self, name, from_date, to_date):
        self.name = name
        self.from_date = from_date
        self.to_date = to_date
        self.stock_data = yf.Ticker(self.name).history(start=self.from_date, end=self.to_date)
        
        self.opens= self.stock_data["Open"].tolist()
        self.closes = self.stock_data["Close"].tolist()
        self.highs = self.stock_data["High"].tolist()
        self.lows = self.stock_data["Low"].tolist()
 
        self.unix_dates = [int(timestamp.timestamp()) * 1000 for timestamp in self.stock_data.index] # A function later on expects milliseconds
    
    
    def create_candle_stick_series(self):
        stock_series = QCandlestickSeries()
        stock_series.setName(self.name)
        stock_series.setIncreasingColor(QColor(0, 255, 113, 255))
        stock_series.setDecreasingColor(QColor(218, 13, 79, 255))

        for i in range(len(self.unix_dates)):
            candlestick_set = QCandlestickSet(self.unix_dates[i])
            candlestick_set.setOpen(self.opens[i])
            candlestick_set.setClose(self.closes[i])
            candlestick_set.setHigh(self.highs[i])
            candlestick_set.setLow(self.lows[i])
            stock_series.append(candlestick_set)

        return stock_series

class MainWindow(QMainWindow):
    def __init__(self, stock):
        super().__init__()
        
        self.stock = stock
        self.stock_series = self.stock.create_candle_stick_series()
        self.initUI()

    def initUI(self):
        self.chart = QChart()
        self.chart.addSeries(self.stock_series)
        self.chart.setTitle( f"{self.stock.name} Stock Data ({self.stock.from_date} - {self.stock.to_date})" )
        
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        x_axis = QDateTimeAxis()
        x_axis.setFormat("yyyy-MM-dd")
        x_axis.setTitleText("Date")

        min_date = QDateTime.fromSecsSinceEpoch(self.stock.unix_dates[0] // 1000) # this function expects milliseconds
        max_date = QDateTime.fromSecsSinceEpoch(self.stock.unix_dates[-1] // 1000)

        min_date = min_date.addSecs(-3600 * 24)
        max_date = max_date.addSecs(3600 * 24)

        x_axis.setRange(min_date, max_date)

        x_axis.setTickCount(10)
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.stock_series.attachAxis(x_axis)

        y_axis = QValueAxis()
        y_axis.setTitleText("Stock Price")
        y_axis.setLabelFormat("%.2f")
        self.chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        self.stock_series.attachAxis(y_axis)

        #self.chart.createDefaultAxes()
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chart_view = QChartView(self.chart)
        self.setCentralWidget(self.chart_view)

        self.setWindowTitle("Stock Chart")
        self.resize(800, 600)
        self.show()


if __name__ == '__main__':
    apple = Stock("AAPL", "2024-11-01", "2025-01-01")

    app = QApplication(sys.argv)
    window = MainWindow(apple)
    sys.exit(app.exec())
