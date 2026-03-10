#Zadanie 2: Test Wpłaty
#Zadanie: Napisz test dla wpłaty ujemnej kwoty - powinien rzucić ValueError.
from aaa.BankAccount import BankAccount


def test_deposit_increases_balance():
    # Arrange
    account = BankAccount("PL61...", 1000)
    deposit_amount = 500

    # Act
    result = account.deposit(deposit_amount)

    # Assert
    assert account.balance == 1500
    assert result["type"] == "deposit"
    assert result["amount"] == deposit_amount