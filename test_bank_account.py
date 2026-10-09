import unittest

from bank_account import BankAccount, InsufficientFundsError


class TestCreation(unittest.TestCase):
    def test_owner_and_number_are_stored(self):
        acc = BankAccount("Айдана", "KG001")
        self.assertEqual(acc.owner, "Айдана")
        self.assertEqual(acc.account_number, "KG001")

    def test_initial_balance_is_zero(self):
        self.assertEqual(BankAccount("Айдана", "KG001").get_balance(), 0)

    def test_empty_owner_raises(self):
        for bad in ("", "   ", None, 123):
            with self.subTest(owner=bad):
                with self.assertRaises(ValueError):
                    BankAccount(bad, "KG001")

    def test_empty_number_raises(self):
        for bad in ("", "   ", None, 123):
            with self.subTest(number=bad):
                with self.assertRaises(ValueError):
                    BankAccount("Айдана", bad)


class TestDeposit(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Айдана", "KG001")

    def test_deposit_increases_balance(self):
        self.acc.deposit(100)
        self.assertEqual(self.acc.get_balance(), 100)

    def test_multiple_deposits(self):
        self.acc.deposit(100)
        self.acc.deposit(50.5)
        self.assertEqual(self.acc.get_balance(), 150.5)

    def test_deposit_zero_or_negative_raises(self):
        for bad in (0, -1, -100.5):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.acc.deposit(bad)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_deposit_invalid_type_raises(self):
        for bad in ("100", None, [1], True):
            with self.subTest(amount=bad):
                with self.assertRaises(TypeError):
                    self.acc.deposit(bad)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_deposit_nan_inf_raises(self):
        for bad in (float("nan"), float("inf")):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.acc.deposit(bad)


class TestWithdraw(unittest.TestCase):
    def setUp(self):
        self.acc = BankAccount("Айдана", "KG001")
        self.acc.deposit(200)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(50)
        self.assertEqual(self.acc.get_balance(), 150)

    def test_withdraw_entire_balance(self):
        self.acc.withdraw(200)
        self.assertEqual(self.acc.get_balance(), 0)

    def test_withdraw_more_than_balance_raises(self):
        with self.assertRaises(InsufficientFundsError):
            self.acc.withdraw(200.01)
        self.assertEqual(self.acc.get_balance(), 200)

    def test_withdraw_zero_or_negative_raises(self):
        for bad in (0, -10):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.acc.withdraw(bad)
        self.assertEqual(self.acc.get_balance(), 200)

    def test_withdraw_invalid_type_raises(self):
        with self.assertRaises(TypeError):
            self.acc.withdraw("50")
        self.assertEqual(self.acc.get_balance(), 200)


class TestTransfer(unittest.TestCase):
    def setUp(self):
        self.a = BankAccount("Айдана", "KG001")
        self.b = BankAccount("Дика", "KG002")
        self.a.deposit(500)
        self.b.deposit(100)

    def test_successful_transfer(self):
        self.a.transfer(self.b, 200)
        self.assertEqual(self.a.get_balance(), 300)
        self.assertEqual(self.b.get_balance(), 300)

    def test_transfer_changes_are_equal(self):
        total_before = self.a.get_balance() + self.b.get_balance()
        a_before, b_before = self.a.get_balance(), self.b.get_balance()
        self.a.transfer(self.b, 123)
        self.assertEqual(a_before - self.a.get_balance(),
                         self.b.get_balance() - b_before)
        self.assertEqual(total_before,
                         self.a.get_balance() + self.b.get_balance())

    def test_transfer_insufficient_funds_keeps_state(self):
        with self.assertRaises(InsufficientFundsError):
            self.a.transfer(self.b, 1000)
        self.assertEqual(self.a.get_balance(), 500)
        self.assertEqual(self.b.get_balance(), 100)

    def test_transfer_invalid_amount_keeps_state(self):
        for bad in (0, -50):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    self.a.transfer(self.b, bad)
        with self.assertRaises(TypeError):
            self.a.transfer(self.b, "50")
        self.assertEqual(self.a.get_balance(), 500)
        self.assertEqual(self.b.get_balance(), 100)

    def test_transfer_to_non_account_raises(self):
        with self.assertRaises(TypeError):
            self.a.transfer("KG002", 10)
        self.assertEqual(self.a.get_balance(), 500)

    def test_transfer_to_self_raises(self):
        with self.assertRaises(ValueError):
            self.a.transfer(self.a, 10)
        self.assertEqual(self.a.get_balance(), 500)


class TestBalanceAndEmpty(unittest.TestCase):
    def test_balance_after_operations(self):
        acc = BankAccount("Айдана", "KG001")
        other = BankAccount("Дика", "KG002")
        acc.deposit(1000)
        acc.withdraw(250)
        acc.transfer(other, 300)
        self.assertEqual(acc.get_balance(), 450)
        self.assertEqual(other.get_balance(), 300)

    def test_new_account_is_empty(self):
        self.assertTrue(BankAccount("Айдана", "KG001").is_empty())

    def test_account_with_money_is_not_empty(self):
        acc = BankAccount("Айдана", "KG001")
        acc.deposit(1)
        self.assertFalse(acc.is_empty())

    def test_account_becomes_empty_after_full_withdraw(self):
        acc = BankAccount("Айдана", "KG001")
        acc.deposit(100)
        acc.withdraw(100)
        self.assertTrue(acc.is_empty())

    def test_sender_empty_after_full_transfer(self):
        a = BankAccount("Айдана", "KG001")
        b = BankAccount("Дика", "KG002")
        a.deposit(100)
        a.transfer(b, 100)
        self.assertTrue(a.is_empty())
        self.assertFalse(b.is_empty())


if __name__ == "__main__":
    unittest.main()