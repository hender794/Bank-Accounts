from new_account import *
from PyQt6.QtWidgets import *
import csv


class Account(QMainWindow, Ui_MainWindow):
    """
    Class representing savings and checking accounts
    """
    def __init__(self, savings=10000, checking=1000) -> None:
        """
        Method of initializing buttons and values
        :param savings: total amount in savings account
        :param checking: total amount in checking account
        """
        super().__init__()
        self.setupUi(self)
        self.button_savings.setChecked(True)
        self.button_withdraw.setChecked(True)
        self.savings_balance = savings
        self.checking_balance = checking
        self.label_message.setText('Please click clear after each submission to reset values')
        self.button_submit.clicked.connect(lambda: self.submit())
        self.button_clear.clicked.connect(lambda: self.clear())

    def submit(self) -> None:
        """
        Method to try as long as there is no value error for input of the amount and name
        """
        try:
            name = self.input_name.text()
            amount = float(self.input_amount.text())
            self.label_message.setText('')
            with open('details.csv', 'r') as csv_file:
                for line in csv_file:
                    line = line.split(',')
                    if line[0] == name and line[1] == self.check_account():
                        if self.button_savings.isChecked():
                            self.savings_balance = float(line[2])
                        else:
                            self.checking_balance = float(line[2])
            self.finish(name, amount)
        except ValueError:
            self.label_details.setText('')
            self.label_user_name.setText('')
            self.label_used.setText('')
            self.label_sum.setText('')
            self.label_detailed_name.setText('')
            self.label_detailed_amount.setText('')
            self.label_total.setText('')
            error = 'Amount of money needs to be a positive number like 81.52 not $81.52'
            self.label_message.setText(error)

    def finish(self, name, amount) -> None:
        """
        Method to finish displaying the account name and totals
        :param name: account name
        :param amount: amount inputted
        """
        self.label_detailed_name.setText('Account name')
        self.label_total.setText(f"{name}'s {self.check_account()} total")
        self.label_used.setText(f'{amount:.2f}')
        self.label_user_name.setText(name)
        self.label_sum.setText(f'{self.check_action(amount, name)}')
        if self.button_savings.isChecked():
            button = 'savings'
        elif self.button_checking.isChecked():
            button = 'checking'
        with open('details.csv', 'a', newline='') as csv_file:
            info = csv.writer(csv_file, delimiter=',')
            header2 = [f'{self.input_name.text()}', f'{button}', f'{self.label_sum.text()}']
            info.writerow(header2)
            # Need help getting the csv file to write in a new line when submit has been clicked

    def check_action(self, amount, name) -> str:
        """
        Method to check if there is enough money in account to withdraw and to check if using savings or checking account
        :param amount: amount inputted
        :param name: account name
        :return: either a blank string or the total balance of the account
        """
        if self.check_account() == 'savings':
            if self.button_withdraw.isChecked():
                if self.savings_balance <= 0 or amount > self.savings_balance:
                    self.label_message.setText(f'There is not enough money in {name} to withdraw')
                    self.label_user_name.setText('')
                    self.label_used.setText('')
                    self.label_sum.setText('')
                    self.label_detailed_name.setText('')
                    self.label_detailed_amount.setText('')
                    self.label_total.setText('')
                    return ''
                else:
                    self.label_message.setText('')
                    self.savings_balance = self.savings_balance - amount
                    self.label_detailed_amount.setText('Money withdrawn')
                    return self.savings_balance
            elif self.button_deposit.isChecked():
                self.label_message.setText('')
                self.savings_balance = self.savings_balance + amount
                self.label_detailed_amount.setText('Money deposited')
                return self.savings_balance

        else:
            if self.button_withdraw.isChecked():
                if self.checking_balance <= 0 or amount > self.checking_balance:
                    self.label_message.setText(f'There is not enough money in {name} to withdraw')
                    self.label_user_name.setText('')
                    self.label_used.setText('')
                    self.label_sum.setText('')
                    self.label_detailed_name.setText('')
                    self.label_detailed_amount.setText('')
                    self.label_total.setText('')
                    return ''
                else:
                    self.label_message.setText('')
                    self.checking_balance = self.checking_balance - amount
                    self.label_detailed_amount.setText('Money withdrawn')
                    return self.checking_balance
            else:
                self.label_message.setText('')
                self.checking_balance = self.checking_balance + amount
                self.label_detailed_amount.setText('Money deposited')
                return self.checking_balance

    def check_account(self) -> str:
        """
        Method to check and display the title for the details of the account
        :return: a string help to decide whether to use savings or checking
        """
        if self.button_savings.isChecked():
            self.label_details.setText('Savings Account Details')
            return 'savings'
        else:
            self.label_details.setText('Checking Account Details')
            return 'checking'

    def clear(self) -> None:
        """
        Method to clear all values on the display
        """
        self.label_details.setText('')
        self.label_message.setText('')
        self.input_amount.setText('')
        self.input_name.setText('')
        self.label_user_name.setText('')
        self.label_used.setText('')
        self.label_detailed_name.setText('')
        self.label_detailed_amount.setText('')
        self.button_savings.setChecked(True)
        self.button_withdraw.setChecked(True)
        self.savings_balance = 10000
        self.checking_balance = 1000
