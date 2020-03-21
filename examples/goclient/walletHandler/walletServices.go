package walletHandler

import (
	"./grpcConn"
	pb "./identityLayer"
	"context"
	"google.golang.org/grpc/status"
	"log"
)

/*
CreateWallet() takes target as <host/ip>:<port> returns error code or error message
*/
func CreateWallet(target string) (*string, string, []interface{}) {

	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	wallClient := pb.NewWalletServiceClient(gconn)

	cnw, werr := wallClient.CreateNewWallet(context.Background(), &pb.NewWalletDefinition{
		WalletConfig: &pb.Config{
			WalletID: "Wallet3",

			StorePath: &pb.StorageConfig{NewWalletPath: "miu/tempStorage"},
		},
		WalletCredentials: &pb.Credentials{
			NewWalletKey:                "SuperSecret",
			NewWalletStorageCredentials: "",
		},
	})

	if werr != nil {
		resErr, ok := status.FromError(werr)
		{
			// if ok, this will be user error
			if ok {
				log.Println(resErr.Message())
				log.Println(resErr.Details())
				return nil, resErr.Message(), resErr.Details()
			}

		}
	}

	return &cnw.NewWalletErrorCode, "", nil
}
