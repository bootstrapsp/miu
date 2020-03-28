package issuer

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"miu-client/grpcConn"
	"miu-client/identityLayer"
	"miu-client/models"
	"github.com/lucsky/cuid"
	"strconv"
	"time"
	"context"
)

type CredConfig struct {
	CredDefId   string `mapstructure:"cred_def_id"`
	RevRecId    string `mapstructure:"rev_rec_id"`
	RevocRegDef string `mapstructure:"rev_reg_def"`
	CredDefJson string `mapstructure:"cred_def_json"`
	SchemaID    string `mapstructure:"schema_id"`
	Schema      string `mapstructure:"schema"`
}

func GetParsedSchema(ledgerService identitylayer.LedgerServiceClient,poolHandler int64, submitterDID string, schemaId string) (*identitylayer.ParseGetSchemaResponseRs, error) {
	get_schema_request, err := ledgerService.BuildGetSchemaRequest(context.Background(), &identitylayer.BuildGetSchemaRequestRq{
		SubmitterDid: submitterDID,
		Id_:          schemaId,
	})
	if err != nil {
		return nil, err

	}

	resp1 := waitUntilApplied(poolHandler, get_schema_request.Resp, func(res string) bool {
		var r models.SubmitResponseRich
		respBytes := []byte(res)
		err = json.NewDecoder(bytes.NewReader(respBytes)).Decode(&r)
		if err != nil {
			panic(err)
		}
		if r.Result.SeqNo == 0 {
			return false
		}
		return true
	}, ledgerService)

	fmt.Printf("Ensure Request Applied  | Success = %t\n", resp1 != "")

	parsedResp, err := ledgerService.ParseGetSchemaResponse(context.Background(), &identitylayer.ParseGetSchemaResponseRq{
		GetSchemaResponse: resp1,
	})
	if err != nil {
		return nil, err
	}
	return parsedResp, nil
}

func GetParsedCredentialDefinition(ledgerService identitylayer.LedgerServiceClient,poolHandler int64, submitterDID string, credDefId string) (*identitylayer.ParseGetCredDefResponseRs, error) {
	credGetDefReq, err := ledgerService.BuildGetCredDefRequest(context.Background(), &identitylayer.BuildGetCredDefRequestRq{
		SubmitterDid: submitterDID,
		Id_:          credDefId,
	})
	if err != nil {
		return nil, err
	}

	resp2 := waitUntilApplied(poolHandler, credGetDefReq.Resp, func(res string) bool {
		var r models.SubmitResponseRich
		respBytes := []byte(res)
		err = json.NewDecoder(bytes.NewReader(respBytes)).Decode(&r)
		if err != nil {
			panic(err)
		}
		if r.Result.SeqNo == 0 {
			return false
		}
		return true
	}, ledgerService)

	parsedCredResp, err := ledgerService.ParseGetCredDefResponse(context.Background(), &identitylayer.ParseGetCredDefResponseRq{
		GetCredDefResponse: resp2,
	})
	if err != nil {
		return nil, err
	}
	return parsedCredResp, nil
}

func GetParsedRevocationRegistryDefinition(ledgerService identitylayer.LedgerServiceClient,poolHandler int64, submitterDID string, revRecId string) (*identitylayer.ParseGetRevocRegDefResponseRs, error) {
	get_revoc_reg_def_request, err := ledgerService.BuildGetRevocRegDefRequest(context.Background(), &identitylayer.BuildGetRevocRegDefRequestRq{
		SubmitterDid: submitterDID,
		RevRegDefId:  revRecId,
	})
	if err != nil {
		return nil, err
	}

	get_revoc_reg_def_response := waitUntilApplied(poolHandler, get_revoc_reg_def_request.Resp, func(res string) bool {
		var r models.SubmitResponseRich
		respBytes := []byte(res)
		err = json.NewDecoder(bytes.NewReader(respBytes)).Decode(&r)
		if err != nil {
			panic(err)
		}
		if r.Result.SeqNo == 0 {
			return false
		}
		return true
	}, ledgerService)

	parsedRevocRegReqDef, err := ledgerService.ParseGetRevocRegDefResponse(context.Background(), &identitylayer.ParseGetRevocRegDefResponseRq{
		GetRevocRefDefResponse: get_revoc_reg_def_response,
	})
	if err != nil {
		return nil, err
	}
	return parsedRevocRegReqDef, nil
}

