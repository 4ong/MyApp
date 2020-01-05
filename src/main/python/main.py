from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QToolBar
from PyQt5 import QtWebEngineWidgets, QtCore, QtGui, QtWidgets
import sys
import bokeh
from io import BytesIO
import numpy as np
import holoviews as hv
import pyviz_comms

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    def qt_message_handler(mode, context, message):
        if mode == QtCore.QtInfoMsg:
            mode = 'INFO'
        elif mode == QtCore.QtWarningMsg:
            mode = 'WARNING'
        elif mode == QtCore.QtCriticalMsg:
            mode = 'CRITICAL'
        elif mode == QtCore.QtFatalMsg:
            mode = 'FATAL'
        else:
            mode = 'DEBUG'
        print('qt_message_handler: line: %d, func: %s(), file: %s' % (
            context.line, context.function, context.file))
        print('  %s: %s\n' % (mode, message))


    QtCore.qInstallMessageHandler(qt_message_handler)


    class Ui_Dialog(object):
        def setupUi(self, Dialog):
            Dialog.setObjectName("Dialog")
            Dialog.resize(666, 493)
            self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
            self.buttonBox.setGeometry(QtCore.QRect(30, 430, 341, 32))
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
            self.buttonBox.setObjectName("buttonBox")
            self.checkBox = QtWidgets.QCheckBox(Dialog)
            self.checkBox.setGeometry(QtCore.QRect(10, 390, 85, 24))
            self.checkBox.setObjectName("checkBox1")
            self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
            self.checkBox_2.setGeometry(QtCore.QRect(120, 390, 85, 24))
            self.checkBox_2.setObjectName("checkBox2")
            self.webView = QtWebEngineWidgets.QWebEngineView(Dialog)
            self.webView.setGeometry(QtCore.QRect(0, 0, 671, 381))
            self.webView.setUrl(QtCore.QUrl("about:blank"))
            self.webView.setObjectName("webView")

            # Bokeh test
            def bokeh_test():
                if self.webView.isHidden():
                    self.webView.show()
                else:
                    curve = hv.Curve(range(10))
                    img = hv.Image(np.random.rand(10, 10))
                    buf = BytesIO()
                    hv.save(curve + img, buf, backend='bokeh', fmt='html')
                    self.html = buf.read().decode()
                    self.webView.setHtml(self.html)
                    self.webView.adjustSize()

            self.retranslateUi(Dialog)
            self.buttonBox.accepted.connect(Dialog.accept)
            self.buttonBox.rejected.connect(Dialog.reject)
            self.checkBox.stateChanged['int'].connect(self.webView.hide)
            self.checkBox_2.stateChanged['int'].connect(bokeh_test)
            QtCore.QMetaObject.connectSlotsByName(Dialog)

        def retranslateUi(self, Dialog):
            _translate = QtCore.QCoreApplication.translate
            Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
            self.checkBox.setText(_translate("Dialog", "Hide"))
            self.checkBox_2.setText(_translate("Dialog", "Show"))


    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
