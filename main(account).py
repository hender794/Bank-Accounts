from account import *


def main():
    application = QApplication([])
    window = Account()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()