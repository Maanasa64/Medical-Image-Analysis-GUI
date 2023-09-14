import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsView, QGraphicsScene, QAction, QFileDialog, QGraphicsItem,
    QButtonGroup, QRadioButton
)
from PyQt5.QtGui import QPixmap, QPen, QColor, QPainter
from PyQt5.QtCore import Qt, QPointF, QRectF, QSizeF
from enum import Enum

from annotations import AnnotationType, AnnotationItem
from annotation_view import AnnotationView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cancer Tissue Annotation")

        self.darker_blue = "#6495ED"

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.central_widget.setStyleSheet("background-color: white;")

        self.layout = QHBoxLayout(self.central_widget)

        self.annotation_view = AnnotationView(self)
        self.layout.addWidget(self.annotation_view)

        self.is_fullscreen = False

        self.initial_zoom_factor = 0.5

        self.scene = QGraphicsScene(self)
        self.annotation_view.setScene(self.scene)

        self.image_label = QLabel()
        self.image_label.setStyleSheet("background-color: black;")
        self.scene.addWidget(self.image_label)

        self.tool_layout = QVBoxLayout()
        self.layout.addLayout(self.tool_layout)

        self.fullscreen_button = QPushButton("Fullscreen")
        self.fullscreen_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.fullscreen_button)

        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.zoom_out_button)

        self.download_button = QPushButton("Download")
        self.download_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.download_button)

        # Annotation buttons
        self.annotation_button_group = QButtonGroup(self)

        self.freehand_button = QRadioButton("Freehand")
        self.freehand_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.annotation_button_group.addButton(self.freehand_button)
        self.tool_layout.addWidget(self.freehand_button)

        self.square_button = QRadioButton("Square")
        self.square_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.annotation_button_group.addButton(self.square_button)
        self.tool_layout.addWidget(self.square_button)

        self.circle_button = QRadioButton("Circle")
        self.circle_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.annotation_button_group.addButton(self.circle_button)
        self.tool_layout.addWidget(self.circle_button)

        self.rectangle_button = QRadioButton("Rectangle")
        self.rectangle_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.annotation_button_group.addButton(self.rectangle_button)
        self.tool_layout.addWidget(self.rectangle_button)

        self.triangle_button = QRadioButton("Triangle")
        self.triangle_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.annotation_button_group.addButton(self.triangle_button)
        self.tool_layout.addWidget(self.triangle_button)

        self.ellipse_button = QRadioButton("Ellipse")
        self.ellipse_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.annotation_button_group.addButton(self.ellipse_button)
        self.tool_layout.addWidget(self.ellipse_button)

        self.undo_button = QPushButton("Undo")
        self.undo_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.undo_button)

        self.redo_button = QPushButton("Redo")
        self.redo_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.redo_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setStyleSheet(f"background-color: {self.darker_blue}; color: white;")
        self.tool_layout.addWidget(self.clear_button)

        self.annotation_history = []  # Store annotations for undo
        self.redo_history = []  # Store undone annotations for redo

        self.annotation_type = AnnotationType.NONE
        self.annotation_color = QColor("red")
        self.annotation_items = []

        self.logo_label = QLabel()
        logo_pixmap = QPixmap("/Users/maana/Documents/Boolean Lab/BooleanLab.jpeg")
        logo_pixmap = logo_pixmap.scaledToWidth(55)  # Adjust the width as needed
        self.logo_label.setPixmap(logo_pixmap)
        self.layout.addWidget(self.logo_label, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.original_image_path = None

        self.setup_actions()
        self.connect_signals()

    def setup_actions(self):
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_out_action = QAction("Zoom Out", self)
        self.download_action = QAction("Download", self)

        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.download_action.triggered.connect(self.download_image)

        self.addAction(self.zoom_in_action)
        self.addAction(self.zoom_out_action)
        self.addAction(self.download_action)

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True

    def connect_signals(self):
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.download_button.clicked.connect(self.download_image)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        self.freehand_button.clicked.connect(lambda: self.annotation_view.set_annotation_type(AnnotationType.FREEHAND))
        self.square_button.clicked.connect(lambda: self.annotation_view.set_annotation_type(AnnotationType.SQUARE))
        self.circle_button.clicked.connect(lambda: self.annotation_view.set_annotation_type(AnnotationType.CIRCLE))
        self.rectangle_button.clicked.connect(lambda: self.annotation_view.set_annotation_type(AnnotationType.RECTANGLE))
        self.triangle_button.clicked.connect(lambda: self.annotation_view.set_annotation_type(AnnotationType.TRIANGLE))
        self.ellipse_button.clicked.connect(lambda: self.annotation_view.set_annotation_type(AnnotationType.ELLIPSE))

        self.clear_button.clicked.connect(self.clear_annotations)
        self.undo_button.clicked.connect(self.undo_annotation)
        self.redo_button.clicked.connect(self.redo_annotation)

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.original_image_path = image_path

        self.image_label.setPixmap(pixmap)
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        self.annotation_view.resetTransform()
        self.annotation_view.scale(self.initial_zoom_factor, self.initial_zoom_factor)

    def undo_annotation(self):
        if self.annotation_history:
            last_annotation = self.annotation_history.pop()
            self.annotation_items.remove(last_annotation)
            self.scene.removeItem(last_annotation)
            self.redo_history.append(last_annotation)
            self.undo_button.setEnabled(bool(self.annotation_history))

    def redo_annotation(self):
        if self.redo_history:
            redo_annotation = self.redo_history.pop()
            self.annotation_items.append(redo_annotation)
            self.annotation_history.append(redo_annotation)
            self.scene.addItem(redo_annotation)
            self.redo_button.setEnabled(bool(self.redo_history))

    def clear_annotations(self):
        if self.original_image_path:
            # Remove annotation items from the scene
            for item in self.annotation_items:
                self.scene.removeItem(item)

            # Clear the annotation items list
            self.annotation_items.clear()

            # Clear the annotation history
            self.annotation_history.clear()

            # Clear the redo history
            self.redo_history.clear()

            self.undo_button.setEnabled(False)
            self.redo_button.setEnabled(False)

    def zoom_in(self):
        self.annotation_view.scale(1.2, 1.2)

    def zoom_out(self):
        self.annotation_view.scale(0.8, 0.8)

    def download_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Images (*.png);;All Files (*)", options=options
        )

        if file_name:
            pixmap = QPixmap(self.scene.sceneRect().size().toSize())
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            self.scene.render(painter)

            # Iterate through annotation items and paint them on the image
            for item in self.annotation_items:
                item.paint(painter, None, None)

            painter.end()
            pixmap.save(file_name, "PNG")
            print(f"Image with annotations saved as {file_name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    image_path = "/Users/maana/Documents/Boolean Lab/cancertissue .png"
    window.set_image(image_path)
    window.show()

    sys.exit(app.exec_())
