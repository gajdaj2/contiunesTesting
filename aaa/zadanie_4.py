# Zadanie 4: Test Historii Transakcji (⭐ Średnie)
# Napisz test który:
#
# Arrange: Stwórz konto z saldem 500
# Act: Wpłacisz 300, następnie wypłacisz 100
# Assert: Sprawdzisz że historii są 3 transakcje (initial, deposit, withdraw)
from aaa.BankAccount import BankAccount


def test_withdraw_success():
    # Arrange
    account = BankAccount("PL61...", 1000)
    withdraw_amount = 300

    # Act
    result = account.withdraw(withdraw_amount)

    # Assert
    assert account.balance == 700
    assert result["type"] == "withdraw"
    assert result["amount"] == withdraw_amount