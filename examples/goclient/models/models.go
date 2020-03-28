
package models

type SumbitResponse struct {
	Op     string `json:"op"`
	Result Result `json:"result"`
}
type Data struct {
	Alias  string `json:"alias"`
	Dest   string `json:"dest"`
	Verkey string `json:"verkey"`
}
type Metadata struct {
	From          string `json:"from"`
	ReqID         int64  `json:"reqId"`
	Digest        string `json:"digest"`
	PayloadDigest string `json:"payloadDigest"`
}
type Txn struct {
	Type            string   `json:"type"`
	Data            Data     `json:"data"`
	ProtocolVersion int      `json:"protocolVersion"`
	Metadata        Metadata `json:"metadata"`
}
type TxnMetadata struct {
	TxnID   string `json:"txnId"`
	TxnTime int    `json:"txnTime"`
	SeqNo   int    `json:"seqNo"`
}
type Values struct {
	From  string `json:"from"`
	Value string `json:"value"`
}
type ReqSignature struct {
	Type   string   `json:"type"`
	Values []Values `json:"values"`
}
type Result struct {
	Txn          Txn          `json:"txn"`
	TxnMetadata  TxnMetadata  `json:"txnMetadata"`
	ReqSignature ReqSignature `json:"reqSignature"`
	Ver          string       `json:"ver"`
	RootHash     string       `json:"rootHash"`
	AuditPath    []string     `json:"auditPath"`
}

type ByuildNymResponse struct {
	ReqID           int64     `json:"reqId"`
	Identifier      string    `json:"identifier"`
	Operation       Operation `json:"operation"`
	ProtocolVersion int       `json:"protocolVersion"`
}
type Operation struct {
	Type   string `json:"type"`
	Dest   string `json:"dest"`
	Verkey string `json:"verkey"`
	Alias  string `json:"alias"`
}

type SignNymResponse struct {
	Identifier      string    `json:"identifier"`
	Operation       Operation `json:"operation"`
	ProtocolVersion int       `json:"protocolVersion"`
	ReqID           int64     `json:"reqId"`
	Signature       string    `json:"signature"`
}
type MetaResponse struct {
	SeqNo   int `json:"seqNo"`
	TxnTime int `json:"txnTime"`
}
type ErrorResponse struct {
	Op         string `json:"op"`
	Identifier string `json:"identifier"`
	ReqID      int64  `json:"reqId"`
	Reason     string `json:"reason"`
}

type GetIdentityResponse struct {
	Op     string    `json:"op"`
	Result GetResult `json:"result"`
}
type Value struct {
	LedgerID          int    `json:"ledger_id"`
	PoolStateRootHash string `json:"pool_state_root_hash"`
	StateRootHash     string `json:"state_root_hash"`
	Timestamp         int    `json:"timestamp"`
	TxnRootHash       string `json:"txn_root_hash"`
}
type MultiSignature struct {
	Signature    string   `json:"signature"`
	Participants []string `json:"participants"`
	Value        Value    `json:"value"`
}
type StateProof struct {
	RootHash       string         `json:"root_hash"`
	MultiSignature MultiSignature `json:"multi_signature"`
	ProofNodes     string         `json:"proof_nodes"`
}
type GetResult struct {
	Type       string     `json:"type"`
	Dest       string     `json:"dest"`
	Data       string     `json:"data"`
	Identifier string     `json:"identifier"`
	ReqID      int64      `json:"reqId"`
	SeqNo      int        `json:"seqNo"`
	TxnTime    int        `json:"txnTime"`
	StateProof StateProof `json:"state_proof"`
}
type IdentityInfo struct {
	Dest       string      `json:"dest"`
	Identifier string      `json:"identifier"`
	Role       interface{} `json:"role"`
	SeqNo      int         `json:"seqNo"`
	TxnTime    int         `json:"txnTime"`
	Verkey     string      `json:"verkey"`
}

type SubmitResponseRich struct {
	Op     string `json:"op"`
	Result struct {
		Type string `json:"type"`
		Dest string `json:"dest"`
		Data struct {
			AttrNames []string `json:"attr_names"`
			Name      string   `json:"name"`
			Version   string   `json:"version"`
		} `json:"data"`
		Identifier string `json:"identifier"`
		ReqID      int64  `json:"reqId"`
		SeqNo      int    `json:"seqNo"`
		TxnTime    int    `json:"txnTime"`
		StateProof struct {
			RootHash       string `json:"root_hash"`
			MultiSignature struct {
				Signature    string   `json:"signature"`
				Participants []string `json:"participants"`
				Value        struct {
					LedgerID          int    `json:"ledger_id"`
					PoolStateRootHash string `json:"pool_state_root_hash"`
					StateRootHash     string `json:"state_root_hash"`
					Timestamp         int    `json:"timestamp"`
					TxnRootHash       string `json:"txn_root_hash"`
				} `json:"value"`
			} `json:"multi_signature"`
			ProofNodes string `json:"proof_nodes"`
		} `json:"state_proof"`
	} `json:"result"`
}
