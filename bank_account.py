class InsufficientFundsError(Exception):
    """Недостаточно средств на счёте."""


class BankAccount:
    def __init__(self, owner, account_number):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта должен быть непустой строкой")
        self._owner = owner.strip()
        self._account_number = account_number.strip()
        self._balance = 0  # начальный баланс всегда 0

    @property
    def owner(self):
        return self._owner

    @property
    def account_number(self):
        return self._account_number

    @staticmethod
    def _check_amount(amount):
        """Сумма должна быть числом (не bool) и строго больше нуля."""
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount != amount or amount in (float("inf"), float("-inf")):
            raise ValueError("Сумма должна быть конечным числом")
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")

    def deposit(self, amount):
        """Пополнение счёта."""
        self._check_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        """Снятие средств."""
        self._check_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств на счёте")
        self._balance -= amount

    def transfer(self, other, amount):
        """Перевод на другой счёт. При ошибке состояние обоих счетов не меняется."""
        if not isinstance(other, BankAccount):
            raise TypeError("Получатель должен быть объектом BankAccount")
        if other is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт")
        # все проверки выполняются ДО изменения балансов
        self._check_amount(amount)
        if amount > self._balance:
            raise InsufficientFundsError("Недостаточно средств на счёте")
        self._balance -= amount
        other._balance += amount

    def get_balance(self):
        """Текущий баланс."""
        return self._balance

    def is_empty(self):
        """True, если баланс равен нулю."""
        return self._balance == 0

    def __repr__(self):
        return (f"BankAccount(owner={self._owner!r}, "
                f"number={self._account_number!r}, balance={self._balance})")