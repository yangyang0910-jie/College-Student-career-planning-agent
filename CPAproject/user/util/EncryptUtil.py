from passlib.context import CryptContext
crypt = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)
#使用hash加密密码
def hash_password(password:str) -> str:
    return crypt.hash(str(password))

#验证密码
def verify_password(password:str, hashed_password:str) -> bool:
    return crypt.verify(str(password), hashed_password)