func GetParsedRevocDelta(ledgerService identitylayer.LedgerServiceClient,poolHandler int64, submitterDID string, revRecId string, timeFrom int64, timeTo int64) (*identitylayer.ParseGetRevocRegDeltaResponseRs, error) {

	get_cred_def_request, err := ledgerService.BuildGetRevocRegDeltaRequest(context.Background(), &identitylayer.BuildGetRevocRegDeltaRequestRq{
		SubmiterDid:   submitterDID,
		To:            timeTo,
		From_:         timeFrom,
		RevocRegDefId: revRecId,
	})
	if err != nil {
		return nil, err
	}

	get_cred_def_response := waitUntilApplied(poolHandler, get_cred_def_request.Resp, func(res string) bool {
		var r models.SubmitResponseRich
		respBytes := []byte(res)
		err = json.NewDecoder(bytes.NewReader(respBytes)).Decode(&r)
		if err != nil {
			panic(err)
		}
		if r.Result.SeqNo == 0 {
			return false
		}
		return true
	}, ledgerService)

	parsedDeltaResponse, err := ledgerService.ParseGetRevocRegDeltaResponse(context.Background(), &identitylayer.ParseGetRevocRegDeltaResponseRq{
		GetRevocRegDeltaResponse: get_cred_def_response,
	})
	if err != nil {
		return nil, err
	}

	return parsedDeltaResponse, nil
}

func GetParsedRevocationRegistry(ledgerService identitylayer.LedgerServiceClient,poolHandler int64, submitterDID string, revRecId string, timestamp int64) (*identitylayer.ParseGetRevocRegResponseRs, error) {

	revocRegReq, err := ledgerService.BuildGetRevocRegRequest(context.Background(), &identitylayer.BuildGetRevocRegRequestRq{
		SubmitterDid:  submitterDID,
		RevocRegDefId: revRecId,
		Timestamp:     strconv.FormatUint(uint64(timestamp), 10),
	})
	if err != nil {
		return nil, err
	}
	//fmt.Printf("BuildGetRevocRegRequest resp %+v \n", revocRegReq)

	resp3 := waitUntilApplied(poolHandler, revocRegReq.Resp, func(res string) bool {
		var r models.SubmitResponseRich
		respBytes := []byte(res)
		err = json.NewDecoder(bytes.NewReader(respBytes)).Decode(&r)
		if err != nil {
			panic(err)
		}
		if r.Result.SeqNo == 0 {
			return false
		}
		return true
	}, ledgerService)
	//fmt.Println("response after waiting \n", resp3)
	parsedRevocRegReq, err := ledgerService.ParseGetRevocRegResponse(context.Background(), &identitylayer.ParseGetRevocRegResponseRq{
		GetRevocRegResponse: resp3,
	})
	if err != nil {
		return nil, err
	}
	return parsedRevocRegReq, nil
}

