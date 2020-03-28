package walletHandler

import (

	"context"
	"google.golang.org/grpc/status"
	"log"
	"miu-client/grpcConn"
	pb "miu-client/proto"
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


/*
GenerateWalletKey() takes target and seed as input and returns generatedWalletKey or message and details on error

*/

func GenerateWalletKey(target, seed string) (generatedWalletKey string, message string, details []interface{}) {
	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	wallClient := pb.NewWalletServiceClient(gconn)

	gwk, err := wallClient.GenerateWalletKey(context.Background(), &pb.GenerateWalletKeyDefinition{
		Seed: sch.ConfigProcessor().GeneratedWalletSeed,
	})
	generatedWalletKey = gwk.GenerateWalletKeyStatus
	if err != nil {
		genwallres, ok := status.FromError(err)
		if ok {
			log.Println(genwallres.Message())
			log.Println(genwallres.Details())
			return "", genwallres.Message(), genwallres.Details()
		}
	}

	return generatedWalletKey, "", nil
}

/*

ExportWallet() takes input to target and wallet handle, returns bool based confirmation on success / failure

*/
func ExportWallet(target string, wh int64) (exportWallCon bool, message string, details []interface{}, err error) {
	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	wallClient := pb.NewWalletServiceClient(gconn)


	exWalCon, err := wallClient.ExportWallet(context.Background(), &pb.ExportWalletDefinition{
		ExportWalletHandle: wh,
		ExportConfigJson: &pb.ExportWalletConfigJson{
			ExportWalletPath:                sch.ConfigProcessor().WalletExportLoc,
			ExportWalletKey:                 "SuperSecret",
			ExportWalletKeyDerivationMethod: "ARGON2I_MOD",
		},
	})
	exportWallCon = exWalCon.ExportWalletStatus

	if err != nil {
		exWalRes, ok := status.FromError(err)
		if ok {
			log.Println(exWalRes.Message())
			log.Println(exWalRes.Details())
			return exportWallCon, exWalRes.Message(), exWalRes.Details(), nil
		}

		return exportWallCon, exWalRes.Message(), exWalRes.Details(), err
	}
	return exportWallCon, "", nil, nil

}

/*
ImportWallet (ImportWalletDefinition) returns wallet import confirmation or error with details and messages
*/
func ImportWallet(target string) (wallImportMsg, message string, details []interface{}) {
	gconn, gerr := grpcConn.GrpcConn(target)
	if gerr != nil {
		log.Fatal("CreateWallet rpc failed to connect see err", gerr)
	}

	wallClient := pb.NewWalletServiceClient(gconn)

	wallImpRes, err := wallClient.ImportWallet(context.Background(), &pb.ImportWalletDefinition{
		Config: &pb.ImportWalletConfig{
			Id:          sch.ConfigProcessor().WallId,
			StorageType: "",
			StorageConfig: &pb.ImportWalletStorageConfig{
				Path: sch.ConfigProcessor().WalletImportLoc,
			},
		},
		Credentials: &pb.ImportWalletCredentials{
			Key:                 "SuperSecret",
			StorageCredentials:  "",
			KeyDerivationMethod: "ARGON2I_MOD",
		},
		ConfigJson: &pb.ImportWalletConfigJson{
			Path: sch.ConfigProcessor().WalletExportLoc,
			Key:  "SuperSecret",
		},
	})

	wallImportMsg = wallImpRes.ImportWalletStatusCode
	if err != nil {
		walres, ok := status.FromError(err)
		if ok {
			log.Println(walres.Message())
			log.Println(walres.Details())

		}
		return "", walres.Message(), walres.Details()

	}

	return wallImportMsg, "", nil
}
