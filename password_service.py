from typing import List, Tuple, Optional
from cryptography.fernet import Fernet
from account_data_base import Account_db
import security


class PasswordManager:
    def __init__(self, db_path: str) -> None:
        self.db = Account_db(db_path)
        self.fernet: Optional[Fernet] = None

    def initialize(self, master_password: str, salt: bytes) -> None:
        self.fernet = security.get_fernet_key(master_password, salt)

    def add_password(self, service: str, password: str) -> None:
        if not self.fernet:
            raise RuntimeError('Fernet not initialized')

        enc_pswd = security.encrypt_password(password, self.fernet)
        self.db.new_account(service, enc_pswd)

    def delete_password(self, service: str) -> bool:
        if not self.fernet:
            raise RuntimeError('Fernet not initialized')
        self.db.delete_account(service)
        return True

    def update_password(self, service: str, password: str) -> bool:
        if not self.db.check_account(service):
            return False

        if not self.fernet:
            raise RuntimeError('Fernet not initialized')

        enc_pswd = security.encrypt_password(password, self.fernet)
        self.db.redact_account(service, enc_pswd)
        return True

    def get_all_passwords(self) -> List[Tuple[str, str]]:
        if not self.fernet:
            raise RuntimeError('Fernet not initialized')

        enc_rows = self.db.get_data()
        dcr_data = []
        for name, enc_pswd in enc_rows:
            plain_pswd = security.decrypt_password(enc_pswd, self.fernet)
            dcr_data.append((name, plain_pswd))
        return dcr_data

    def change_master_password(self, new_mp: str, new_salt: bytes) -> bool:
        if not self.fernet:
            raise RuntimeError('Fernet not initialized')

        all_records = self.get_all_passwords()

        self.fernet = security.get_fernet_key(new_mp, new_salt)

        for name, plain_pswd in all_records:
            enc_pswd = security.encrypt_password(plain_pswd, self.fernet)
            self.db.redact_account(name, enc_pswd)

        return True