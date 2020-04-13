import json
import os
import sys

import grpc
from indy import wallet as indy_wallet, IndyError
from indy.error import ErrorCode
from grpc import StatusCode
import hashlib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR + '/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))

from identityLayer import identitylayer_pb2
from identityLayer import identitylayer_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_value(value):
    """
    This function return the value of the specified key else `None`

    For `strings`, the default value is the empty string.
    For `bytes`, the default value is empty bytes.
    For `bools`, the default value is false.
    For `numeric` types, the default value is zero.
    For `enums`, the default value is the first defined enum value, which must be 0.
    For message fields, the field is not set. Its exact value is language-dependent. See the generated code guide for details.
    The default value for `repeated` fields is empty (generally an empty list in the appropriate language).
    """
    # print('\n\n----------')
    # print(value, value_type, type(value))

    # string check
    if isinstance(value, str) and len(value) == 0:
        return None
    elif isinstance(value, str):
        return value

    # numeric check
    if isinstance(value, int) and value == 0:
        return None
    elif isinstance(value, int):
        return value


class WalletServiceServicer(identitylayer_pb2_grpc.WalletServiceServicer):
    """ WalletServiceServicer
  """
    #dictionary for opened wallets - key : walletID ; value : WalletHandle;
    openedWallets = {}
    async def CreateNewWallet(self, request, context):
        resp = None
        try:
            storage_config_path = get_value(request.walletConfig.storePath.newWalletPath)
            wallet_config = json.dumps({"id": get_value(request.walletConfig.walletID),
                                        "storage_type": get_value(request.walletConfig.walletstorageType),
                                        "storage_config": {} if storage_config_path is None else {
                                            "path": storage_config_path}})
            # print(wallet_config)

            key_derivation_method = get_value(request.walletCredentials.newWalletKeyDerivationMethod)
            storage_credentials = get_value(request.walletCredentials.newWalletKeyDerivationMethod)

            wallet_credentials = json.dumps({"key": get_value(request.walletCredentials.newWalletKey),
                                             "storage_credentials": {} if storage_credentials is None else storage_credentials,
                                             "key_derivation_method": 'ARGON2I_MOD' if key_derivation_method is None else key_derivation_method})
            # print(wallet_credentials)

            resp = await indy_wallet.create_wallet(wallet_config, wallet_credentials)
            return identitylayer_pb2.CreateWalletErrorCode(NewWalletErrorCode=str(resp))
        except IndyError as e:
            logger.error("Indy Exception Occurred @ CreateNewWallet ------")
            logger.error(e.message)
            return identitylayer_pb2.CreateWalletErrorCode(NewWalletErrorCode=e.message)
        except Exception as e:
            logger.error("Exception Occurred @ CreateNewWallet------")
            logger.error(e)
            return identitylayer_pb2.CreateWalletErrorCode(NewWalletErrorCode=str(e))

    async def OpenWallet(self, request, context):
        resp = None
        openWalletKey = ""
        try:
            storage_config_path = get_value(request.Config.Path.path)
            config = json.dumps({"id": get_value(request.Config.Id),
                                 "storage_type": get_value(request.Config.StorageType),
                                 "storage_config": {} if storage_config_path is None else {
                                     "path": storage_config_path}})

            key_derivation_method = get_value(request.Credentials.KeyDerivationMethod)
            re_key_derivation_method = get_value(request.Credentials.ReKeyDerivationMethod)
            storage_credentials = get_value(request.Credentials.StorageCredentials)
            credentials = json.dumps({"key": request.Credentials.Key,
                                      "rekey": get_value(request.Credentials.ReKey),
                                      "storage_credentials": {} if storage_credentials is None else storage_credentials,
                                      "key_derivation_method": 'ARGON2I_MOD' if key_derivation_method is None else key_derivation_method,
                                      "rekey_derivation_method": 'ARGON2I_MOD' if re_key_derivation_method is None else re_key_derivation_method,
                                      })
            # hashing of cred key is done, because we need to control who can recieve a handler if wallet is opened
            openWalletKey = hashlib.sha256((request.Config.Id + request.Credentials.Key).encode('utf-8')).hexdigest() 
            resp = await indy_wallet.open_wallet(config, credentials)
            self.openedWallets[openWalletKey] = resp
            logger.info("wallet with id %s is added to memory, memoryKey: %s",request.Config.Id, openWalletKey) 
            return identitylayer_pb2.OpenWalletHandle(WalletHandle=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ OpenWallet ------")
            logger.error(e.message)
            if e.error_code == ErrorCode.WalletAlreadyOpenedError:
                if openWalletKey in self.openedWallets.keys():
                    return identitylayer_pb2.OpenWalletHandle(WalletHandle=self.openedWallets[openWalletKey], ErrorCode = ErrorCode.WalletAlreadyOpenedError)
                else:
                    logger.error("wallet with id %s has been opened before, but provided credentials are wrong",request.Config.Id) 
                    return identitylayer_pb2.OpenWalletHandle(WalletHandle=-1, ErrorCode = ErrorCode.WalletAccessFailed)
            return identitylayer_pb2.OpenWalletHandle(WalletHandle=-1 ,ErrorCode = e.error_code) 
        except Exception as e:
            logger.error("Exception Occurred @ OpenWallet------")
            logger.error(e)
            return identitylayer_pb2.OpenWalletHandle(WalletHandle= -1, ErrorCode = StatusCode.INTERNAL.value[0] ) 

    async def CloseWallet(self, request, context):
        resp = None
        try:
            resp = await indy_wallet.close_wallet(request.WalletHandle)
            for k, v in list(self.openedWallets.items()):
                if v == request.WalletHandle:
                    del self.openedWallets[k]   
                    logger.info("wallet with memoryKey %s is removed from memory",k)   
            return identitylayer_pb2.CloseWalletStatus(CloseWalletCode=str(resp))
        except IndyError as e:
            logger.error("Indy Exception Occurred @ CloseWallet ------")
            logger.error(e.message)
            return identitylayer_pb2.CloseWalletStatus(CloseWalletCode=e.message) 
        except Exception as e:
            logger.error("Exception Occurred @ CloseWallet------")
            logger.error(e)
            return identitylayer_pb2.CloseWalletStatus(CloseWalletCode=str(e))

    async def DeleteWallet(self, request, context):
        resp = None
        try:
            storage_config_path = get_value(request.Config.StorageConfig.Path)
            config = json.dumps({"id": get_value(request.Config.DeleteWalletID),
                                 "storage_type": get_value(request.Config.DeleteWalletStorageType),
                                 "storage_config": {} if storage_config_path is None else {
                                     "path": storage_config_path}})

            key_derivation_method = get_value(request.Credentials.DeleteWalletKeyDerivationMethod)
            storage_credentials = get_value(request.Credentials.DeleteWalletStorageCredentials)
            credentials = json.dumps({"key": request.Credentials.DeleteWalletKey,
                                      "storage_credentials": {} if storage_credentials is None else storage_credentials,
                                      "key_derivation_method": 'ARGON2I_MOD' if key_derivation_method is None else key_derivation_method,
                                      })
            resp = await indy_wallet.delete_wallet(config=config, credentials=credentials)
            return identitylayer_pb2.DeleteWalletConfirmation(DeleteWalletStatus=1)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ DeleteWallet ------")
            logger.error(e.message)
            return identitylayer_pb2.DeleteWalletConfirmation(DeleteWalletStatus=0) 
        except Exception as e:
            logger.error("Exception Occurred @ DeleteWallet------")
            logger.error(e)
            return identitylayer_pb2.DeleteWalletConfirmation(DeleteWalletStatus=0)

    async def ExportWallet(self, request, context):
        resp = None
        try:
            wallet_handle = get_value(request.ExportWalletHandle)
            key_derivation_method = get_value(request.ExportConfigJson.ExportWalletKeyDerivationMethod)
            export_config_json = json.dumps({"path": get_value(request.ExportConfigJson.ExportWalletPath),
                                             "key": get_value(request.ExportConfigJson.ExportWalletKey),
                                             "key_derivation_method": 'ARGON2I_MOD' if key_derivation_method is None else key_derivation_method})
            resp = await indy_wallet.export_wallet(wallet_handle, export_config_json)
            return identitylayer_pb2.ExportWalletConfirmation(ExportWalletStatus=1)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ExportWallet ------")
            logger.error(e.message)
            return identitylayer_pb2.ExportWalletConfirmation(ExportWalletStatus=0) 
        except Exception as e:
            logger.error("Exception Occurred @ ExportWallet------")
            logger.error(e)
            return identitylayer_pb2.ExportWalletConfirmation(ExportWalletStatus=0)

    async def ImportWallet(self, request, context):
        resp = None
        try:
            storage_config_path = get_value(request.Config.StorageConfig.Path)
            config = json.dumps({"id": get_value(request.Config.Id),
                                 "storage_type": get_value(request.Config.StorageType),
                                 "storage_config": {} if storage_config_path is None else {
                                     "path": storage_config_path}})

            key_derivation_method = get_value(request.Credentials.KeyDerivationMethod)
            storage_credentials = get_value(request.Credentials.StorageCredentials)
            credentials = json.dumps({"key": request.Credentials.Key,
                                      "storage_credentials": {} if storage_credentials is None else storage_credentials,
                                      "key_derivation_method": 'ARGON2I_MOD' if key_derivation_method is None else key_derivation_method,
                                      })

            import_config_json = json.dumps({"path": request.ConfigJson.Path, "key": request.ConfigJson.Key})
            resp = await indy_wallet.import_wallet(config, credentials, import_config_json)
            return identitylayer_pb2.ImportWalletConfirmation(ImportWalletStatusCode=str(resp))
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ImportWallet ------")
            logger.error(e.message)
            return identitylayer_pb2.ImportWalletConfirmation(ImportWalletStatusCode=e.message) 
        except Exception as e:
            logger.error("Exception Occurred @ ImportWallet------")
            logger.error(e)
            return identitylayer_pb2.ImportWalletConfirmation(ImportWalletStatusCode=str(e))

    async def GenerateWalletKey(self, request, context):
        resp = None
        try:
            config = json.dumps({"seed": None})

            resp = await indy_wallet.generate_wallet_key(config=config)
            return identitylayer_pb2.GenerateWalletKeyConfirmation(GenerateWalletKeyStatus=str(resp))
        except IndyError as e:
            logger.error("Indy Exception Occurred @ GenerateWalletKey ------")
            logger.error(e.message)
            return identitylayer_pb2.GenerateWalletKeyConfirmation(GenerateWalletKeyStatus=e.message) 
        except Exception as e:
            logger.error("Exception Occurred @ GenerateWalletKey------")
            logger.error(e)
            return identitylayer_pb2.GenerateWalletKeyConfirmation(GenerateWalletKeyStatus=str(e))
