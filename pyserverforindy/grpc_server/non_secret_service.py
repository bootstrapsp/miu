import os
import sys

from indy import non_secrets as indy_non_secret, IndyError
from indy.error import ErrorCode
from grpc import StatusCode



ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR+'/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))


from identityLayer import identitylayer_pb2



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


class NonSecretServiceServicer(object):
    """`non-secret` services
    """

    async def AddWalletRecord(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_, value, tags_json = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id_), get_value(request.Value), get_value(request.TagsJson)
            resp = await indy_non_secret.add_wallet_record(wallet_handle, type_, id_, value, tags_json)
            return identitylayer_pb2.AddWalletRecordResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ AddWalletRecord ------")
            logger.error(e.message)
            return identitylayer_pb2.AddWalletRecordResponse(Resp = e.message) 
        except Exception as e:
            logger.error("Exception occurred @ AddWalletRecord")
            logger.error(e)
            return identitylayer_pb2.AddWalletRecordResponse(Resp=str(e))


    async def UpdateWalletRecordValue(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_, value = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id_), get_value(request.Value)
            resp = await indy_non_secret.update_wallet_record_value(wallet_handle, type_, id_, value)
            return identitylayer_pb2.UpdateWalletRecordValueResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ UpdateWalletRecordValue ------")
            logger.error(e.message)
            return identitylayer_pb2.UpdateWalletRecordValueResponse(Resp = e.message)
        except Exception as e:
            logger.error("Exception occurred @ UpdateWalletRecordValue")
            logger.error(e)
            return identitylayer_pb2.UpdateWalletRecordValueResponse(Resp=str(e))


    async def UpdateWalletRecordTags(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_, tags_json = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id_), get_value(request.TagsJson)
            resp = await indy_non_secret.update_wallet_record_tags(wallet_handle, type_, id_, tags_json)
            return identitylayer_pb2.UpdateWalletRecordTagsResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ UpdateWalletRecordTags ------")
            logger.error(e.message)
            return identitylayer_pb2.UpdateWalletRecordTagsResponse(Resp = e.message)
        except Exception as e:
            logger.error("Exception occurred @ UpdateWalletRecordTags")
            logger.error(e)
            return identitylayer_pb2.UpdateWalletRecordTagsResponse(Resp=str(e))


    async def AddWalletRecordTags(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_, tags_json = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id_), get_value(request.TagsJson)
            resp = await indy_non_secret.add_wallet_record_tags(wallet_handle, type_, id_, tags_json)
            return identitylayer_pb2.AddWalletRecordTagsResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ AddWalletRecordTags ------")
            logger.error(e.message)
            return identitylayer_pb2.AddWalletRecordTagsResponse(Resp = e.message)
        except Exception as e:
            logger.error("Exception occurred @ AddWalletRecordTags")
            logger.error(e)
            return identitylayer_pb2.AddWalletRecordTagsResponse(Resp=str(e))


    async def DeleteWalletRecordTags(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_, tag_names_json = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id_), get_value(request.TagNamesJson)
            resp = await indy_non_secret.delete_wallet_record_tags(wallet_handle, type_, id_, tag_names_json)
            return identitylayer_pb2.DeleteWalletRecordTagsResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ DeleteWalletRecordTags ------")
            logger.error(e.message)
            return identitylayer_pb2.DeleteWalletRecordTagsResponse(Resp = e.message)
        except Exception as e:
            logger.error("Exception occurred @ DeleteWalletRecordTags")
            logger.error(e)
            return identitylayer_pb2.DeleteWalletRecordTagsResponse(Resp= str(e))


    async def DeleteWalletRecord(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_ = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id_)
            resp = await indy_non_secret.delete_wallet_record(wallet_handle, type_, id_)
            return identitylayer_pb2.DeleteWalletRecordResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ DeleteWalletRecord ------")
            logger.error(e.message)
            return identitylayer_pb2.DeleteWalletRecordResponse(Resp = e.message)
        except Exception as e:
            logger.error("Exception occurred @ DeleteWalletRecord")
            logger.error(e)
            return identitylayer_pb2.DeleteWalletRecordResponse(Resp=str(e))


    async def GetWalletRecord(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, id_, options_json = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.Id), get_value(request.OptionsJson)
            resp = await indy_non_secret.get_wallet_record(wallet_handle, type_, id_, options_json)
            return identitylayer_pb2.GetWalletRecordResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ GetWalletRecord ------")
            logger.error(e.message)
            return identitylayer_pb2.GetWalletRecordResponse(Resp = e.message)
        except Exception as e:
            logger.error("Exception occurred @ GetWalletRecord")
            logger.error(e)
            return identitylayer_pb2.GetWalletRecordResponse(Resp = str(e))


    async def OpenWalletSearch(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, type_, query_json, options_json = get_value(request.WalletHandle), get_value(request.Type_), get_value(request.QueryJson), get_value(request.OptionsJson)
            resp = await indy_non_secret.open_wallet_search(wallet_handle, type_, query_json, options_json)
            return identitylayer_pb2.OpenWalletSearchResponse(SearchHandle=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ OpenWalletSearch ------")
            logger.error(e.message)
            return identitylayer_pb2.OpenWalletSearchResponse(SearchHandle = -1)
        except Exception as e:
            logger.error("Exception occurred @ OpenWalletSearch")
            logger.error(e)
            return identitylayer_pb2.OpenWalletSearchResponse(SearchHandle = -1)


    async def FetchWalletSearchNextRecords(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle, wallet_search_handle, count = get_value(request.WalletHandle), get_value(request.WalletSearchHandle), get_value(request.Count)
            resp = await indy_non_secret.fetch_wallet_search_next_records(wallet_handle, wallet_search_handle, count)
            return identitylayer_pb2.FetchWalletSearchNextRecordsResponse(WalletRecordsJson=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ FetchWalletSearchNextRecords ------")
            logger.error(e.message)
            return identitylayer_pb2.FetchWalletSearchNextRecordsResponse(WalletRecordsJson = e.message)
        except Exception as e:
            logger.error("Exception occurred @ FetchWalletSearchNextRecords")
            logger.error(e)
            return identitylayer_pb2.FetchWalletSearchNextRecordsResponse(WalletRecordsJson = str(e))


    async def CloseWalletSearch(self, request, context):
        # missing associated documentation comment in .proto file
        try:
            wallet_handle = get_value(request.WalletHandle)
            resp = await indy_non_secret.close_wallet_search(wallet_handle)
            return identitylayer_pb2.CloseWalletSearchResponse(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ CloseWalletSearch ------")
            logger.error(e.message)
            return identitylayer_pb2.FetchWalletSearchNextRecordsResponse(Resp= e.message)
        except Exception as e:
            logger.error("Exception occurred @ CloseWalletSearch")
            logger.error(e)
            return identitylayer_pb2.CloseWalletSearchResponse(Resp=str(e))

