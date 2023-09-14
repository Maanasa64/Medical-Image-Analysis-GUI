# annotations.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsView, QGraphicsScene, QAction, QFileDialog, QGraphicsItem,
    QButtonGroup, QRadioButton
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, QSizeF
from enum import Enum

class AnnotationType(Enum):
    NONE = 0
    FREEHAND = 1
    SQUARE = 2
    CIRCLE = 3
    RECTANGLE = 4
    TRIANGLE = 5
    ELLIPSE = 6

class AnnotationItem(QGraphicsItem):
    def __init__(self, path, pen):
        super().__init__()
        self.path = path
        self.pen = pen

    def boundingRect(self):
        return self.path.boundingRect()

    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawPath(self.path)

    def type(self):
        # Return a unique user type for the custom item
        return QGraphicsItem.UserType + 1
