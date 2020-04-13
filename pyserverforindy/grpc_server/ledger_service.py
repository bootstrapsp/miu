import os
import sys

from indy import ledger as indy_ledger, IndyError
from indy.error import ErrorCode


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.abspath(ROOT_DIR+'/identityLayer'))
sys.path.append(os.path.abspath(ROOT_DIR))

from identityLayer import identitylayer_pb2


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


class LedgerServiceServicer(object):
    """`ledger` services
    """

    async def SignAndSubmitRequest(self, request, context):
        try:
            pool_handle, wallet_handle, submitter_did, request_json = get_value(request.PoolHandle), get_value(request.WalletHandle), get_value(request.SubmitterDid), get_value(request.RequestJson)
            resp = await indy_ledger.sign_and_submit_request(pool_handle, wallet_handle, submitter_did, request_json)
            return identitylayer_pb2.SignAndSubmitRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ SignAndSubmitRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.SignAndSubmitRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ SignAndSubmitRequest----")
            logger.error(e)
            return identitylayer_pb2.SignAndSubmitRequestRs()


    async def SubmitRequest(self, request, context):
        try:
            pool_handle, request_json = get_value(request.PoolHandle), get_value(request.RequestJson)
            resp = await indy_ledger.submit_request(pool_handle, request_json)
            return identitylayer_pb2.SubmitRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ SubmitRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.SubmitRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ SubmitRequest----")
            logger.error(e)
            return identitylayer_pb2.SubmitRequestRs()


    async def SubmitAction(self, request, context):
        try:
            pool_handle, request_json, nodes, timeout = get_value(request.PoolHandle), get_value(request.RequestJson), get_value(request.Nodes), get_value(request.Timeout)
            resp = await indy_ledger.submit_action(pool_handle, request_json, nodes, timeout)
            return identitylayer_pb2.SubmitActionRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ SubmitAction ------")
            logger.error(e.message)
            return identitylayer_pb2.SubmitActionRs() 
        except Exception as e:
            logger.error("Exception occurred @ SubmitAction----")
            logger.error(e)
            return identitylayer_pb2.SubmitActionRs()


    async def SignRequest(self, request, context):
        try:
            wallet_handle, submitter_did, request_json = get_value(request.WalletHandle), get_value(request.SubmitterDid), get_value(request.RequestJson)
            resp = await indy_ledger.sign_request(wallet_handle, submitter_did, request_json)
            return identitylayer_pb2.SignRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ SignRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.SignRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ SignRequest----")
            logger.error(e)
            return identitylayer_pb2.SignRequestRs()


    async def MultiSignRequest(self, request, context):
        try:
            wallet_handle, submitter_did, request_json = get_value(request.WalletHandle), get_value(request.SubmitterDid), get_value(request.RequestJson)
            resp = await indy_ledger.multi_sign_request(wallet_handle, submitter_did, request_json)
            return identitylayer_pb2.MultiSignRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ MultiSignRequestRs ------")
            logger.error(e.message)
            return identitylayer_pb2.MultiSignRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ MultiSignRequest----")
            logger.error(e)
            return identitylayer_pb2.MultiSignRequestRs()


    async def BuildGetDdoRequest(self, request, context):
        try:
            submitter_did, target_did = get_value(request.SubmitterDid), get_value(request.TargetDid)
            resp = await indy_ledger.build_get_ddo_request(submitter_did, target_did)
            return identitylayer_pb2.BuildGetDdoRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetDdoRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetDdoRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildGetDdoRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetDdoRequestRs()


    async def BuildNymRequest(self, request, context):
        try:
            submitter_did, target_did, ver_key, alias, role = get_value(request.SubmitterDid), get_value(request.TargetDid), get_value(request.VerKey), get_value(request.Alias), get_value(request.Role)
            resp = await indy_ledger.build_nym_request(submitter_did, target_did, ver_key, alias, role)
            return identitylayer_pb2.BuildNymRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildNymRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildNymRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildNymRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildNymRequestRs() 


    async def BuildAttribRequest(self, request, context):
        try:
            submitter_did, target_did, xhash, raw, enc = get_value(request.SubmitterDid), get_value(request.TargetDid), get_value(request.Xhash), get_value(request.Raw), get_value(request.Enc)
            resp = await indy_ledger.build_attrib_request(submitter_did, target_did, xhash, raw, enc)
            return identitylayer_pb2.BuildAttribRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildAttribRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildAttribRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildAttribRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildAttribRequestRs()


    async def BuildGetAttribRequest(self, request, context):
        try:
            submitter_did, target_did, raw, xhash, enc = get_value(request.SubmitterDid), get_value(request.TargetDid), get_value(request.Raw), get_value(request.Xhash), get_value(request.Enc)
            resp = await indy_ledger.build_get_attrib_request(submitter_did, target_did, raw, xhash, enc)
            return identitylayer_pb2.BuildGetAttribRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetAttribRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetAttribRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildGetAttribRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetAttribRequestRs()


    async def BuildGetNymRequest(self, request, context):
        try:
            submitter_did, target_did = get_value(request.SubmitterDid), get_value(request.TargetDid)
            resp = await indy_ledger.build_get_nym_request(submitter_did, target_did)
            return identitylayer_pb2.BuildGetNymRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetNymRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetNymRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildGetNymRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetNymRequestRs()


    async def BuildSchemaRequest(self, request, context):
        try:
            submitter_did, data = get_value(request.SubmitterDid), get_value(request.Data)
            resp = await indy_ledger.build_schema_request(submitter_did, data)
            return identitylayer_pb2.BuildSchemaRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildSchemaRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildSchemaRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildSchemaRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildSchemaRequestRs()


    async def BuildGetSchemaRequest(self, request, context):
        try:
            submitter_did, id_ = get_value(request.SubmitterDid), get_value(request.Id_)
            resp = await indy_ledger.build_get_schema_request(submitter_did, id_)
            return identitylayer_pb2.BuildGetSchemaRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetSchemaRequestRs ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetSchemaRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildGetSchemaRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetSchemaRequestRs()


    async def ParseGetSchemaResponse(self, request, context):
        try:
            get_schema_response = get_value(request.GetSchemaResponse)
            resp = await indy_ledger.parse_get_schema_response(get_schema_response)
            return identitylayer_pb2.ParseGetSchemaResponseRs(Id=resp[0], SchemaJson=resp[1])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ParseGetSchemaResponse ------")
            logger.error(e.message)
            return identitylayer_pb2.ParseGetSchemaResponseRs() 
        except Exception as e:
            logger.error("Exception occurred @ ParseGetSchemaResponse----")
            logger.error(e)
            return identitylayer_pb2.ParseGetSchemaResponseRs()


    async def BuildCredDefRequest(self, request, context):
        try:
            submitter_did, data = get_value(request.SubmitterDid), get_value(request.Data)
            resp = await indy_ledger.build_cred_def_request(submitter_did, data)
            return identitylayer_pb2.BuildCredDefRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildCredDefRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildCredDefRequest() 
        except Exception as e:
            logger.error("Exception occurred @ BuildCredDefRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildCredDefRequestRs()


    async def BuildGetCredDefRequest(self, request, context):
        try:
            submitter_did, id_ = get_value(request.SubmitterDid), get_value(request.Id_)
            resp = await indy_ledger.build_get_cred_def_request(submitter_did, id_)
            return identitylayer_pb2.BuildGetCredDefRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetCredDefRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetCredDefRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildGetCredDefRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetCredDefRequestRs()


    async def ParseGetCredDefResponse(self, request, context):
        try:
            get_cred_def_response = get_value(request.GetCredDefResponse)
            resp = await indy_ledger.parse_get_cred_def_response(get_cred_def_response)
            return identitylayer_pb2.ParseGetCredDefResponseRs(CredentialDefinitionId=resp[0], CredentialDefinitionJson=resp[1])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ParseGetCredDefResponse ------")
            logger.error(e.message)
            return identitylayer_pb2.ParseGetCredDefResponseRs() 
        except Exception as e:
            logger.error("Exception occurred @ ParseGetCredDefResponse----")
            logger.error(e)
            return identitylayer_pb2.ParseGetCredDefResponseRs()


    async def BuildNodeRequest(self, request, context):
        try:
            submitter_did, target_did, data = get_value(request.SubmitterDid), get_value(request.TargetDid), get_value(request.Data)
            resp = await indy_ledger.build_node_request(submitter_did, target_did, data)
            return identitylayer_pb2.BuildNodeRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildNodeRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildNodeRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildNodeRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildNodeRequestRs()


    async def BuildGetValidatorInfoRequest(self, request, context):
        try:
            submitter_did = get_value(request.SubmitterDid)
            resp = await indy_ledger.build_get_validator_info_request(submitter_did)
            return identitylayer_pb2.BuildGetValidatorInfoRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetValidatorInfoRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetValidatorInfoRequestRs() 
        except Exception as e:
            logger.error("Exception occurred @ BuildGetValidatorInfoRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetValidatorInfoRequestRs()


    async def BuildGetTxnRequest(self, request, context):
        try:
            submitter_did, ledger_type, seq_no = get_value(request.SubmitterDid), get_value(request.LedgerType), get_value(request.SeqNo)
            resp = await indy_ledger.build_get_txn_request(submitter_did, ledger_type, seq_no)
            return identitylayer_pb2.BuildGetTxnRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetTxnRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetTxnRequestRs()    
        except Exception as e:
            logger.error("Exception occurred @ BuildGetTxnRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetTxnRequestRs()


    async def BuildPoolConfigRequest(self, request, context):
        try:
            submitter_did, writes, force = get_value(request.SubmitterDid), get_value(request.Writes), get_value(request.Force)
            resp = await indy_ledger.build_pool_config_request(submitter_did, writes, force)
            return identitylayer_pb2.BuildPoolConfigRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildPoolConfigRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildPoolConfigRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildPoolConfigRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildPoolConfigRequestRs()


    async def BuildPoolRestartRequest(self, request, context):
        try:
            submitter_did, action, datetime = get_value(request.SubmitterDid), get_value(request.Action), get_value(request.Datetime)
            resp = await indy_ledger.build_pool_restart_request(submitter_did, action, datetime)
            return identitylayer_pb2.BuildPoolRestartRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildPoolRestartRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildPoolRestartRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildPoolRestartRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildPoolRestartRequestRs()


    async def BuildPoolUpgradeRequest(self, request, context):
        try:
            submitter_did, name, version, action, _sha256, _timeout, schedule, justification, reinstall, force, package = get_value(request.submitter_did), get_value(request.name), get_value(request.version), get_value(request.action), get_value(request.str), get_value(request.str), get_value(request.schedule), get_value(request.str), get_value(request.str), get_value(request.bool), get_value(request.package), 
            resp = await indy_ledger.build_pool_upgrade_request(submitter_did, name, version, action, _sha256, _timeout, schedule, justification, reinstall, force, package)
            return identitylayer_pb2.BuildPoolUpgradeRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildPoolUpgradeRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildPoolUpgradeRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildPoolUpgradeRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildPoolUpgradeRequestRs()


    async def BuildRevocRegDefRequest(self, request, context):
        try:
            submitter_did, data = get_value(request.SubmitterDid), get_value(request.Data)
            resp = await indy_ledger.build_revoc_reg_def_request(submitter_did, data)
            return identitylayer_pb2.BuildRevocRegDefRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildRevocRegDefRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildRevocRegDefRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildRevocRegDefRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildRevocRegDefRequestRs()


    async def BuildGetRevocRegDefRequest(self, request, context):
        try:
            submitter_did, rev_reg_def_id = get_value(request.SubmitterDid), get_value(request.RevRegDefId)
            resp = await indy_ledger.build_get_revoc_reg_def_request(submitter_did, rev_reg_def_id)
            return identitylayer_pb2.BuildGetRevocRegDefRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetRevocRegDefRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetRevocRegDefRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildGetRevocRegDefRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetRevocRegDefRequestRs()


    async def ParseGetRevocRegDefResponse(self, request, context):
        try:
            get_revoc_ref_def_response = get_value(request.GetRevocRefDefResponse)
            resp = await indy_ledger.parse_get_revoc_reg_def_response(get_revoc_ref_def_response)
            return identitylayer_pb2.ParseGetRevocRegDefResponseRs(RevocationId=resp[0], RevocationJson=resp[1])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ParseGetRevocRegDefResponse ------")
            logger.error(e.message)
            return identitylayer_pb2.ParseGetRevocRegDefResponseRs()  
        except Exception as e:
            logger.error("Exception occurred @ ParseGetRevocRegDefResponse----")
            logger.error(e)
            return identitylayer_pb2.ParseGetRevocRegDefResponseRs()


    async def BuildRevocRegEntryRequest(self, request, context):
        try:
            submitter_did, revoc_reg_def_id, rev_def_type, value = get_value(request.SubmitterDid), get_value(request.RevocRegDefId), get_value(request.RevDefType), get_value(request.Value)
            resp = await indy_ledger.build_revoc_reg_entry_request(submitter_did, revoc_reg_def_id, rev_def_type, value)
            return identitylayer_pb2.BuildRevocRegEntryRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildRevocRegEntryRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildRevocRegEntryRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildRevocRegEntryRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildRevocRegEntryRequestRs()


    async def BuildGetRevocRegRequest(self, request, context):
        try:
            submitter_did, revoc_reg_def_id, timestamp = get_value(request.SubmitterDid), get_value(request.RevocRegDefId),int( get_value(request.Timestamp))
            resp = await indy_ledger.build_get_revoc_reg_request(submitter_did, revoc_reg_def_id, timestamp)
            return identitylayer_pb2.BuildGetRevocRegRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetRevocRegRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetRevocRegRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildGetRevocRegRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetRevocRegRequestRs()


    async def ParseGetRevocRegResponse(self, request, context):
        try:
            get_revoc_reg_response = get_value(request.GetRevocRegResponse)
            resp = await indy_ledger.parse_get_revoc_reg_response(get_revoc_reg_response)
            return identitylayer_pb2.ParseGetRevocRegResponseRs(Id=resp[0], Json=resp[1], Timestamp=resp[2])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ParseGetRevocRegResponseRs ------")
            logger.error(e.message)
            return identitylayer_pb2.ParseGetRevocRegResponseRs()  
        except Exception as e:
            logger.error("Exception occurred @ ParseGetRevocRegResponseRs----")
            logger.error(e)
            return identitylayer_pb2.ParseGetRevocRegResponseRs()


    async def BuildGetRevocRegDeltaRequest(self, request, context):
        try:
            submitter_did, revoc_reg_def_id, from_, to = get_value(request.SubmiterDid), get_value(request.RevocRegDefId), get_value(request.From_), get_value(request.To)
            resp = await indy_ledger.build_get_revoc_reg_delta_request(submitter_did, revoc_reg_def_id, from_, to)
            return identitylayer_pb2.BuildGetRevocRegDeltaRequestRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ BuildGetRevocRegDeltaRequest ------")
            logger.error(e.message)
            return identitylayer_pb2.BuildGetRevocRegDeltaRequestRs()  
        except Exception as e:
            logger.error("Exception occurred @ BuildGetRevocRegDeltaRequest----")
            logger.error(e)
            return identitylayer_pb2.BuildGetRevocRegDeltaRequestRs()


    async def ParseGetRevocRegDeltaResponse(self, request, context):
        try:
            get_revoc_reg_delta_response = get_value(request.GetRevocRegDeltaResponse)
            resp = await indy_ledger.parse_get_revoc_reg_delta_response(get_revoc_reg_delta_response)
            return identitylayer_pb2.ParseGetRevocRegDeltaResponseRs(Id=resp[0],Json=resp[1],Timestamp=resp[2])
        except IndyError as e:
            logger.error("Indy Exception Occurred @ ParseGetRevocRegDeltaResponse ------")
            logger.error(e.message)
            return identitylayer_pb2.ParseGetRevocRegDeltaResponseRs()  
        except Exception as e:
            logger.error("Exception occurred @ ParseGetRevocRegDeltaResponse----")
            logger.error(e)
            return identitylayer_pb2.ParseGetRevocRegDeltaResponseRs()


    async def GetResponseMetadata(self, request, context):
        try:
            response = get_value(request.Response)
            resp = await indy_ledger.get_response_metadata(response)
            return identitylayer_pb2.GetResponseMetadataRs(Resp=resp)
        except IndyError as e:
            logger.error("Indy Exception Occurred @ GetResponseMetadata ------")
            logger.error(e.message)
            return identitylayer_pb2.GetResponseMetadataRs()  
        except Exception as e:
            logger.error("Exception occurred @ GetResponseMetadata----")
            logger.error(e)
            return identitylayer_pb2.GetResponseMetadataRs()

