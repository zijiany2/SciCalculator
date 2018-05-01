from PyQt4 import Qt
import view
import sys
# The main function to initialize the app and create the GUI object
app = Qt.QApplication(sys.argv)
GUI = view.Window()
sys.exit(app.exec_())
