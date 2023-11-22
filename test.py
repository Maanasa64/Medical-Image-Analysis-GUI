import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtWidgets
from PyQt5 import *
from PyQt5.QtCore import Qt 

import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

def histogramNormalization(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate the histogram of the grayscale image
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # Calculate the cumulative histogram
    cdf = hist.cumsum()

    # Normalize the cumulative histogram
    cdf_normalized = cdf / cdf.max()

    # Map the normalized cumulative histogram to the range [0, 255]
    lookUpTable = np.uint8(np.round(cdf_normalized * 255))

    # Apply the look-up table to the grayscale image
    normalizedImage = cv2.LUT(gray, lookUpTable)

    return normalizedImage

class HistogramNormalizationWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cvImage = None
        self.qtImage = None

        self.imageLabel = QLabel()
        self.normalizedImageLabel = QLabel()

        self.normalizeButton = QPushButton("Normalize Image")
        self.normalizeButton.clicked.connect(self.normalizeImage)

        layout = QGridLayout()
        layout.addWidget(self.imageLabel, 0, 0)
        layout.addWidget(self.normalizeButton, 1, 0)
        layout.addWidget(self.normalizedImageLabel, 2, 0)

        self.setLayout(layout)

    def setImage(self, cvImage, qtImage):
        self.cvImage = cvImage
        self.qtImage = qtImage

        pixmap = QPixmap.fromImage(qtImage)
        scaledPixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(scaledPixmap)

    def normalizeImage(self):
        normalizedImage = histogramNormalization(self.cvImage)

        # Convert the normalized image to the correct format
        height, width = normalizedImage.shape
        bytesPerLine = 1 * width
        qImg = QImage(normalizedImage.data, width, height, bytesPerLine, QImage.Format_Grayscale8)

        # Scale the QPixmap and set it to the label
        pixmap = QPixmap.fromImage(qImg)
        scaledPixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)
        self.normalizedImageLabel.setPixmap(scaledPixmap)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Load your image here
    image1 = cv2.imread('/Volumes/LENOVO_USB_/Project/Medical-Image-Analysis-GUI/test2.png')
    image2 = QImage('/Volumes/LENOVO_USB_/Project/Medical-Image-Analysis-GUI/test2.png')

    widget = HistogramNormalizationWidget()
    widget.setImage(image1, image2)
    widget.show()

    sys.exit(app.exec_())
