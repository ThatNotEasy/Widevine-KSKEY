
import os

class Device:
    def __init__(self, name):
        path = f"{name}"
        full_path = os.path.abspath(path)
        # print("Constructed full path:", full_path)
        if not os.path.exists(full_path):
            raise Exception("Device not found")
        self.name = name
        self.blob = f"{full_path}/device_client_id_blob"
        self.private_key = f"{full_path}/device_private_key"

class CDMSession:
    def __init__(
        self,
        session_id,
        init_data,
        device,
        offline
    ):
        self.session_id = session_id
        self.init_data = init_data
        self.offline = offline
        self.device: Device = device
        self.device_key = None
        self.session_key = None
        self.derived_keys = {
            "enc": None, 
            "auth_1": None, 
            "auth_2": None
        }
        self.license_request = None
        self.license = None
        self.service_certificate = None
        self.privacy_mode = False
        self.keys = []

class EncryptionKey:
    def __init__(self, kid, type, key, permissions=[]):
        self.kid = kid
        self.type = type
        self.key = key
        self.permissions = permissions