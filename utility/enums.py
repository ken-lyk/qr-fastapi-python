from enum import Enum

class UserRoleEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    
class QRSourceEnum(str, Enum):
    DIRECT_VALUE = "DIRECT_VALUE"
    IMAGE_DATA = "IMAGE_DATA"
    IMAGE_FILE = "IMAGE_FILE"