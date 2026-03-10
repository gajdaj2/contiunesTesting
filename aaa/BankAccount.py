class BankAccount:
    """Konto bankowe z operacjami wpłaty, wypłaty i sprawdzenia salda."""

    def __init__(self, account_number, initial_balance=0):
        """
        Inicjalizuj konto bankowe.

        Args:
            account_number (str): Numer konta (np. "PL61...")
            initial_balance (float): Początkowe saldo (domyślnie 0)

        Raises:
            ValueError: Jeśli balance < 0
        """
        if initial_balance < 0:
            raise ValueError("Saldo nie może być ujemne")

        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = []

        if initial_balance > 0:
            self.transaction_history.append({
                "type": "initial",
                "amount": initial_balance,
                "balance_after": self.balance
            })

    def deposit(self, amount):
        """
        Wpłać pieniądze na konto.

        Args:
            amount (float): Kwota do wpłaty

        Returns:
            dict: Informacja o transakcji

        Raises:
            ValueError: Jeśli amount <= 0
        """
        if amount <= 0:
            raise ValueError("Kwota wpłaty musi być dodatnia")

        self.balance += amount
        transaction = {
            "type": "deposit",
            "amount": amount,
            "balance_after": self.balance
        }
        self.transaction_history.append(transaction)
        return transaction

    def withdraw(self, amount):
        """
        Wypłać pieniądze z konta.

        Args:
            amount (float): Kwota do wypłaty

        Returns:
            dict: Informacja o transakcji

        Raises:
            ValueError: Jeśli amount <= 0 lub Insufficient funds
        """
        if amount <= 0:
            raise ValueError("Kwota wypłaty musi być dodatnia")

        if amount > self.balance:
            raise ValueError("Niewystarczające środki na koncie")

        self.balance -= amount
        transaction = {
            "type": "withdraw",
            "amount": amount,
            "balance_after": self.balance
        }
        self.transaction_history.append(transaction)
        return transaction

    def get_balance(self):
        """Zwróć aktualne saldo."""
        return self.balance

    def get_transaction_history(self):
        """Zwróć historię transakcji."""
        return self.transaction_history.copy()