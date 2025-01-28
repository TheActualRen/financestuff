import yfinance as yf

import sys
from PySide6.QtCharts import QCandlestickSeries, QCandlestickSet, QChart, QChartView
from PySide6.QtCore import Qt
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
 
        self.unix_dates = [int(timestamp.timestamp()) for timestamp in self.stock_data.index]
    
    
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

        self.chart.createDefaultAxes()
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
