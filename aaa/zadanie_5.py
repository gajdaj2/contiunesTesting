# Zadanie 6: Test Skomplikowany - Sekwencja Operacji (⭐ Trudne)
# Napisz test dla całego scenariusza:
#
# Stwórz konto z 1000 PLN
# Wpłać 500 PLN
# Wypłać 200 PLN
# Sprawdź saldo (powinno być 1300)
# Sprawdź że mamy 3 transakcje (deposit + withdraw, plus initial)
from aaa.BankAccount import BankAccount


def test_full_banking_scenario():
    # Arrange
    account = BankAccount("PL61109010140000071219812874", 1000)

    # Act
    account.deposit(500)
    account.withdraw(200)
    final_balance = account.get_balance()
    history = account.get_transaction_history()

    # Assert
    assert final_balance == 1300
    assert len(history) == 3
    assert history[0]["balance_after"] == 1000  # initial
    assert history[1]["balance_after"] == 1500  # po wpłacie
    assert history[2]["balance_after"] == 1300  # po wypłacie

    # Assert
    history = account.get_transaction_history()
    assert len(history) == 3
    assert history[0]["type"] == "initial"
    assert history[1]["type"] == "deposit"
    assert history[2]["type"] == "withdraw"
    assert history[2]["balance_after"] == 700