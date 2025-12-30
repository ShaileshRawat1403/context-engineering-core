# example_code.py

class User:
    """
    Represents a user in the system.
    """
    def __init__(self, username: str, email: str):
        """
        Initializes a new User instance.

        Args:
            username: The user's chosen username.
            email: The user's email address.
        """
        self.username = username
        self.email = email
        self.is_active = True

    def deactivate(self):
        """
        Deactivates the user's account.
        """
        self.is_active = False
        print(f"User {self.username} has been deactivated.")

    def __repr__(self):
        return f"<User username='{self.username}' email='{self.email}'>"

def send_welcome_email(user: User):
    """
    Sends a welcome email to a new user.
    """
    if user.is_active:
        print(f"Sending welcome email to {user.email}.")
    else:
        print(f"Cannot send email to inactive user {user.username}.")

