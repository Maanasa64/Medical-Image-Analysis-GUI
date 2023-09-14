# annotation_view.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsView, QGraphicsScene, QAction, QFileDialog, QGraphicsItem,
    QButtonGroup, QRadioButton
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, QSizeF
from enum import Enum
from annotations import AnnotationType
from annotations import AnnotationItem

class AnnotationView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.annotation_type = AnnotationType.NONE
        self.annotation_color = QColor("red")
        self.annotation_items = []
        self.current_item = None
        self.current_path = None
        self.setBackgroundBrush(Qt.black)

    def set_annotation_type(self, annotation_type):
        self.annotation_type = annotation_type

    def mousePressEvent(self, event):
        if self.annotation_type != AnnotationType.NONE:
            self.start_point = self.mapToScene(event.pos())
            self.current_item = None
            if self.annotation_type == AnnotationType.FREEHAND:
                self.current_path = QPainterPath()
                self.current_path.moveTo(self.start_point)

    def mouseMoveEvent(self, event):
        if self.annotation_type != AnnotationType.NONE and hasattr(self, 'start_point'):
            end_point = self.mapToScene(event.pos())
            if self.current_item:
                self.scene().removeItem(self.current_item)

            if self.annotation_type == AnnotationType.FREEHAND:
                if self.current_path:
                    self.current_path.lineTo(end_point)
                    pen = QPen(self.annotation_color)
                    pen.setWidth(2)
                    self.current_item = AnnotationItem(self.current_path, pen)
                    self.scene().addItem(self.current_item)
            else:
                shape_draw_functions = {
                    AnnotationType.SQUARE: self.draw_square,
                    AnnotationType.CIRCLE: self.draw_circle,
                    AnnotationType.RECTANGLE: self.draw_rectangle,
                    AnnotationType.TRIANGLE: self.draw_triangle,
                    AnnotationType.ELLIPSE: self.draw_ellipse
                }
                self.current_item = shape_draw_functions[self.annotation_type](self.start_point, end_point)
                self.scene().addItem(self.current_item)


    def mouseReleaseEvent(self, event):
        if self.annotation_type != AnnotationType.NONE and hasattr(self, 'start_point'):
            end_point = self.mapToScene(event.pos())
            if self.annotation_type != AnnotationType.FREEHAND:
                shape_draw_functions = {
                    AnnotationType.SQUARE: self.draw_square,
                    AnnotationType.CIRCLE: self.draw_circle,
                    AnnotationType.RECTANGLE: self.draw_rectangle,
                    AnnotationType.TRIANGLE: self.draw_triangle,
                    AnnotationType.ELLIPSE: self.draw_ellipse
                }
                self.current_item = shape_draw_functions[self.annotation_type](self.start_point, end_point)
                if self.current_item:
                    self.scene().addItem(self.current_item)
                    self.annotation_items.append(self.current_item)

            delattr(self, 'start_point')  # Remove start_point attribute
            self.current_path = None  # Reset the Freehand path

    def draw_square(self, start_point, end_point):
        size = min(abs(end_point.x() - start_point.x()), abs(end_point.y() - start_point.y()))
        size = max(size, 2)

        # Calculate the top-left point for the square
        top_left = QPointF(min(start_point.x(), end_point.x()), min(start_point.y(), end_point.y()))

        rect = QRectF(top_left, QSizeF(size, size))

        pen = QPen(self.annotation_color)
        pen.setWidth(2)

        return AnnotationItem(QPainterPath().addRect(rect), pen)



    def draw_circle(self, start_point, end_point):
        ellipse = QRectF(start_point, end_point).normalized()
        center = ellipse.center()
        radius = QPointF(center.x() - ellipse.left(), center.y() - ellipse.top()).manhattanLength()
        circle_path = QPainterPath()
        circle_path.addEllipse(center, radius, radius)
        pen = QPen(self.annotation_color)
        pen.setWidth(2)
        return AnnotationItem(circle_path, pen)

    def draw_rectangle(self, start_point, end_point):
        # Calculate the top-left and bottom-right points for the rectangle
        top_left = QPointF(min(start_point.x(), end_point.x()), min(start_point.y(), end_point.y()))
        bottom_right = QPointF(max(start_point.x(), end_point.x()), max(start_point.y(), end_point.y()))

        # Calculate the dimensions of the rectangle
        width = bottom_right.x() - top_left.x()
        height = bottom_right.y() - top_left.y()

        # Ensure the dimensions are at least 2
        width = max(width, 2)
        height = max(height, 2)

        rect = QRectF(top_left, QSizeF(width, height))

        pen = QPen(self.annotation_color)
        pen.setWidth(2)

        return AnnotationItem(QPainterPath().addRect(rect), pen)

    def draw_triangle(self, start_point, end_point):
        triangle = QPainterPath()
        triangle.moveTo(start_point)
        triangle.lineTo(QPointF(start_point.x(), end_point.y()))
        
        # Adjust the Y-coordinate to make it within a valid range
        if end_point.y() < start_point.y():
            end_point.setY(start_point.y() + 1)
        
        triangle.lineTo(end_point)
        triangle.lineTo(start_point)

        pen = QPen(self.annotation_color)
        pen.setWidth(2)

        return AnnotationItem(triangle, pen)



    def draw_ellipse(self, start_point, end_point):
        # Calculate the width and height using Manhattan length
        width = abs(end_point.x() - start_point.x())
        height = abs(end_point.y() - start_point.y())

        # Ensure the dimensions are at least 2
        width = max(width, 2)
        height = max(height, 2)

        # Calculate the top-left point for the ellipse
        top_left = QPointF(min(start_point.x(), end_point.x()), min(start_point.y(), end_point.y()))

        rect = QRectF(top_left, QSizeF(width, height))

        pen = QPen(self.annotation_color)
        pen.setWidth(2)

        return AnnotationItem(QPainterPath().addEllipse(rect), pen)