func RevokeCredential(anonCredService identitylayer.AnoncredsServiceClient, ledgerService identitylayer.LedgerServiceClient, poolHandler int64, walletHandler int64, submitterDID string, revRecId string, credRevRecId string, storageHandle int64) error {

	irc, err := anonCredService.IssuerRevokeCredential(context.Background(), &identitylayer.IssuerRevokeCredentialRequest{
		WalletHandle:            walletHandler,
		BlobStorageReaderHandle: storageHandle,
		RevRegId:                revRecId,
		CredRevocId:             credRevRecId,
	})
	if err != nil {
		return err
	}
	fmt.Printf("STEP 9 : IssuerRevokeCredential | Confirmed = %t\n", irc.RevocationRegistryDeltaJson != "")

	/*

	 # Issuer posts Revocation Registry Entry to Ledger

	*/

	entryReq, err := ledgerService.BuildRevocRegEntryRequest(context.Background(), &identitylayer.BuildRevocRegEntryRequestRq{
		SubmitterDid:  submitterDID,
		RevocRegDefId: revRecId,
		RevDefType:    "CL_ACCUM",
		Value:         irc.RevocationRegistryDeltaJson,
	})
	if err != nil {
		return err
	}

	submitResp, err := ledgerService.SignAndSubmitRequest(context.Background(), &identitylayer.SignAndSubmitRequestRq{
		PoolHandle:   poolHandler,
		WalletHandle: walletHandler,
		SubmitterDid: submitterDID,
		RequestJson:  entryReq.Resp,
	})
	if err != nil {
		return err
	}
	fmt.Printf("STEP 9 : Revoc Entry Request created | Confirmed = %t\n", submitResp.Resp != "")

	return nil
}

func CreateProofRequest(anonCredService identitylayer.AnoncredsServiceClient, timeFrom, timeTo int64) (*identitylayer.ProofReqJsonMessage, error) {




	responseGen, err := anonCredService.GenerateNonce(context.Background(), &identitylayer.GenerateNonceRequest{})
	if err != nil {
		return nil, err
	}

	var proofReqJson identitylayer.ProofReqJsonMessage
	proofReqJson.Version = "1.0"
	proofReqJson.Name = "proof_req_1"
	proofReqJson.Nonce = responseGen.Nonce
	proofReqJson.NonRevoInterval = &identitylayer.NonRevocIntervalMessage{From: timeFrom, To: timeTo}

	//atttr map
	//attr := make(map[string])

	proofReqJson.RequestedAttributes = `{ "attr1_referent": {"name":"name"}}`
	proofReqJson.RequestedPredicates = `{ "predicate1_referent": { "name": "age", "p_type": ">=", "p_value": 18}}`
	return &proofReqJson, nil

}

