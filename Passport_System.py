import sys
import random
import smtplib
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QMainWindow, QGraphicsDropShadowEffect, QSizeGrip
from PyQt5.uic import loadUi

# Define file paths
USER_DATA_FILE = "Your file path for data storage in txt format"
STATUS_DATA_FILE = "Your file path for data storage in txt format"
PAYMENT_DATA_FILE = "Your file path for data storage in txt format"
REGISTRATION_DATA_FILE = "Your file path for data storage in txt format"

def read_users():
    users = {}
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    except FileNotFoundError:
        pass
    return users

def write_user(username, password):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{username},{password}\n")

def read_status():
    status = {}
    try:
        with open(STATUS_DATA_FILE, "r") as file:
            for line in file:
                username, status_value = line.strip().split(',')
                status[username] = status_value
    except FileNotFoundError:
        pass
    return status

def write_status(username, status_value):
    with open(STATUS_DATA_FILE, "a") as file:
        file.write(f"{username},{status_value}\n")

def write_registration(details):
    with open(REGISTRATION_DATA_FILE, "a") as file:
        file.write(f"{details}\n")

def write_payment(details):
    with open(PAYMENT_DATA_FILE, "a") as file:
        file.write(f"{details}\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainwindowui.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("PASSPORT AUTOMATION UI")
        QSizeGrip(self.size_grip)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.centralwidget.setGraphicsEffect(self.shadow)
        self.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        self.close_window_button.clicked.connect(lambda: self.close())
        self.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())
        self.user_btn.clicked.connect(self.gotocreate_login)
        self.loginbtn.clicked.connect(self.gotocreate_login)
        self.signupbtn.clicked.connect(self.gotocreate)
        self.forgotpasswordbtn.clicked.connect(self.gotocreate_forgotpwd)
        self.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())

    def slideLeftMenu(self):
        width = self.slide_menu_container.width()
        newWidth = 350 if width == 0 else 0
        self.animation = QtCore.QPropertyAnimation(self.slide_menu_container, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.restore_window_button.setIcon(QtGui.QIcon("icons/maximize-2.svg"))
        else:
            self.showMaximized()
            self.restore_window_button.setIcon(QtGui.QIcon("icons/minimize-2.svg"))

    def gotocreate_login(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_forgotpwd(self):
        forgotpwd = Otp()
        widget.addWidget(forgotpwd)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate(self):
        signup = Signup()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.signup.clicked.connect(self.gotocreate)
        self.forgotpwdbutton.clicked.connect(self.gotocreate_otp)
        self.homebtn.clicked.connect(self.gotocreate_main)

    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        users = read_users()
        if username in users and users[username] == password:
            QMessageBox.information(self, "Login", "Successfully logged in!")
            self.gotocreate_user()
        else:
            QMessageBox.critical(self, "Login", "Invalid username or password.")

    def gotocreate(self):
        signup = Signup()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_otp(self):
        forgotpwdbutton = Otp()
        widget.addWidget(forgotpwdbutton)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_user(self):
        userwindow = UserWindow()
        widget.addWidget(userwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_main(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Signup(QDialog):
    def __init__(self):
        super(Signup, self).__init__()
        loadUi("signup.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.signupbutton.clicked.connect(self.signupfunction)
        self.login.clicked.connect(self.gotocreate_login)
        self.homebtn.clicked.connect(self.gotocreate_main)

    def signupfunction(self):
        email = self.email.text()
        mobileno = self.mobileno.text()
        username_3 = self.username_3.text()
        password = self.password.text()
        confirmpass = self.confirmpass.text()
        if password == confirmpass:
            users = read_users()
            if username_3 in users:
                QMessageBox.critical(self, "Signup", "Username already exists.")
            else:
                write_user(username_3, password)
                registration_details = f"{username_3},{email},{mobileno}"
                write_registration(registration_details)
                write_status(username_3, "Registered")
                QMessageBox.information(self, "Signup", "Account created successfully!")
        else:
            QMessageBox.critical(self, "Signup", "Passwords do not match.")

    def gotocreate_login(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_main(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Otp(QDialog):
    def __init__(self):
        super(Otp, self).__init__()
        loadUi("otp.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.sendotp.clicked.connect(self.sendfunction)
        self.verifyotp.clicked.connect(self.verifyfunction)
        self.cancelotp.clicked.connect(self.gotocreate_login)
        self.homebtn.clicked.connect(self.gotocreate_login)

    def sendfunction(self):
        QMessageBox.information(self, "OTP", "OTP sent successfully")

    def verifyfunction(self):
        QMessageBox.information(self, "OTP", "Success")

    def gotocreate_login(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_forgotpwd(self):
        forgotpwd = Forgotpassword()
        widget.addWidget(forgotpwd)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class UserWindow(QMainWindow):
    def __init__(self):
        super(UserWindow, self).__init__()
        loadUi("userwindowui.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("User Dashboard")
        QSizeGrip(self.size_grip)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.centralwidget.setGraphicsEffect(self.shadow)
        self.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        self.close_window_button.clicked.connect(lambda: self.close())
        self.restore_window_button.clicked.connect(lambda: self.restore_or_maximize_window())
        self.user_btn.clicked.connect(self.gotocreate_login)
        self.registerbtn.clicked.connect(self.gotocreate_register)
        self.paymentbtn.clicked.connect(self.gotocreate_payment)
        self.checkstatusbtn.clicked.connect(self.gotocreate_status)
        self.open_close_side_bar_btn.clicked.connect(lambda: self.slideLeftMenu())

    def slideLeftMenu(self):
        width = self.slide_menu_container.width()
        newWidth = 350 if width == 0 else 0
        self.animation = QtCore.QPropertyAnimation(self.slide_menu_container, b"maximumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.restore_window_button.setIcon(QtGui.QIcon("icons/maximize-2.svg"))
        else:
            self.showMaximized()
            self.restore_window_button.setIcon(QtGui.QIcon("icons/minimize-2.svg"))

    def gotocreate_login(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_register(self):
        register = Register()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_payment(self):
        payment = Payment()
        widget.addWidget(payment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_status(self):
        status = Status()
        widget.addWidget(status)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        loadUi("register.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.register_2.clicked.connect(self.registerfunction)
        self.cancelregi.clicked.connect(self.gotocreate_user)
        self.homebtn.clicked.connect(self.gotocreate_user)

    def registerfunction(self):
        fname = self.fname.text()
        lname = self.lname.text()
        username = self.username.text()
        dob = self.dob.text()
        gender = self.gender.text()
        mobileno = self.mobileno.text()
        email = self.email.text()
        nationality = self.nationality.text()
        martialstatus = self.martialstatus.text()
        aadhar = self.aadhar.text()
        pan = self.pan.text()
        driving = self.driving.text()
        _10mark = self._10mark.text()
        _12mark = self._12mark.text()
        if all([fname, lname, mobileno, username, email, nationality, martialstatus, aadhar, pan, driving, _10mark, _12mark]):
            registration_details = f"{fname},{lname},{username},{dob},{gender},{mobileno},{email},{nationality},{martialstatus},{aadhar},{pan},{driving},{_10mark},{_12mark}"
            write_registration(registration_details)
            write_status(username, "Registered")
            QMessageBox.information(self, "Register", "Registered successfully")
            self.gotocreate_payment()
        else:
            QMessageBox.critical(self, "Register", "Fields cannot be empty")

    def gotocreate_payment(self):
        payment = Payment()
        widget.addWidget(payment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_user(self):
        userwindow = UserWindow()   
        widget.addWidget(userwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Payment(QDialog):
    def __init__(self):
        super(Payment, self).__init__()
        loadUi("payment.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.card.clicked.connect(self.gotocreate_card)
        self.upi.clicked.connect(self.gotocreate_upi)
        self.homebtn.clicked.connect(self.gotocreate_user)

    def gotocreate_user(self):
        userwindow = UserWindow()
        widget.addWidget(userwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_card(self):
        cardpayment = CardPayment()
        widget.addWidget(cardpayment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocreate_upi(self):
        upipayment = UpiPayment()
        widget.addWidget(upipayment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CardPayment(QDialog):
    def __init__(self):
        super(CardPayment, self).__init__()
        loadUi("cardpayment.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.verifybtn.clicked.connect(self.gotocreate_payment)

    def gotocreate_payment(self):
        fname = self.fname.text()
        email = self.email.text()
        dob = self.dob.text()
        gender = self.gender.text()
        card_num = self.card_num.text()
        card_cvc = self.card_cvc.text()
        expdate = self.expdate.text()

        if all([fname, email, dob, gender, card_num, card_cvc, expdate]):
            payment_details = f"{fname},{email},{dob},{gender},{card_num},{card_cvc},{expdate}"
            write_payment(payment_details)
            QMessageBox.information(self, "Payment", "Payment Successful")
            self.gotocreate_user()
        else:
            QMessageBox.critical(self, "Payment", "Fields Cannot Be Empty")

    def gotocreate_user(self):
        userwindow = UserWindow()
        widget.addWidget(userwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class UpiPayment(QDialog):
    def __init__(self):
        super(UpiPayment, self).__init__()
        loadUi("upipayment.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.verifybtn.clicked.connect(self.gotocreate_payment)

    def gotocreate_payment(self):
        fname = self.fname.text()
        email = self.email.text()
        dob = self.dob.text()
        gender = self.gender.text()
        upi_id = self.upi_id.text()

        if all([fname, email, dob, gender, upi_id]):
            payment_details = f"{fname},{email},{dob},{gender},{upi_id}"
            write_payment(payment_details)
            QMessageBox.information(self, "Payment", "Payment Successful")
            self.gotocreate_user()
        else:
            QMessageBox.critical(self, "Payment", "Fields Cannot Be Empty")

    def gotocreate_user(self):
        userwindow = UserWindow()
        widget.addWidget(userwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Status(QDialog):
    def __init__(self):
        super(Status, self).__init__()
        loadUi("status.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.homebtn.clicked.connect(self.gotocreate_user)
        self.checkbtn.clicked.connect(self.statusfunction)

    def statusfunction(self):
        username = self.username.text()
        status = read_status()
        if username in status:
            self.status_label.setText(status[username])
        else:
            QMessageBox.critical(self, "Status", "Wrong username or email, please try again!")

    def gotocreate_user(self):
        userwindow = UserWindow()
        widget.addWidget(userwindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

def main():
    print("Initializing application...")
    app = QApplication(sys.argv)
    global widget
    widget = QtWidgets.QStackedWidget()
    mainwindow = MainWindow()
    widget.addWidget(mainwindow)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1000)
    widget.show()
    try:
        print("Starting application event loop...")
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()