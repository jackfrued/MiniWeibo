import random
from hashlib import sha256


def gen_password(user_password):
    '''产生一个安全的密码'''
    bin_password = user_password.encode('utf8')  # 将密码转成 bytes 类型
    hash_value = sha256(bin_password).hexdigest()  # 计算用户密码的哈希值
    salt = '%x' % random.randint(0x10000000, 0xffffffff)  # 产生随机盐
    safe_password = salt + hash_value
    return safe_password


def check_password(user_password, safe_password):
    '''检查用户密码是否正确'''
    bin_password = user_password.encode('utf8')  # 将密码转成 bytes 类型
    hash_value = sha256(bin_password).hexdigest()  # 计算用户密码的哈希值

    return hash_value == safe_password[8:]
