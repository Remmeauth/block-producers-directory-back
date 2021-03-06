"""
Provide implementation of user domain.
"""
import uuid

from user.domain.errors import (
    RecoveryPasswordHasBeenAlreadySentError,
    SpecifiedUserPasswordIsIncorrectError,
    UserWithSpecifiedEmailAddressAlreadyExistsError,
    UserWithSpecifiedEmailAddressDoesNotExistError,
    UserWithSpecifiedIdentifierAlreadyConfirmedError,
    UserWithSpecifiedIdentifierDoesNotExistError,
    UserWithSpecifiedUsernameAlreadyExistsError,
    UserWithSpecifiedUsernameDoesNotExistError,
)


class RegisterUser:
    """
    User registration implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def by_credentials(self, email, username, password):
        """
        Create a user with specified e-mail address and password.
        """
        if self.user.does_exist_by_email(email=email):
            raise UserWithSpecifiedEmailAddressAlreadyExistsError

        if self.user.does_exist_by_username(username=username):
            raise UserWithSpecifiedUsernameAlreadyExistsError

        self.user.create_with_email(email=email, username=username, password=password)


class ChangeUserPassword:
    """
    Change user password implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def do(self, email, old_password, new_password):
        """
        Change user password.
        """
        if not self.user.does_exist_by_email(email=email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        is_password_matched = self.user.verify_password(email=email, password=old_password)

        if not is_password_matched:
            raise SpecifiedUserPasswordIsIncorrectError

        self.user.set_new_password(email=email, password=new_password)


class ChangeUserEmail:
    """
    Change user e-mail implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def do(self, username, new_email):
        """
        Change user e-mail.
        """
        if not self.user.does_exist_by_username(username=username):
            raise UserWithSpecifiedUsernameDoesNotExistError

        self.user.set_new_email(username=username, email=new_email)


class RequestUserPasswordRecovery:
    """
    Request to recovery user password implementation.
    """

    def __init__(self, user, password_recovery_state):
        """
        Constructor.
        """
        self.user = user
        self.password_recovery_state = password_recovery_state

    def do(self, email):
        """
        Request to recover user password by email.
        """
        if not self.user.does_exist_by_email(email=email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        identifier = uuid.uuid4().hex

        self.password_recovery_state.create(email=email, identifier=identifier)

        return identifier


class RecoverUserPassword:
    """
    Recover user password implementation.
    """

    def __init__(self, user, password_recovery_state):
        """
        Constructor.
        """
        self.user = user
        self.password_recovery_state = password_recovery_state

    def do(self, user_identifier):
        """
        Recover user password by user identifier.
        """
        if not self.password_recovery_state.does_exist(user_identifier=user_identifier):
            raise UserWithSpecifiedIdentifierDoesNotExistError

        if not self.password_recovery_state.is_active_(user_identifier=user_identifier):
            raise RecoveryPasswordHasBeenAlreadySentError

        self.password_recovery_state.deactivate(user_identifier=user_identifier)

        email = self.password_recovery_state.get_email(user_identifier=user_identifier)

        new_password = uuid.uuid4().hex[:12]

        self.user.set_new_password(email=email, password=new_password)
        return email, new_password


class UpdateUserProfile:
    """
    Update user profile implementation.
    """

    def __init__(self, user, profile):
        """
        Constructor.
        """
        self.user = user
        self.profile = profile

    def do(self, username, info):
        """
        Update user profile.
        """
        if not self.user.does_exist_by_username(username=username):
            raise UserWithSpecifiedUsernameDoesNotExistError

        self.profile.update(username=username, info=info)


class GetUser:
    """
    Get user implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def do(self, username):
        """
        Get user information by username.
        """
        if not self.user.does_exist_by_username(username=username):
            raise UserWithSpecifiedUsernameDoesNotExistError

        return self.user.get(username=username)


class GetUserProfile:
    """
    Get user profile implementation.
    """

    def __init__(self, user, profile):
        """
        Constructor.
        """
        self.user = user
        self.profile = profile

    def do(self, username):
        """
        Get user profile information by username.
        """
        if not self.user.does_exist_by_username(username=username):
            raise UserWithSpecifiedUsernameDoesNotExistError

        return self.profile.get(username=username)


class DeleteUser:
    """
    Delete user implementation.
    """

    def __init__(self, user):
        """
        Constructor.
        """
        self.user = user

    def do(self, username):
        """
        Delete user by username.
        """
        if not self.user.does_exist_by_username(username=username):
            raise UserWithSpecifiedUsernameDoesNotExistError

        return self.user.delete_(username=username)


class UserRequestEmailConfirm:
    """
    Request email confirm at the specified email address implementation.
    """

    def __init__(self, user, email_confirm_state):
        """
        Constructor.
        """
        self.user = user
        self.email_confirm_state = email_confirm_state

    def do(self, email):
        """
        Request email confirm at the specified email address.
        """
        if not self.user.does_exist_by_email(email=email):
            raise UserWithSpecifiedEmailAddressDoesNotExistError

        identifier = uuid.uuid4().hex

        self.email_confirm_state.create(email=email, identifier=identifier)

        return identifier


class UserEmailConfirm:
    """
    Confirm registration by user identifier implementation.
    """

    def __init__(self, user, email_confirm_state):
        """
        Constructor.
        """
        self.user = user
        self.email_confirm_state = email_confirm_state

    def do(self, user_identifier):
        """
        Confirm registration by user identifier.
        """
        if not self.email_confirm_state.does_exist(user_identifier=user_identifier):
            raise UserWithSpecifiedIdentifierDoesNotExistError

        if self.user.is_email_confirmed_(user_identifier=user_identifier):
            raise UserWithSpecifiedIdentifierAlreadyConfirmedError

        self.user.set_email_as_confirmed(user_identifier=user_identifier)
