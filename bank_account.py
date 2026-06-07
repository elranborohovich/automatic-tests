class BankAccount:

    def __init__(self, owner_name: str, balance: int):
        """
        The constructor for BankAccount class. Runs automatically when a new account is created.
        
        :param owner_name: The name of the account owner (str)
        :param balance: The initial balance of the account (int)
        """
        self.owner_name = owner_name
        self.balance = balance

    def deposit(self, amount: int):
        """
        A dynamic instance function that deposits money into the account, increasing the balance.
        
        :param amount: The amount of money to deposit (int)
        """
        self.balance += amount

    def withdraw(self, amount: int):
        """
        A dynamic instance function that withdraws money from the account, decreasing the balance.
        
        :param amount: The amount of money to withdraw (int)
        """
        self.balance -= amount

    @staticmethod
    def is_valid_amount(amount: int):
        """
        A static function that checks if a given amount is valid (greater than zero).
        
        :param amount: The amount to validate (int)
        :return: True if the amount is greater than 0, False otherwise
        """
        if amount > 0:
            return True
        else:
            return False