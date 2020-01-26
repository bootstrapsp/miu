import os
import sys

from indy import blob_storage as indy_blob_storage


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR+'/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))

from ..identityLayer import identitylayer_pb2
from ..identityLayer import identitylayer_pb2_grpc


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


class BlobStorageServiceServicer(object):
    """`blob storage` services
    """
    async def OpenReader(self, request, context):
        try:
            type_, config = get_value(request.Type_), get_value(request.Config)
            resp = await indy_blob_storage.open_reader(type_, config)
            return identitylayer_pb2.OpenReaderResponse(Res=resp)
        except Exception as e:
            logger.error("Exception occurred @ OpenReader")
            logger.error(e)
            return identitylayer_pb2.OpenReaderResponse()

    async def OpenWriter(self, request, context):
        try:
            type_ = get_value(request.Type_)
            config = get_value(request.Config)
            resp = await indy_blob_storage.open_writer(type_, config)
            return identitylayer_pb2.OpenWriterRequest(Res=resp)
        except Exception as e:
            logger.error("Exception occurred @ OpenWriter")
            logger.error(e)
            return identitylayer_pb2.OpenWriterResponse()
