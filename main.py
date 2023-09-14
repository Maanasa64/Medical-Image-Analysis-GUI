# main.py
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    image_path = "/Users/maana/Documents/Boolean Lab/cancertissue .png"  
    window.set_image(image_path)
    window.show()

    sys.exit(app.exec_())