func SetupIssuer(target string, poolHandler int64, walletHandler int64, submitterDID string) (*CredConfig, error) {



	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	ledgerService := identitylayer.NewLedgerServiceClient(gconn)
	anonCredService := identitylayer.NewAnoncredsServiceClient(gconn)
	blobStorageClient := identitylayer.NewBlobStorageServiceClient(gconn)


	//r := rand.New(rand.NewSource(99)
	schemaName := "schema-" + cuid.New()

	/*
		create schema
	*/

	//schema creation request
	isc, err := anonCredService.IssuerCreateSchema(context.Background(), &identitylayer.IssuerCreateSchemaRequest{
		IssuerDid: submitterDID,
		Name:      schemaName,
		Version:   "1.0",
		Attrs:     `["name", "age", "sex", "height"]`,
	})
	if err != nil {
		return nil, err
	}
	fmt.Printf("STEP 1 :  Schema Created | Success = %t\n", isc.SchemaId != "")

	/*
		Issuer Posts schema
	*/
	bsr, err := ledgerService.BuildSchemaRequest(context.Background(), &identitylayer.BuildSchemaRequestRq{
		SubmitterDid: submitterDID,
		Data:         isc.SchemaJson,
	})
	if err != nil {
		return nil, err

	}

	submitResp1, err := ledgerService.SignAndSubmitRequest(context.Background(), &identitylayer.SignAndSubmitRequestRq{
		WalletHandle: walletHandler,
		SubmitterDid: submitterDID,
		RequestJson:  bsr.Resp,
		PoolHandle:   poolHandler,
	})

	if err != nil {
		return nil, err

	}
	fmt.Printf("STEP 2 :  Schema Request sent | Success = %t\n", submitResp1.Resp != "")

	parsedResp, err := GetParsedSchema(ledgerService,poolHandler, submitterDID, isc.SchemaId)

	if err != nil {
		return nil, err

	}
	fmt.Printf("STEP 4 :  Schema Parsed Response  | Success = %t\n", parsedResp.Id != "")

	/*
		    Issuer Creates credential Definition for Schema
	*/

	credDefResp, err := anonCredService.IssuerCreateAndStoreCredentialDef(context.Background(), &identitylayer.IssuerCreateAndStoreCredentialDefRequest{
		WalletHandle:  walletHandler,
		IssuerDid:     submitterDID,
		SchemaJson:    parsedResp.SchemaJson,
		Tag:           "tag1",
		SignatureType: "CL",
		ConfigJson:    `{ "support_revocation": true }`,
	})
	if err != nil {
		return nil, err
	}
	fmt.Printf("STEP 5 :  Credential definition created  | Success = %t\n", credDefResp.CredDefId != "")

	/*
		Issuer Posts Credential Definition
	*/

	credReq, err := ledgerService.BuildCredDefRequest(context.Background(), &identitylayer.BuildCredDefRequestRq{
		SubmitterDid: submitterDID,
		Data:         credDefResp.CredDefJson,
	})
	if err != nil {
		return nil, err
	}

	submitResp, err := ledgerService.SignAndSubmitRequest(context.Background(), &identitylayer.SignAndSubmitRequestRq{
		PoolHandle:   poolHandler,
		WalletHandle: walletHandler,
		SubmitterDid: submitterDID,
		RequestJson:  credReq.Resp,
	})

	if err != nil {
		return nil, err
	}
	fmt.Printf("STEP 5 :  Credential definition sent  | Confirmed = %t\n", submitResp.Resp != "")

	/*
			Create revocation registry
		    Issuer Creates Revocation Registry
	*/
	//open storage
	op, err := blobStorageClient.OpenWriter(context.Background(), &identitylayer.OpenWriterRequest{
		Type_: "default",
		Config: `{
    "base_dir": "/home/app/tails",
    "uri_pattern": ""
  }`,
	})
	if err != nil {
		return nil, err
	}

	// Revoc Reg Def
	csrevoc, err := anonCredService.IssuerCreateAndStoreRevocReg(context.Background(), &identitylayer.IssuerCreateAndStoreRevocRegRequest{
		WalletHandle:      walletHandler,
		IssuerDid:         submitterDID,
		Tag:               "tag1",
		CredDefId:         credDefResp.CredDefId,
		ConfigJSon:        `{ "max_cred_num": 5 , "issuance_type":"ISSUANCE_ON_DEMAND" }`,
		TailsWriterHandle: op.Res,
	})
	if err != nil {
		return nil, err
	}
	fmt.Printf("STEP 7 :  Revoc registry definition created | Success = %t\n", csrevoc.RevocRegDefJson != "")

	/*
	 Issuer posts Revocation Registry Definition to Ledger
	*/
	buildRevocRes, err := ledgerService.BuildRevocRegDefRequest(context.Background(), &identitylayer.BuildRevocRegDefRequestRq{
		SubmitterDid: submitterDID,
		Data:         csrevoc.RevocRegDefJson,
	})
	if err != nil {
		return nil, err
	}

	submitResp, err = ledgerService.SignAndSubmitRequest(context.Background(), &identitylayer.SignAndSubmitRequestRq{
		PoolHandle:   poolHandler,
		WalletHandle: walletHandler,
		SubmitterDid: submitterDID,
		RequestJson:  buildRevocRes.Resp,
	})
	if err != nil {
		return nil, err
	}
	fmt.Printf("STEP 7 :  Revoc registry definition created | Confirmed = %t\n", submitResp.Resp != "")

	// Revoc Reg Entry

	/*

	 # Issuer posts Revocation Registry Entry to Ledger
	*/

	entryReq, err := ledgerService.BuildRevocRegEntryRequest(context.Background(), &identitylayer.BuildRevocRegEntryRequestRq{
		SubmitterDid:  submitterDID,
		RevocRegDefId: csrevoc.RevocRegId,
		RevDefType:    "CL_ACCUM",
		Value:         csrevoc.RevocRegEntryJson,
	})
	if err != nil {
		return nil, err
	}

	submitResp, err = ledgerService.SignAndSubmitRequest(context.Background(), &identitylayer.SignAndSubmitRequestRq{
		PoolHandle:   poolHandler,
		WalletHandle: walletHandler,
		SubmitterDid: submitterDID,
		RequestJson:  entryReq.Resp,
	})
	if err != nil {
		return nil, err
	}
	fmt.Printf("STEP 8 : Revoc Entry Request created | Confirmed = %t\n", submitResp.Resp != "")

	return &CredConfig{CredDefId: credDefResp.CredDefId, RevRecId: csrevoc.RevocRegId, RevocRegDef: csrevoc.RevocRegDefJson, CredDefJson: credDefResp.CredDefJson, Schema: parsedResp.SchemaJson, SchemaID: parsedResp.Id}, nil
}

