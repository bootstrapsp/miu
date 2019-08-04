import json
import os
import sys

from indy import anoncreds as indy_anoncreds


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



class AnoncredsServiceServicer(identitylayer_pb2_grpc.AnoncredsServiceServicer):
    """
    `anoncreds` Services
    """

    async def IssuerCreateSchema(self, request, context):
        """Issuer Create Schema
        """
        try:
            issuer_did, name, version, attrs = get_value(request.IssuerDid), get_value(request.Name), get_value(request.Version), get_value(request.Attrs)
            resp = await indy_anoncreds.issuer_create_schema(issuer_did, name, version, attrs)
            return identitylayer_pb2.IssuerCreateSchemaResponse(SchemaId=str(resp[0]), SchemaJson=str(resp[1]))
        except Exception as e:
            logger.error("Exception Occurred @ IssuerCreateSchema------")
            logger.error(e)
            return identitylayer_pb2.IssuerCreateSchemaResponse(SchemaId='', SchemaJson='')


    async def IssuerCreateAndStoreCredentialDef(self, request, context):
        """ issuer create and store credential def
        """
        try:
            wallet_handle, issuer_did, schema_json, tag, signature_type, config_json = \
            get_value(request.WalletHandle), get_value(request.IssuerDid), get_value(request.SchemaJson), get_value(request.Tag), get_value(request.SignatureType), get_value(request.ConfigJson)
            resp = await indy_anoncreds.issuer_create_and_store_credential_def(wallet_handle, issuer_did, schema_json, tag, signature_type, config_json)
            return identitylayer_pb2.IssuerCreateAndStoreCredentialDefResponse(CredDefId=str(resp[0]), CredDefJson=str(resp[1]))
        except Exception as e:
            logger.error("Exception Occurred @IssuerCreateAndStoreCredentialDef ------")
            logger.error(e)
            return identitylayer_pb2.IssuerCreateAndStoreCredentialDefResponse(CredDefId='', CredDefJson='')


    async def IssuerCreateAndStoreRevocReg(self, request, context):
        """ Issuer Create And Store Revoc Reg
        """
        try:
            wallet_handle, issuer_did, revoc_def_type, tag, cred_def_id, config_json, tails_writer_handle = \
            get_value(request.WalletHandle), get_value(request.IssuerDid), get_value(request.RevocDefType), get_value(request.Tag), get_value(request.CredDefId), get_value(request.ConfigJSon), get_value(request.TailsWriterHandle)
            resp = await indy_anoncreds.issuer_create_and_store_revoc_reg(wallet_handle, issuer_did, revoc_def_type, tag, cred_def_id, config_json, tails_writer_handle)
            return identitylayer_pb2.IssuerCreateAndStoreRevocRegResponse(RevocRegId=str(resp[0]), RevocRegDefJson=str(resp[1]), RevocRegEntryJson=str(resp[2]))
        except Exception as e:
            logger.error("Exception Occurred @ IssuerCreateAndStoreRevocReg------")
            logger.error(e)
            return identitylayer_pb2.IssuerCreateAndStoreRevocRegResponse(RevocRegId='', RevocRegDefJson='', RevocRegEntryJson='')


    async def IssuerCreateCredentialOffer(self, request, context):
        """ Issuer Create Credential Offer
        """
        try:
            wallet_handle, cred_def_id = get_value(request.WalletHandle), get_value(request.CredDefId)
            resp = await indy_anoncreds.issuer_create_credential_offer(wallet_handle, cred_def_id)
            return identitylayer_pb2.IssuerCreateCredentialOfferResponse(SchemaId=resp[0], CreeDefId=resp[1], Nonce=resp[2], KeyCorrectnessProof=resp[3])
        except Exception as e:
            logger.error("Exception Occurred @IssuerCreateCredentialOffer------")
            logger.error(e)
            return identitylayer_pb2.IssuerCreateCredentialOfferResponse(SchemaId='', CreeDefId='', Nonce='', KeyCorrectnessProof='')


    async def IssuerCreateCredential(self, request, context):
        """ 
        """
        try:
            wallet_handle, cred_offer_json, cred_req_json, cred_values_json, rev_reg_id, blob_storage_reader_handle = \
            get_value(request.WalletHandle), get_value(request.CredOfferJson), get_value(request.CredReqJson), get_value(request.CredValuesJson), get_value(request.RevRegId), get_value(request.BlobStorageReaderHandle)
            resp = await indy_anoncreds.issuer_create_credential(wallet_handle, cred_offer_json, cred_req_json, cred_values_json, rev_reg_id, blob_storage_reader_handle)
            cred_json = identitylayer_pb2.CredJsonMessage
            cred_json.SchemaId = resp[0]['schema_id']
            cred_json.CredDefId = resp[0]['cred_def_id']
            cred_json.RevRegDefID = resp[0]['rev_reg_def_id']
            cred_json.Values = resp[0]['signature']
            cred_json.Signature = resp[0]['schema_id']
            cred_json.SignatureCorrectnessProof = resp[0]['signature_correctness_proof']
            return identitylayer_pb2.IssuerCreateCredentialResponse(CredJson=cred_json, CredRevocId=resp[1], RevocRegDeltaJson=resp[2])
        except Exception as e:
            logger.error("Exception Occurred @IssuerCreateCredential ------")
            logger.error(e)
            return identitylayer_pb2.IssuerCreateCredentialResponse(CredJson=identitylayer_pb2.CredJsonMessage, CredRevocId='', RevocRegDeltaJson='')


    async def IssuerRevokeCredential(self, request, context):
        """ Issuer Revoke Credential
        """
        try:
            wallet_handle, blob_storage_reader_handle, rev_reg_id, cred_revoc_id = get_value(request.WalletHandle), get_value(request.BlobStorageReaderHandle), get_value(request.RevRegId), get_value(request.CredRevocId)
            resp = await indy_anoncreds.issuer_revoke_credential(wallet_handle, blob_storage_reader_handle, rev_reg_id, cred_revoc_id)
            return identitylayer_pb2.IssuerRevokeCredentialResponse(RevocationRegistryDeltaJson=resp[0])
        except Exception as e:
            logger.error("Exception Occurred @IssuerRevokeCredential ------")
            logger.error(e)
            return identitylayer_pb2.IssuerRevokeCredentialResponse(RevocationRegistryDeltaJson='')


    async def IssuerMergeRevocationRegistryDeltas(self, request, context):
        """ Issuer Merge Revocation Registry Deltas
        """
        try:
            rev_reg_delta_json, other_rev_reg_delta_json = get_value(request.RevRegDeltaJson), get_value(request.OtherRevRegDeltaJson)
            resp = await indy_anoncreds.issuer_merge_revocation_registry_deltas(rev_reg_delta_json, other_rev_reg_delta_json)
            return identitylayer_pb2.IssuerMergeRevocationRegistryDeltasResponse(MergedRevocationRegistryDelta=resp)
        except Exception as e:
            logger.error("Exception Occurred @IssuerMergeRevocationRegistryDeltas ------")
            logger.error(e)
            return identitylayer_pb2.IssuerMergeRevocationRegistryDeltasResponse(MergedRevocationRegistryDelta='')


    async def ProverCreateMasterSecret(self, request, context):
        """ Prover Create Master Secret
        """
        try:
            wallet_handle, master_secret_name = get_value(request.WalletHandle), get_value(request.MasterSecretName)
            resp = await indy_anoncreds.prover_create_master_secret(wallet_handle, master_secret_name)
            return identitylayer_pb2.ProverCreateMasterSecretResponse(GeneratedMasterSecretId=resp)
        except Exception as e:
            logger.error("Exception Occurred @ProverCreateMasterSecret ------")
            logger.error(e)
            return identitylayer_pb2.ProverCreateMasterSecretResponse(GeneratedMasterSecretId='')


    async def ProverCreateCredentialReq(self, request, context):
        """ Prover Create Credential Req
        """
        resp = None
        try:
            wallet_handle, prover_did, cred_offer_json, cred_def_json, master_secret_id = get_value(request.WaletHandle), get_value(request.ProverDid), get_value(request.CredOfferJSon), get_value(request.CredDefJson), get_value(request.MasterSecretId), 
            resp = await indy_anoncreds.prover_create_credential_req(wallet_handle, prover_did, cred_offer_json, cred_def_json, master_secret_id)
            cred_req_json = identitylayer_pb2.CredReqJsonMessage
            cred_req_json.ProverDid = resp[0]['ProverDid']
            cred_req_json.CredDefId = resp[0]['CredDefId']
            cred_req_json.BlindedMs = resp[0]['BlindedMs']
            cred_req_json.BlindedMsCorrectnessProof = resp[0]['BlindedMsCorrectnessProof']
            cred_req_json.Nonce = resp[0]['Nonce']
            return identitylayer_pb2.ProverCreateCredentialReqResponse(CredReqJson=cred_req_json, CredReqMetadataJson=resp[1])
        except Exception as e:
            logger.error("Exception Occurred @ProverCreateCredentialReq ------")
            logger.error(e)
            return identitylayer_pb2.ProverCreateCredentialReqResponse(CredReqJson=identitylayer_pb2.CredReqJsonMessage, CredReqMetadataJson='')


    async def ProverStoreCredential(self, request, context):
        """ Prover Store Credential
        """
        try:
            wallet_handle, cred_id, cred_req_metadata_json, cred_json, cred_def_json, rev_reg_def_json = \
            get_value(request.WalletHandle), get_value(request.CredId), get_value(request.CredReqMetadataJson), get_value(request.CredJson), get_value(request.CredDefJson), get_value(request.RevRegDefJson)
            resp = await indy_anoncreds.prover_store_credential(wallet_handle, cred_id, cred_req_metadata_json, cred_json, cred_def_json, rev_reg_def_json)
            return identitylayer_pb2.ProverStoreCredentialResponse(CredId=resp)
        except Exception as e:
            logger.error("Exception Occurred @ProverStoreCredential ------")
            logger.error(e)
            return identitylayer_pb2.ProverStoreCredentialResponse(CredId='')


    async def ProverGetCredential(self, request, context):
        """ Prover Get Credential
        """
        try:
            wallet_handle, cred_id = get_value(request.WalletHandle), get_value(request.CredId)
            resp = await indy_anoncreds.prover_get_credential(wallet_handle, cred_id)
            return identitylayer_pb2.ProverGetCredentialResponse(Referent=resp[0], Attrs=resp[1], SchemaId=resp[2], CredDefId=resp[3], RevRegId=resp[4], CredRevId=resp[5])
        except Exception as e:
            logger.error("Exception Occurred @ProverGetCredential ------")
            logger.error(e)
            return identitylayer_pb2.ProverGetCredentialResponse()


    async def ProverGetCredentials(self, request, context):
        """ Prover Get Credentials
        """
        try:
            wallet_handle, filter_json = get_value(request.WalletHandle), request.FilterJson
            filter_json = json.dumps({"schema_id":get_value(filter_json['SchemaId']), "schema_issuer_did":get_value(filter_json['SchemaIssuerDid']), "schema_name":get_value(filter_json['SchemaName']), \
                "schema_version":get_value(filter_json['SchemaVersion']), "issuer_did":get_value(filter_json['IssuerDid']), "cred_def_id":get_value(filter_json['CredDefId'])})
            resp = await indy_anoncreds.prover_get_credentials(wallet_handle, filter_json)
            return identitylayer_pb2.ProverGetCredentialsResponse(CredentialsJson=resp)
        except Exception as e:
            logger.error("Exception Occurred @ProverGetCredentials ------")
            logger.error(e)
            return identitylayer_pb2.ProverGetCredentialsResponse()


    async def ProverSeachCredentials(self, request, context):
        """ Prover Seach Credentials
        """
        try:
            wallet_handle, query_json = get_value(request.WalletHandle), get_value(request.QueryJson)
            resp = await indy_anoncreds.prover_search_credentials(wallet_handle, query_json)
            return identitylayer_pb2.ProverSeachCredentialsResponse(SearchHandle=resp[0], TotalCount=resp[1])
        except Exception as e:
            logger.error("Exception Occurred @ProverSeachCredentials ------")
            logger.error(e)
            return identitylayer_pb2.ProverSeachCredentialsResponse()


    async def ProverFetchCredentials(self, request, context):
        """ Prover Fetch Credentials
        """
        try:
            search_handle, count = get_value(request.SearchHandle), get_value(request.Count)
            resp = await indy_anoncreds.prover_fetch_credentials(search_handle, count)
            credentials_json = [identitylayer_pb2.CredentialsJsonMessage(Referent=el['referent'], Attrs=el['attrs'], SchemaID=el['schema_id'], CredDefId=el['cred_def_id'], RevRegId=el['rev_reg_id'], CredRevId=el['cred_rev_id']) for el in resp]
            return identitylayer_pb2.ProverFetchCredentialsResponse(CredentialsJson=credentials_json)
        except Exception as e:
            logger.error("Exception Occurred @ProverFetchCredentials ------")
            logger.error(e)
            return identitylayer_pb2.ProverFetchCredentialsResponse()


    async def ProverCloseCredentialsSearch(self, request, context):
        """ Prover Close Credentials Search
        """
        try:
            search_handle = get_value(request.SearchHandle)
            resp = await indy_anoncreds.prover_close_credentials_search(search_handle)
            return identitylayer_pb2.ProverCloseCredentialsSearchResponse(Resp=resp)
        except Exception as e:
            logger.error("Exception Occurred @ProverCloseCredentialsSearch ------")
            logger.error(e)
            return identitylayer_pb2.ProverCloseCredentialsSearchResponse()


    async def ProverGetCredentialsForProofReq(self, request, context):
        """ Prover Get Credentials For Proof Req
        """
        try:
            wallet_handle, proof_request_json = get_value(request.WalletHandle), request.ProofRequestJson
            proof_request_json = json.dumps({"name":proof_request_json['Name'], "version":proof_request_json['Version'], "nonce":proof_request_json['Nonce'], "requested_attributes":proof_request_json['RequestedAttributes'], "requested_predicates":proof_request_json['RequestedPredicates'], "non_revoked":proof_request_json['NonRevoked']})
            resp = await indy_anoncreds.prover_search_credentials_for_proof_req(wallet_handle, proof_request_json)
            return identitylayer_pb2.ProverGetCredentialsForProofReqResponse(RequestedAttrs=resp[0], RequestedPredicates=resp[1])
        except Exception as e:
            logger.error("Exception Occurred @ProverGetCredentialsForProofReq ------")
            logger.error(e)
            return identitylayer_pb2.ProverGetCredentialsForProofReqResponse()


    async def ProverSearchCredentialsForProofReq(self, request, context):
        """ Prover Search Credentials For Proof Req
        """
        try:
            wallet_handle, proof_request_json, extra_query_json = get_value(request.WalletHandle), request.ProofRequestJson, request.ExtraQueryJson
            proof_request_json = json.dumps({"name":get_value(proof_request_json['Name']), "version":get_value(proof_request_json['Version']), "nonce":get_value(proof_request_json['Nonce']), "requested_attributes":get_value(proof_request_json['RequestedAttributes']), "requested_predicates":get_value(proof_request_json['RequestedPredicates']), "non_revoked":proof_request_json['NonRevoked']})
            extra_query_json = json.dumps({"attr_referent":extra_query_json.AttrReferent ,"predicate_referent":extra_query_json.PredicateReferent})
            resp = await indy_anoncreds.prover_search_credentials_for_proof_req(wallet_handle, proof_request_json, extra_query_json)
            return identitylayer_pb2.ProverSearchCredentialsForProofReqResponse(SearchHandle=resp)
        except Exception as e:
            logger.error("Exception Occurred @ProverSearchCredentialsForProofReq------")
            logger.error(e)
            return identitylayer_pb2.ProverSearchCredentialsForProofReqResponse()


    async def ProverFetchCredentialsForProofReq(self, request, context):
        """ Prover Fetch Credentials For Proof Req
        """
        try:
            search_handle, item_referent, count = get_value(request.SearchHandle), get_value(request.ItemReference), get_value(request.Count)
            resp = await indy_anoncreds.prover_fetch_credentials_for_proof_req(search_handle, item_referent, count)
            credentials_json = [identitylayer_pb2.CredentialsGivenProofRequest(CredInfo=identitylayer_pb2.CredentialInfo(Referent=el['cred_info']['referent'], \
                Attrs=el['cred_info']['attrs'], SchemaId=el['cred_info']['schema_id'], CredDefId=el['cred_info']['cred_def_id'], RevRegId=el['cred_info']['rev_reg_id'], \
                CredRevId=el['cred_info']['cred_rev_id']),Interval=el["interval"]) for el in resp]
            return identitylayer_pb2.ProverFetchCredentialsForProofReqResponse(credentials_json)
        except Exception as e:
            logger.error("Exception Occurred @ProverFetchCredentialsForProofReq ------")
            logger.error(e)
            return identitylayer_pb2.ProverFetchCredentialsForProofReqResponse()


    async def ProverCloseCredentialsSearchForProofReq(self, request, context):
        """ Prover Close Credentials Search For Proof Req
        """
        try:
            search_handle = get_value(request.SearchHandle)
            resp = await indy_anoncreds.prover_close_credentials_search_for_proof_req(search_handle)
            return identitylayer_pb2.ProverCloseCredentialsSearchForProofReqResponse(Resp=resp)
        except Exception as e:
            logger.error("Exception Occurred @ProverCloseCredentialsSearchForProofReq ------")
            logger.error(e)
            return identitylayer_pb2.ProverCloseCredentialsSearchForProofReqResponse()


    async def ProverCreateProof(self, request, context):
        """ Prover Create Proof
        """
        try:
            wallet_handle, proof_req_json, requested_credentials_json, master_secret_name, schemas_json, credential_defs_json, \
            rev_states_json = get_value(request.WalletHandle), get_value(request.ProofReqJson), get_value(request.RequestedCredentialsJson), get_value(request.MasterSecretName), get_value(request.SchemasJson), get_value(request.CredentialDefsJson), get_value(request.RevStatesJson), 
            non_revoked = json.dumps({"from":proof_req_json.NonRevoInterval.From, "to":proof_req_json.NonRevoInterval.To})
            proof_req_json = json.dumps({"Name":proof_req_json.name, "Version":proof_req_json.version, "Nonce":proof_req_json.nonce, \
                "RequestedAttributes":proof_req_json.requested_attributes, "RequestedPredicates":proof_req_json.requested_predicates, \
                "non_revoked":non_revoked})
            requested_credentials_json = json.dumps({"self_attested_attributes":requested_credentials_json.SelfAttestedAttributes, \
                "requested_attributes":requested_credentials_json.RequestedAttributes, "requested_predicates":requested_credentials_json.RequestedPredicates})
            resp = await indy_anoncreds.prover_create_proof(wallet_handle, proof_req_json, requested_credentials_json, \
                master_secret_name, schemas_json, credential_defs_json, rev_states_json)
            return identitylayer_pb2.ProverCreateProofResponse(Requested=resp[0], Proof=resp[1], identifiers=resp[2])
        except Exception as e:
            logger.error("Exception Occurred @ProverCreateProof ------")
            logger.error(e)
            return identitylayer_pb2.ProverCreateProofResponse()


    async def VerifierVerifyProofRequest(self, request, context):
        """ Verifier Verify Proof
        """
        try:
            proof_request_json, proof_json, schemas_json, credential_defs_json, rev_reg_defs_json, rev_regs_json = request.ProofRequestJson, \
            get_value(request.ProofJson), get_value(request.SchemasJson), get_value(request.CredentialDefsJson), get_value(request.RevRegDefsJson), \
            get_value(request.RevRegJson)
            proof_request_json = json.dumps({"name": proof_request_json.Name, "version": proof_request_json.Version, "nonce": proof_request_json.Nonce, "requested_attributes": \
                proof_request_json.RequestedAttributes, "requested_predicates": proof_request_json.RequestedPredicates, "non_revoked": proof_request_json.NonRevoked})
            resp = await indy_anoncreds.verifier_verify_proof(proof_request_json, proof_json, schemas_json, credential_defs_json, rev_reg_defs_json, rev_regs_json)
            return identitylayer_pb2.VerifierVerifyProofResponse(Valid=resp)
        except Exception as e:
            logger.error("Exception Occurred @VerifierVerifyProofRequest ------")
            logger.error(e)
            return identitylayer_pb2.VerifierVerifyProofResponse()


    async def CreateRevocationState(self, request, context):
        """ Create Revocation State
        """
        try:
            blob_storage_reader_handle, rev_reg_def_json, rev_reg_delta_json, timestamp, cred_rev_id = \
            get_value(request.BlobStorageReaderHandle), get_value(request.RevRegDefJson), get_value(request.RevRegDeltaJson), get_value(request.Timestamp), get_value(request.CredRevId), 
            resp = await indy_anoncreds.create_revocation_state(blob_storage_reader_handle, rev_reg_def_json, rev_reg_delta_json, timestamp, cred_rev_id)
            return identitylayer_pb2.CreateRevocationStateResponse(RevReg=resp[0], Witness=resp[1], Timestamp=resp[2])
        except Exception as e:
            logger.error("Exception Occurred @CreateRevocationState ------")
            logger.error(e)
            return identitylayer_pb2.CreateRevocationStateResponse()

    async def UpdateRevocationState(self, request, context):
        """ Update Revocation State
        """
        try:
            blob_storage_reader_handle, rev_state_json, rev_reg_def_json, rev_reg_delta_json, timestamp, cred_rev_id = \
            get_value(request.BlobStorageReaderHandle), get_value(request.RevStateJson), get_value(request.RevRegDefJson), get_value(request.RevRegDeltaJson), get_value(request.Timestamp), get_value(request.CredRevId)
            resp = await indy_anoncreds.update_revocation_state(blob_storage_reader_handle, rev_state_json, rev_reg_def_json, rev_reg_delta_json, timestamp, cred_rev_id)
            return identitylayer_pb2.UpdateRevocationStateResponse(RevReg=resp[0], Witness=resp[0], Timestamp=resp[0])
        except Exception as e:
            logger.error("Exception Occurred @UpdateRevocationState ------")
            logger.error(e)
            return identitylayer_pb2.UpdateRevocationStateResponse()
