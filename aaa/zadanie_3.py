#Zadanie 3: Test Wypłaty
#Zadanie: Napisz test dla sytuacji gdy próbujemy wypłacić więcej niż mamy na koncie.
import pytest

from aaa.BankAccount import BankAccount


def test_deposit_negative_amount():
    # Arrange
    account = BankAccount("PL61...", 1000)

    # Act & Assert
    with pytest.raises(ValueError):
        account.deposit(-100)