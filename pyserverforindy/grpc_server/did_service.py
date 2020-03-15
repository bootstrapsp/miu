import os
import json
import sys
from indy import did as indy_did, IndyError
from indy.error import ErrorCode
from grpc import StatusCode


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR+'/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))

from identityLayer import identitylayer_pb2
from identityLayer import identitylayer_pb2_grpc

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


class DidServiceServicer(identitylayer_pb2_grpc.DidServiceServicer):
    """
    DID Service
    """

    async def CreateAndStoreMyDid(self, request, context):
        """Create And Store My Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did_json = json.dumps({"did": get_value(request.DidJson.Did),
                "seed": get_value(request.DidJson.Seed),
                "crypto_type": get_value(request.DidJson.CryptoType),
                "cid": get_value(request.DidJson.Cid)})
            resp = await indy_did.create_and_store_my_did(wallet_handle, did_json)
            return identitylayer_pb2.CreateAndStoreMyDidResponse(Did=resp[0], Verkey=resp[1])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ CreateAndStoreMyDid ------")
            logger.error(e.message)
            return identitylayer_pb2.CreateAndStoreMyDidResponse() 
        except Exception as e:
            logger.error("Exception occurred @ CreateAndStoreMyDid----")
            logger.error(e)
            return identitylayer_pb2.CreateAndStoreMyDidResponse()


    async def ReplaceKeysStart(self, request, context):
        """Replace Keys Start
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            identity_json = json.dumps({"seed": get_value(request.IdentityJson.Seed),
                "crypto_type":get_value(request.IdentityJson.CryptoType)})
            resp = await indy_did.replace_keys_start(wallet_handle, did, identity_json)
            return identitylayer_pb2.ReplaceKeysStartResponse(Verkey=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ReplaceKeysStart ------")
            logger.error(e.message)
            return identitylayer_pb2.ReplaceKeysStartResponse() 
        except Exception as e:
            logger.error("Exception occurred @ ReplaceKeysStart----")
            logger.error(e)
            return identitylayer_pb2.ReplaceKeysStartResponse()


    async def ReplaceKeysApply(self, request, context):
        """Replace Keys Apply
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            resp = await indy_did.replace_keys_apply(wallet_handle, did)
            return identitylayer_pb2.ReplaceKeysApplyResponse(ErrorCode=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ReplaceKeysApply ------")
            logger.error(e.message)
            return identitylayer_pb2.ReplaceKeysApplyResponse(ErrorCode=e.error_code) 
        except Exception as e:
            logger.error("Exception occurred @ ReplaceKeysApply----")
            logger.error(e)
            return identitylayer_pb2.ReplaceKeysApplyResponse(ErrorCode=StatusCode.INTERNAL.value[0])


    async def StoreTheirDid(self, request, context):
        """Store Their Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            identity_json = json.dumps({"did": get_value(request.IdentityJson.Did),
                "verkey": get_value(request.IdentityJson.Verkey),
                "crypto_type":get_value(request.IdentityJson.CryptoType)})
            resp = await indy_did.store_their_did(wallet_handle, identity_json)
            return identitylayer_pb2.StoreTheirDidResponse(ErrorCode=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ StoreTheirDid ------")
            logger.error(e.message)
            return identitylayer_pb2.StoreTheirDidResponse(ErrorCode=e.error_code) 
        except Exception as e:
            logger.error("Exception occurred @ StoreTheirDid----")
            logger.error(e)
            return identitylayer_pb2.StoreTheirDidResponse(ErrorCode=StatusCode.INTERNAL.value[0])


    async def DidCreateKey(self, request, context):
        """Create Key; Prefix 'Did' to avoid co
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            key_json = json.dumps({"did": get_value(request.KeyJson.Did),
                "crypto_type":get_value(request.KeyJson.CryptoType)})
            resp = await indy_did.create_key(wallet_handle, key_json)
            return identitylayer_pb2.DidCreateKeyResponse(verkey=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ DidCreateKey ------")
            logger.error(e.message)
            return identitylayer_pb2.DidCreateKeyResponse() 
        except Exception as e:
            logger.error("Exception occurred @ DidCreateKey----")
            logger.error(e)
            return identitylayer_pb2.DidCreateKeyResponse()


    async def DidSetKeyMetadata(self, request, context):
        """Set Key Metadata
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            verkey = get_value(request.Verkey)
            metadata = get_value(request.Metadata)
            resp = await indy_did.set_key_metadata(wallet_handle, verkey, metadata)
            return identitylayer_pb2.DidSetKeyMetadataResponse(ErrorCode=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ DidSetKeyMetadata ------")
            logger.error(e.message)
            return identitylayer_pb2.DidSetKeyMetadataResponse(ErrorCode=e.error_code) 
        except Exception as e:
            logger.error("Exception occurred @ DidSetKeyMetadata----")
            logger.error(e)
            return identitylayer_pb2.DidSetKeyMetadataResponse(ErrorCode=StatusCode.INTERNAL.value[0])


    async def DidGetKeyMetadata(self, request, context):
        """Get Key Metadata
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            verkey = get_value(request.Verkey)
            resp = await indy_did.get_key_metadata(wallet_handle, verkey)
            return identitylayer_pb2.DidGetKeyMetadataResponse(Metadata=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ DidGetKeyMetadata ------")
            logger.error(e.message)
            return identitylayer_pb2.DidGetKeyMetadataResponse() 
        except Exception as e:
            logger.error("Exception occurred @ DidGetKeyMetadata----")
            logger.error(e)
            return identitylayer_pb2.DidGetKeyMetadataResponse()


    async def KeyForDid(self, request, context):
        """Key For Did
        """
        try:
            pool_handle = get_value(request.PoolHandle)
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            resp = await indy_did.key_for_did(pool_handle, wallet_handle, did)
            return identitylayer_pb2.KeyForDidResponse(key=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ KeyForDid ------")
            logger.error(e.message)
            return identitylayer_pb2.KeyForDidResponse() 
        except Exception as e:
            logger.error("Exception occurred @ KeyForDid----")
            logger.error(e)
            return identitylayer_pb2.KeyForDidResponse()


    async def KeyForLocalDid(self, request, context):
        """Key For Local Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            resp = await indy_did.key_for_local_did(wallet_handle, did)
            return identitylayer_pb2.KeyForLocalDidResponse(key=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ KeyForLocalDid ------")
            logger.error(e.message)
            return identitylayer_pb2.KeyForLocalDidResponse() 
        except Exception as e:
            logger.error("Exception occurred @ KeyForLocalDid----")
            logger.error(e)
            return identitylayer_pb2.KeyForLocalDidResponse()


    async def SetEndpointForDid(self, request, context):
        """Set Endpoint For Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            address = get_value(request.Address)
            transport_key = get_value(request.TransportKey)
            resp = await indy_did.set_endpoint_for_did(wallet_handle, did, address, transport_key)
            return identitylayer_pb2.SetEndpointForDidResponse(ErrorCode=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ SetEndpointForDid ------")
            logger.error(e.message)
            return identitylayer_pb2.SetEndpointForDidResponse(ErrorCode=e.error_code) 
        except Exception as e:
            logger.error("Exception occurred @ SetEndpointForDid----")
            logger.error(e)
            return identitylayer_pb2.SetEndpointForDidResponse(ErrorCode=StatusCode.INTERNAL.value[0])


    async def GetEndpointForDid(self, request, context):
        """Get Endpoint For Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            pool_handle = get_value(request.PoolHandle)
            did = get_value(request.Did)
            resp = await indy_did.get_endpoint_for_did(wallet_handle, pool_handle, did)
            return identitylayer_pb2.GetEndpointForDidResponse(Endpoint=resp[0], TransportVk=resp[1])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ GetEndpointForDid ------")
            logger.error(e.message)
            return identitylayer_pb2.GetEndpointForDidResponse() 
        except Exception as e:
            logger.error("Exception occurred @ GetEndpointForDid----")
            logger.error(e)
            return identitylayer_pb2.GetEndpointForDidResponse()


    async def SetDidMetadata(self, request, context):
        """Set Did Metadata
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            metadata = get_value(request.Metadata)
            resp = await indy_did.set_did_metadata(wallet_handle, did, metadata)
            return identitylayer_pb2.SetDidMetadataResponse(Error=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ SetDidMetadata ------")
            logger.error(e.message)
            return identitylayer_pb2.SetDidMetadataResponse(Error=e.error_code) 
        except Exception as e:
            logger.error("Exception occurred @ SetDidMetadata----")
            logger.error(e)
            return identitylayer_pb2.SetDidMetadataResponse(Error=StatusCode.INTERNAL.value[0])


    async def GetDidMetadata(self, request, context):
        """Get Did Metadata
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            resp = await indy_did.get_did_metadata(wallet_handle, did)
            return identitylayer_pb2.GetDidMetadataResponse(Metadata=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ GetDidMetadata ------")
            logger.error(e.message)
            return identitylayer_pb2.GetDidMetadataResponse() 
        except Exception as e:
            logger.error("Exception occurred @ GetDidMetadata----")
            logger.error(e)
            return identitylayer_pb2.GetDidMetadataResponse()


    async def GetMyDidWithMeta(self, request, context):
        """Get My Did With Meta
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            resp = await indy_did.get_my_did_with_meta(wallet_handle, did)
            return identitylayer_pb2.GetMyDidWithMetaResponse(Did=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ GetMyDidWithMeta ------")
            logger.error(e.message)
            return identitylayer_pb2.GetMyDidWithMetaResponse() 
        except Exception as e:
            logger.error("Exception occurred @ GetMyDidWithMeta----")
            logger.error(e)
            return identitylayer_pb2.GetMyDidWithMetaResponse()


    async def ListMyDidsWithMeta(self, request, context):
        """List My Dids With Meta
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            resp = await indy_did.list_my_dids_with_meta(wallet_handle)
            return identitylayer_pb2.ListMyDidsWithMetaResponse(Did=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ListMyDidsWithMeta ------")
            logger.error(e.message)
            return identitylayer_pb2.ListMyDidsWithMetaResponse() 
        except Exception as e:
            logger.error("Exception occurred @ ListMyDidsWithMeta----")
            logger.error(e)
            return identitylayer_pb2.ListMyDidsWithMetaResponse()


    async def AbbreviateVerkey(self, request, context):
        """Abbreviate Verkey
        """
        try:
            did = get_value(request.Did)
            verkey = get_value(request.FullVerkey)
            resp = await indy_did.abbreviate_verkey(did, verkey)
            return identitylayer_pb2.AbbreviateVerkeyResponse(Metadata=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ AbbreviateVerkey ------")
            logger.error(e.message)
            return identitylayer_pb2.AbbreviateVerkeyResponse() 
        except Exception as e:
            logger.error("Exception occurred @ AbbreviateVerkey----")
            logger.error(e)
            return identitylayer_pb2.AbbreviateVerkeyResponse()
