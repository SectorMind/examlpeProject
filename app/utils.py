# app/utils.py

from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    default="bcrypt",
    bcrypt__rounds=12,  # Setting bcrypt rounds to 12 for added security
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == '__main__':
    print(get_password_hash("1234"))
    # print(verify_password("1234", "$2b$12$dipLH3LYmq2e7/FqPsjazu2eiNZJesydIa603EdXmyjYL/wgRXtHi"))
