#Zadanie 1: Test Tworzenia Konta
#Napisz test dla funkcji __init__ korzystając ze struktury AAA

import pytest

from aaa.BankAccount import BankAccount


def test_create_account_with_initial_balance():
    # Arrange - przygotuj dane
    account_number = "PL61109010140000071219812874"
    initial_balance = 1000

    # Act - stwórz konto
    account = BankAccount(account_number, initial_balance)

    # Assert - sprawdź wyniki
    assert account.account_number == account_number
    assert account.balance == initial_balance
    assert len(account.transaction_history) == 1