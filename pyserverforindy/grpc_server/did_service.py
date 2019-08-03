import asyncio
import json
import time
import math
import os
import sys
import base64
import binascii

import warnings
# warnings.simplefilter('ignore')
from concurrent import futures
import grpc

from indy import did as indy_did


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
            return identitylayer_pb2.CreateAndStoreMyDidResponse(Did=resp[0], Verkey=Did[1])
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
            resp = await indy_did.replace_keys_start(wallet_handle, did_json, identity_json)
            return identitylayer_pb2.ReplaceKeysStartResponse(resp)
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
            return identitylayer_pb2.ReplaceKeysApplyResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @ ReplaceKeysApply----")
            logger.error(e)
            return identitylayer_pb2.ReplaceKeysApplyResponse()


    async def StoreTheirDid(self, request, context):
        """Store Their Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            identity_json = json.dumps({"did": get_value(request.IdentityJson.Did),
                "verkey": get_value(request.IdentityJson.Verkey),
                "crypto_type":get_value(request.IdentityJson.CryptoType)})
            resp = await indy_did.store_their_did()
            return identitylayer_pb2.StoreTheirDidResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @ StoreTheirDid----")
            logger.error(e)
            return identitylayer_pb2.StoreTheirDidResponse()


    async def DidCreateKey(self, request, context):
        """Create Key; Prefix 'Did' to avoid co
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            key_json = json.dumps({"did": get_value(request.KeyJson.Did),
                "crypto_type":get_value(request.KeyJson.CryptoType)})
            resp = await indy_did.create_key()
            return identitylayer_pb2.DidCreateKeyResponse(verkey=resp)
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
            return identitylayer_pb2.DidSetKeyMetadataRequest(resp)
        except Exception as e:
            logger.error("Exception occurred @ DidSetKeyMetadata----")
            logger.error(e)
            return identitylayer_pb2.DidSetKeyMetadataRequest()


    async def DidGetKeyMetadata(self, request, context):
        """Get Key Metadata
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            verkey = get_value(request.Verkey)
            resp = await indy_did.get_key_metadata(wallet_handle, verkey)
            return identitylayer_pb2.DidGetKeyMetadataResponse(metadata)
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
            return identitylayer_pb2.SetEndpointForDidResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @ SetEndpointForDid----")
            logger.error(e)
            return identitylayer_pb2.SetEndpointForDidResponse()


    async def GetEndpointForDid(self, request, context):
        """Get Endpoint For Did
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            pool_handle = get_value(request.PoolHandle)
            did = get_value(request.Did)
            resp = await indy_did.get_endpoint_for_did(wallet_handle, pool_handle, did)
            return identitylayer_pb2.GetEndpointForDidResponse(Endpoint=resp[0], TransportVk=resp[1])
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
            return identitylayer_pb2.SetDidMetadataResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @ SetDidMetadata----")
            logger.error(e)
            return identitylayer_pb2.SetDidMetadataResponse()


    async def GetDidMetadata(self, request, context):
        """Get Did Metadata
        """
        try:
            wallet_handle = get_value(request.WalletHandle)
            did = get_value(request.Did)
            resp = await indy_did.get_did_metadata(wallet_handle, did)
            return identitylayer_pb2.GetDidMetadataResponse(Metadata=resp)
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
            return identitylayer_pb2.GetMyDidWithMetaResponse(resp)
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
            return identitylayer_pb2.ListMyDidsWithMetaResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @ ListMyDidsWithMeta----")
            logger.error(e)
            return identitylayer_pb2.ListMyDidsWithMetaResponse()


    async def AbbreviateVerkey(self, request, context):
        """Abbreviate Verkey
        """
        try:
            did = get_value(request.Did)
            verkey = get_value(request.Verkey)
            resp = await indy_did.abbreviate_verkey(did, verkey)
            return identitylayer_pb2.AbbreviateVerkeyResponse(resp)
        except Exception as e:
            logger.error("Exception occurred @ AbbreviateVerkey----")
            logger.error(e)
            return identitylayer_pb2.AbbreviateVerkeyResponse()
