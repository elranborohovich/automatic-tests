from bank_account import BankAccount

def test_deposit():
    """
    Test case for the deposit function.
    Creates an account for Alice with 100, deposits 50,
    and asserts that the new balance is exactly 150.
    """
    account = BankAccount("Alice", 100)
    account.deposit(50)
    assert account.balance == 150

def test_withdraw():
    """
    Test case for the withdraw function.
    Creates an account with a balance of 100, withdraws 20,
    and asserts that the remaining balance is exactly 80.
    """
    account = BankAccount("Bob", 100)
    account.withdraw(20)
    assert account.balance == 80

def test_static_function():
    """
    Test case for the static function (is_valid_amount).
    Calls the static function directly from the class using a negative number (-10),
    and asserts that the returned result is False.
    """
    result = BankAccount.is_valid_amount(-10)
    assert result == False