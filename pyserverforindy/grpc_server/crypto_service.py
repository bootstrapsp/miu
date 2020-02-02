import json
import os
import sys

from indy import crypto as indy_crypto


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR+'/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))

from ..identityLayer import identitylayer_pb2
from ..identityLayer import identitylayer_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_value(value, value_type=None):
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
    if isinstance(value, str) and len(value)==0:
        return None
    elif isinstance(value, str):
        return value

    # numeric check
    if isinstance(value, int) and value==0:
        return None
    elif isinstance(value, int):
        return value



class CryptoServiceServicer(identitylayer_pb2_grpc.CryptoServiceServicer):
    """`crypto` Services
    """
    async def CreateKey(self, request, context):
        """Create Key
        """
        resp = None
        try:
            wallet_handle = get_value(request.WalletHandle)
            key_json = json.dumps({"seed": get_value(request.KeyJsonCreateKey.seed),
                "crypto_type": get_value(request.KeyJsonCreateKey.CryptoType)})
            resp = await indy_crypto.create_key(wallet_handle, key_json)
            return identitylayer_pb2.CreateKeyResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @CreateKey--------")
            logger.error(e)
            return identitylayer_pb2.CreateKeyResponse(resp)

    async def SetKeyMetadata(self, request, context):
        """Set Key Metadata
        """
        resp = None
        try:
            wallet_handle, verkey, metadata = get_value(request.WalletHandle), \
            get_value(request.Verkey), get_value(request.Metadata)
            resp = await indy_crypto.set_key_metadata(wallet_handle, verkey, metadata)
            return identitylayer_pb2.SetKeyMetadataResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @SetKeyMetadata--------")
            logger.error(e)
            return identitylayer_pb2.SetKeyMetadataResponse(resp)

    async def GetKeyMetadata(self, request, context):
        """Get Key Metadata
        """
        resp = None
        try:
            wallet_handle, verkey = get_value(request.WalletHandle), get_value(request.Verkey)
            resp = await indy_crypto.get_key_metadata(wallet_handle, verkey)
            return identitylayer_pb2.GetKeyMetadataResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @GetKeyMetadata--------")
            logger.error(e)
            return identitylayer_pb2.GetKeyMetadataResponse(resp)

    async def CryptoSign(self, request, context):
        """Crypto Sign
        """
        resp = None
        try:
            wallet_handle, signer_vk, msg = get_value(request.WalletHandle), get_value(request.SignerVk), get_value(request.Msg)
            resp = await indy_crypto.crypto_sign(wallet_handle, signer_vk, msg)
            return identitylayer_pb2.CryptoSignResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @CryptoSign--------")
            logger.error(e)
            return identitylayer_pb2.CryptoSignResponse(resp)

    async def CryptoVerify(self, request, context):
        """Crypto Verify
        """
        resp = None
        try:
            signer_vk, msg, signature = get_value(request.SignerVk), get_value(request.Msg), get_value(request.Signature)
            resp = await indy_crypto.crypto_verify(signer_vk, msg, signature)
            return identitylayer_pb2.CryptoVerifyResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @CryptoVerify--------")
            logger.error(e)
            return identitylayer_pb2.CryptoVerifyResponse(resp)

    async def AuthCrypt(self, request, context):
        """Auth Crypt
        """
        resp = None
        try:
            wallet_handle, sender_vk, recipient_vk, msg = get_value(request.WalletHandle), get_value(request.SenderVk), get_value(request.RecipientVk), get_value(request.Msg)
            resp = await indy_crypto.auth_crypt(wallet_handle, sender_vk, recipient_vk, msg)
            return identitylayer_pb2.AuthCryptResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @AuthCrypt--------")
            logger.error(e)
            return identitylayer_pb2.AuthCryptResponse(resp)

    async def AuthDecrypt(self, request, context):
        """Auth Decrypt
        """
        resp = None
        try:
            wallet_handle, recipient_vk, encrypted_msg = get_value(request.WalletHandle), get_value(request.RecipientVk), get_value(request.EncryptedMsg)
            resp = await indy_crypto.auth_decrypt(wallet_handle, recipient_vk, encrypted_msg)
            return identitylayer_pb2.AuthDecryptResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @AuthDecrypt--------")
            logger.error(e)
            return identitylayer_pb2.AuthDecryptResponse(Verkey=resp[0], Msg=resp[1])

    async def AnonCrypt(self, request, context):
        """Anon Crypt
        """
        resp = None
        try:
            recipient_vk, msg = get_value(request.RecipientVk), get_value(request.Msg)
            resp = await indy_crypto.anon_crypt(recipient_vk, msg)
            return identitylayer_pb2.AnonCryptResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @AnonCrypt--------")
            logger.error(e)
            return identitylayer_pb2.AnonCryptResponse(resp)

    async def AnonDecrypt(self, request, context):
        """Anon Decrypt
        """
        resp = None
        try:
            wallet_handle, recipient_vk, encrypted_msg = get_value(request.WalletHandle), get_value(request.RecipientVk), get_value(request.EncryptedMsg)
            resp = await indy_crypto.anon_decrypt(wallet_handle, recipient_vk, encrypted_msg)
            return identitylayer_pb2.AnonDecryptResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @AnonDecrypt--------")
            logger.error(e)
            return identitylayer_pb2.AnonDecryptResponse(resp)
