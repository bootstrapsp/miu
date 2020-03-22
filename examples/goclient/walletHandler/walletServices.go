package walletHandler

import (
	"./grpcConn"
	pb "./identityLayer"
	"context"
	"google.golang.org/grpc/status"
	"log"
)

/*
CreateWallet() takes target as <host/ip>:<port> returns error code or error message details from gRPC
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

/*
OpenWallet takes target <host/ip>:<port> returns wallet handle,  error code or error message details from gRPC
*/
func OpenWallet(target string) (wallHandle int64, wallHandleErrCode int64, message string, details []interface{}) {

	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	wallClient := pb.NewWalletServiceClient(gconn)

	owh, err := wallClient.OpenWallet(context.Background(), &pb.OpenWalletDefinition{
		Config: &pb.OpenWalletConfig{
			Id:          "WalletID",
			StorageType: "",
			Path: &pb.OpenWalletStorageConfig{
				Path: "miu/tempStorage",
			},
		},
		Credentials: &pb.OpenWalletCredentials{
			Key:                   "SuperSecret",
			ReKey:                 "",
			StorageCredentials:    "",
			KeyDerivationMethod:   "",
			ReKeyDerivationMethod: "",
		},
	})
	wallHandle = owh.WalletHandle
	wallHandleErrCode = owh.ErrorCode

	if err != nil {
		resErr, ok := status.FromError(err)
		if ok {
			// if ok this will be user error
			log.Println(resErr.Message())
			log.Println(resErr.Details())
			return wallHandle, wallHandleErrCode, resErr.Message(), resErr.Details()
		}

	}
	return wallHandle, wallHandleErrCode, "", nil

}



/*
CloseWallet() takes target <host/ip>:<port>  & wallet handle, returns close status, message and details of gRPC errors

 */

func CloseWallet (target string, wh int64) (closewallstatus string, message string, details []interface{}){
	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	wallClient := pb.NewWalletServiceClient(gconn)

	cws, err := wallClient.CloseWallet(context.Background(), &pb.CloseWalletHandle{
		WalletHandle: wh,
	})
	closewallstatus = cws.CloseWalletCode

	if err != nil{
		wcres ,ok:=status.FromError(err)
		if ok{
			log.Println(wcres.Message())
			log.Println(wcres.Details())
			return "", wcres.Message(),wcres.Details()
		}
	}
	return closewallstatus, "", nil
}