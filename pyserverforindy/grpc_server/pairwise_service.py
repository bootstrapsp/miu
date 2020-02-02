import os
import sys

from indy import pairwise as indy_pairwise


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



class PairwiseServiceServicer(identitylayer_pb2_grpc.PairwiseServiceServicer):
    """`pairwise` Services
    """
    async def IsPairwiseExists(self, request, context):
        """Is Pairwise Exists
        """
        resp = None
        try:
            wallet_handle = get_value(request.WalletHandle)
            their_did = get_value(request.TheirDid)
            resp = await indy_pairwise.is_pairwise_exists(wallet_handle, their_did)
            return identitylayer_pb2.IsPairwiseExistsResponse(Res=resp)
        except Exception as e:
            logger.error("Exception occurred @ IsPairwiseExists--------")
            logger.error(e)
            return identitylayer_pb2.IsPairwiseExistsResponse(Res=resp)


    async def CreatePairwise(self, request, context):
        """Create Pairwise
        """
        resp = None
        try:
            wallet_handle = get_value(request.WalletHandle)
            their_did = get_value(request.TheirDid)
            my_did = get_value(request.MyDid)
            metadata = get_value(request.Metadata)
            resp = await indy_pairwise.create_pairwise(wallet_handle, their_did, my_did, metadata)
            return identitylayer_pb2.CreatePairwiseResponse(ErrorCode=resp)
        except Exception as e:
            logger.error("Exception occurred @ CreatePairwise--------")
            logger.error(e)
            return identitylayer_pb2.CreatePairwiseResponse(ErrorCode=resp)

    async def ListPairwise(self, request, context):
        """List Pairwise
        """
        resp = None
        try:
            wallet_handle = get_value(request.WalletHandle)
            resp = await indy_pairwise.list_pairwise(wallet_handle)
            return identitylayer_pb2.ListPairwiseResponse(PairwiseList=resp)
        except Exception as e:
            logger.error("Exception occurred @ ListPairwise--------")
            logger.error(e)
            return identitylayer_pb2.ListPairwiseResponse(PairwiseList=resp)

    async def GetPairwise(self, request, context):
        """Get Pairwise
        """
        resp = None
        try:
            wallet_handle = get_value(request.WalletHandle)
            their_did = get_value(request.TheirDid)
            resp = await indy_pairwise.get_pairwise(wallet_handle, their_did)
            return identitylayer_pb2.GetPairwiseResponse(PairwiseInfoJson=resp)
        except Exception as e:
            logger.error("Exception occurred @ GetPairwise--------")
            logger.error(e)
            return identitylayer_pb2.GetPairwiseResponse(PairwiseInfoJson=resp)

    async def SetPairwiseMetadata(self, request, context):
        """Set Pairwise
        """
        resp = None
        try:
            wallet_handle = get_value(request.WalletHandle)
            their_did = get_value(request.TheirDid)
            metadata = get_value(request.Metadata)
            resp = await indy_pairwise.set_pairwise_metadata(wallet_handle, their_did, metadata)
            return identitylayer_pb2.SetPairwiseMetadataResponse(ErrorCode=resp)
        except Exception as e:
            logger.error("Exception occurred @ SetPairwiseMetadata--------")
            logger.error(e)
            return identitylayer_pb2.SetPairwiseMetadataResponse(ErrorCode=resp)