func IssueCredentialAndProof( target string, poolHandler int64, walletHandler int64,credDefId string, proverDID string, revRecId string, credId string, schemaId string) error {

	// prover create master key


	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	ledgerService := identitylayer.NewLedgerServiceClient(gconn)
	anonCredService := identitylayer.NewAnoncredsServiceClient(gconn)
	blobStorageClient := identitylayer.NewBlobStorageServiceClient(gconn)



	/*


		Create Prover master key

		Prover Creates Master Secret

	*/

	masterSecretId := cuid.New()
	pcms, err := anonCredService.ProverCreateMasterSecret(context.Background(), &identitylayer.ProverCreateMasterSecretRequest{
		WalletHandle:     walletHandler,
		MasterSecretName: masterSecretId,
	})
	if err != nil {
		return err
	}

	fmt.Printf("STEP 1 :  Master key created | Success = %t\n", pcms.GeneratedMasterSecretId != "")

	/*

		create credential offer

	*/

	icco, err := anonCredService.IssuerCreateCredentialOffer(context.Background(), &identitylayer.IssuerCreateCredentialOfferRequest{
		WalletHandle: walletHandler,
		CredDefId:    credDefId,
	})
	if err != nil {
		return err
	}

	//fmt.Printf("IssuerCreateCredentialOffer resp %+v \n", icco)
	fmt.Printf("STEP 2 :  Credential Offer created | Success = %t\n", icco.Resp != "")

	credOfferjson := icco.Resp

	var credOffer map[string]interface{}

	err = json.Unmarshal([]byte(credOfferjson), &credOffer)

	if err != nil {
		return err
	}

	cred_def_id := credOffer["cred_def_id"].(string)
	fmt.Println(cred_def_id)

	/*

		Prover Gets Credential Definition from Ledger
	*/

	parsedCredResp, err := GetParsedCredentialDefinition(ledgerService,poolHandler, proverDID, credDefId)
	if err != nil {
		return err
	}
	fmt.Printf("STEP 2 :  Parsed cred definition  | Success = %t\n", parsedCredResp.CredentialDefinitionJson != "")

	cred_def_json := parsedCredResp.CredentialDefinitionJson
	cred_def_id = parsedCredResp.CredentialDefinitionId

	/*

		    Create request for credential
			 #  Prover create credential Request
	*/

	pccr, err := anonCredService.ProverCreateCredentialReq(context.Background(), &identitylayer.ProverCreateCredentialReqRequest{
		WaletHandle:    walletHandler,
		CredDefJson:    cred_def_json,
		CredOfferJSon:  credOfferjson,
		MasterSecretId: masterSecretId,
		ProverDid:      proverDID,
	})
	if err != nil {
		return err
	}
	//fmt.Printf("ProverCreateCredentialReq resp %+v \n", pccr)

	fmt.Printf("STEP 3 :  Credential Request created | Success = %t\n", pccr.CredReqJson != "")

	// Issuer open Tails reader

	/*
		Issue credential
	*/

	or, err := blobStorageClient.OpenReader(context.Background(), &identitylayer.OpenReaderRequest{
		Type_: "default",
		Config: `{
    "base_dir": "/home/app/tails",
    "uri_pattern": ""
  }`,
	})

	if err != nil {
		return err
	}


	cred_values_json := `{
		"sex": {
			"raw": "male", "encoded": "5944657099558967239210949258394887428692050081607692519917050011144233115103"},
		"name": {"raw": "Alex", "encoded": "1139481716457488690172217916278103335"},
		"height": {"raw": "175", "encoded": "175"},
		"age": {"raw": "28", "encoded": "28"}
	}`

	icc, err := anonCredService.IssuerCreateCredential(context.Background(), &identitylayer.IssuerCreateCredentialRequest{
		WalletHandle:            walletHandler,
		CredOfferJson:           credOfferjson,
		CredValuesJson:          cred_values_json,
		CredReqJson:             pccr.CredReqJson,
		BlobStorageReaderHandle: or.Res,
		RevRegId:                revRecId,
	})
	if err != nil {
		return err
	}
	//fmt.Printf("IssuerCreateCredential resp %+v \n", icc)

	fmt.Printf("STEP 4 :  Issuer Created Credential | Success = %t\n", icc.CredJson != "")

	/*
		# Issuer Posts Revocation Registry Delta to Ledger

	*/

	revoc_reg_entry_request, err := ledgerService.BuildRevocRegEntryRequest(context.Background(), &identitylayer.BuildRevocRegEntryRequestRq{
		SubmitterDid:  proverDID,
		RevDefType:    "CL_ACCUM",
		RevocRegDefId: revRecId,
		Value:         icc.RevocRegDeltaJson,
	})
	if err != nil {
		return err
	}
	revoc_reg_entry_result, err := ledgerService.SignAndSubmitRequest(context.Background(), &identitylayer.SignAndSubmitRequestRq{
		SubmitterDid: proverDID,
		PoolHandle:   poolHandler,
		WalletHandle: walletHandler,
		RequestJson:  revoc_reg_entry_request.Resp,
	})
	if err != nil {
		return err
	}

	fmt.Printf("STEP 5 :  Posts Revocation Registry Delta to Ledger | Success = %t\n", revoc_reg_entry_result.Resp != "")

	/*

		# Prover Gets RevocationRegistryDefinition


	*/
	parsedRevocRegReqDef, err := GetParsedRevocationRegistryDefinition(ledgerService,poolHandler, proverDID, revRecId)
	if err != nil {
		return err
	}
	fmt.Printf("STEP 5 : Parsed Revoc Def Response  | Success = %t\n", parsedRevocRegReqDef.RevocationJson != "")

	/*

		store credential

	*/

	//    cred_id = 'cred_1_id'
	// Prover process and store credential
	psc, err := anonCredService.ProverStoreCredential(context.Background(), &identitylayer.ProverStoreCredentialRequest{
		WalletHandle:        walletHandler,
		CredId:              credId,
		CredJson:            icc.CredJson,
		CredDefJson:         cred_def_json,
		RevRegDefJson:       parsedRevocRegReqDef.RevocationJson,
		CredReqMetadataJson: pccr.CredReqMetadataJson,
	})
	if err != nil {
		return err
	}
	//fmt.Printf("ProverStoreCredential resp %+v \n", psc)
	fmt.Printf("STEP 5 :  Prover Store Credential | Success = %t\n", psc.CredId != "")

	time.Sleep(2 * time.Second)


	timeTo := time.Now().Unix()


	proofReqJson, err := CreateProofRequest(anonCredService, 0, timeTo)
	if err != nil {
		return err
	}

	proofSearchrequest, err := anonCredService.ProverSearchCredentialsForProofReq(context.Background(), &identitylayer.ProverSearchCredentialsForProofReqRequest{
		WalletHandle:     walletHandler,
		ProofRequestJson: proofReqJson,
	})
	if err != nil {
		return err
	}
	proofFetchrequest, err := anonCredService.ProverFetchCredentialsForProofReq(context.Background(), &identitylayer.ProverFetchCredentialsForProofReqRequest{
		SearchHandle:  proofSearchrequest.SearchHandle,
		ItemReference: "attr1_referent",
		Count:         10,
	})
	if err != nil {
		return err
	}
	proofSearchClose, err := anonCredService.ProverCloseCredentialsSearchForProofReq(context.Background(), &identitylayer.ProverCloseCredentialsSearchForProofReqRequest{
		SearchHandle: proofSearchrequest.SearchHandle,
	})
	if err != nil {
		return err
	}
	fmt.Println(proofSearchClose.Resp)

	var credObject map[string]map[string]interface{}
	//parse

	var fetchResp []map[string]map[string]interface{}

	err = json.Unmarshal([]byte(proofFetchrequest.RespJson), &fetchResp)
	if err != nil {
		return err
	}
	for _, r := range fetchResp {
		if r["cred_info"]["referent"] == credId {
			credObject = r
		}
	}

	fmt.Println(credObject["cred_info"]["referent"])

	fmt.Printf("STEP 6 :  Prover Search CredentialsForProofReq| Success = %t\n", credObject != nil)

	credInfo := credObject["cred_info"]

	/*
		# Prover Gets RevocationRegistryDelta from Ledger
	*/
	parsedDeltaResponse, err := GetParsedRevocDelta(ledgerService,poolHandler, proverDID, revRecId, 0, timeTo)
	if err != nil {
		return err
	}

	fmt.Printf("STEP 6.1 :  Parsed Revoc Delta   | Success = %t\n", parsedDeltaResponse.Json != "")

	/*
		# Prover Creates Revocation State
				create revocation state
	*/
	revocationReq, err := anonCredService.CreateRevocationState(context.Background(), &identitylayer.CreateRevocationStateRequest{
		BlobStorageReaderHandle: or.Res,
		RevRegDeltaJson:         parsedDeltaResponse.Json,
		RevRegDefJson:           parsedRevocRegReqDef.RevocationJson,
		CredRevId:               credInfo["cred_rev_id"].(string),
		Timestamp:               parsedDeltaResponse.Timestamp,
	})
	if err != nil {
		return err
	}
	//fmt.Printf("CreateRevocationState resp %+v \n", res)
	fmt.Printf("STEP 7 :  Prover State  Created | Success = %t\n", revocationReq.RespJson != "")

	/*
		create proof
	*/

	parsedResp, err := GetParsedSchema(ledgerService,poolHandler, proverDID, schemaId)
	if err != nil {
		return err
	}
	fmt.Printf("STEP 7 :  Schema Parsed Response  | Success = %t\n", parsedResp.SchemaJson != "")

	var schemas = make(map[string]interface{})
	var schemaInterface interface{}
	err = json.Unmarshal([]byte(parsedResp.SchemaJson), &schemaInterface)
	if err != nil {
		return err
	}
	schemas[parsedResp.Id] = schemaInterface
	sb, _ := json.Marshal(schemas)
	schemasJson := string(sb)

	var credentialDefs = make(map[string]interface{})
	var credDefInterface interface{}
	err = json.Unmarshal([]byte(cred_def_json), &credDefInterface)
	if err != nil {
		return err
	}
	credentialDefs[cred_def_id] = credDefInterface
	cd, _ := json.Marshal(credentialDefs)
	credDefsJson := string(cd)

	var revocStates = make(map[string]map[int64]interface{})
	revocStates[parsedDeltaResponse.Id] = make(map[int64]interface{})

	//unmarshal revJSON
	var revJsonInterface interface{}
	err = json.Unmarshal([]byte(revocationReq.RespJson), &revJsonInterface)
	if err != nil {
		return err
	}
	revocStates[revRecId][parsedDeltaResponse.Timestamp] = revJsonInterface

	rs, _ := json.Marshal(revocStates)
	rsJson := string(rs)

	//search credential for proof request ?

	var reqCredJson identitylayer.RequestedCredentialsJsonMessage
	reqCredJson.SelfAttestedAttributes = `{}`
	reqCredJson.RequestedAttributes = `{ "attr1_referent": { "cred_id": "` + credInfo["referent"].(string) + `", "revealed": true , "timestamp" : ` + strconv.FormatUint(uint64(parsedDeltaResponse.Timestamp), 10) + `} }`
	reqCredJson.RequestedPredicates = `{ "predicate1_referent": { "cred_id":"` + credInfo["referent"].(string) + `" , "timestamp" : ` + strconv.FormatUint(uint64(parsedDeltaResponse.Timestamp), 10) + `} }`

	pcp, err := anonCredService.ProverCreateProof(context.Background(), &identitylayer.ProverCreateProofRequest{
		WalletHandle:             walletHandler,
		ProofReqJson:             proofReqJson,
		RevStatesJson:            rsJson,
		MasterSecretName:         masterSecretId,
		CredentialDefsJson:       credDefsJson,
		RequestedCredentialsJson: &reqCredJson,
		SchemasJson:              schemasJson,
	})
	if err != nil {
		return err
	}

	fmt.Printf("STEP 8 :  Prover Created  proof | Success = %t\n", pcp.ProofResp != "")

	//verify proof

	/*

		verify proof
	*/

	var revRegDefs = make(map[string]interface{})
	var revRegDefJsonInterface interface{}
	err = json.Unmarshal([]byte(parsedRevocRegReqDef.RevocationJson), &revRegDefJsonInterface)
	if err != nil {
		return err
	}
	revRegDefs[revRecId] = revRegDefJsonInterface
	rb, _ := json.Marshal(revRegDefs)
	revRegDefsJson := string(rb)

	// Verifier Gets Revocation Registry from Ledger

	parsedRevocRegReq, err := GetParsedRevocationRegistry(ledgerService,poolHandler, proverDID, revRecId, parsedDeltaResponse.Timestamp)
	if err != nil {
		return err
	}
	//fmt.Printf("ParseGetRevocRegResponse resp %+v \n", parsedRevocRegReq)

	var revRegJsons = make(map[string]map[int64]interface{})
	revRegJsons[parsedRevocRegReq.Id] = make(map[int64]interface{})
	var revRegJsonInterface interface{}
	err = json.Unmarshal([]byte(parsedRevocRegReq.Json), &revRegJsonInterface)
	if err != nil {
		return err
	}
	revRegJsons[revRecId][parsedRevocRegReq.Timestamp] = revRegJsonInterface
	rd, _ := json.Marshal(revRegJsons)
	revRegJsonsJson := string(rd)

	if err != nil {
		return err
	}
	vvprf, err := anonCredService.VerifierVerifyProof(context.Background(), &identitylayer.VerifierVerifyProofRequest{
		ProofJson:          pcp.ProofResp,
		ProofRequestJson:   proofReqJson,
		RevRegDefsJson:     revRegDefsJson,
		RevRegJson:         revRegJsonsJson,
		CredentialDefsJson: credDefsJson,
		SchemasJson:        schemasJson,
	})
	if err != nil {
		return err
	}
	fmt.Printf("STEP 9 :   Verified  proof | Success = %t\n", vvprf.Valid)


	return nil
}

type Credential struct {
	Referent  string
	Attrs     string
	SchemaId  string
	CredDefId string
	RevRegId  string
	CredRevId string
}

type checkFunc func(string) bool

func waitUntilApplied(ph int64, req string, cond checkFunc, c identitylayer.LedgerServiceClient) string {
	for i := 0; i < 5; i++ {
		res, err := c.SubmitRequest(context.Background(), &identitylayer.SubmitRequestRq{
			PoolHandle:  ph,
			RequestJson: req,
		})
		if err != nil {
			panic(err)
		}
		if cond(res.Resp) {
			return res.Resp
		}
		time.Sleep(10 * time.Second)
	}
	return ""
}
