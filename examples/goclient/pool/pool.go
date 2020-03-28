package pool


import (
	"fmt"
	"context"
	"miu-client/identityLayer"
)

func NewPool(p identitylayer.PoolServiceClient, poolName, txnPath string) {
	//this function creates a new pool / we should check an error if pool exists.
	pcr, err := p.CreatePoolLedgerConfig(context.Background(), &identitylayer.CreatePoolLedgerConfigRequest{ConfigName: poolName, Config: &identitylayer.ConfigCreatePoolLedger{GensisTxn: txnPath}})
	if err != nil {
		fmt.Println("pool exist" + poolName)
	}
	fmt.Printf("Pool creation result %d \n", pcr.GetErrorCode())
}
func OpenPool(p identitylayer.PoolServiceClient, poolName string) int64 {
	ledger, err := p.OpenPoolLedger(context.Background(), &identitylayer.OpenPoolLedgerRequest{ConfigName: poolName, Config: &identitylayer.ConfigOpenLedger{Timeout: 20, ExtendedTimeour: 5, PreorderedNodes: []string{}}})
	if err != nil {
		panic(err)
	}
	fmt.Printf("Ledger Handle %d  Error %d \n", ledger.Handle, ledger.ErrorCode)
	return ledger.Handle
}
func ClosePool(p identitylayer.PoolServiceClient, poolHandle int64) {
	p.ClosePoolLedger(context.Background(), &identitylayer.ClosePoolLedgerRequest{Handle: poolHandle})
}
