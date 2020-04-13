package didHandler

import (
	grpcConn "bitbucket.org/scuridclient/grpcConn"
	pb "bitbucket.org/scuridclient/idproto"
	"context"
	"google.golang.org/grpc/status"
	"log"
)

// CreateAndStoreDID takes target for grpc client connection and wallet handle
func CreateAndStoreDID(target string, wallHandler int64) {

	myConn, err := grpcConn.GrpcConn(target)
	if err != nil {
		log.Fatal("DIDHandler's CreateAndStoreDiD() context failed to make grpc connection ", err)
		panic(myConn)
	}
	didClient := pb.NewDidServiceClient(myConn)

	didCreate, didCreateError := didClient.CreateAndStoreMyDid(context.Background(), &pb.CreateAndStoreMyDidRequest{
		WalletHandle: wallHandler,
		DidJson: &pb.CreateAndStoreMyDidJsonMessage{
			Did:        "",
			Seed:       "",
			CryptoType: "ed25519",
			Cid:        true,
		},
	})
	if didCreateError != nil {
		resErr, ok := status.FromError(didCreateError)
		if ok {
			log.Println(resErr.Code())
			log.Println(resErr.Message())
			log.Println(resErr.Details())

		}
	}

	log.Println("New DID created ", pb.CreateAndStoreMyDidResponse{
		Did: didCreate.Did,
	})
	log.Println("New VerKey created ", pb.CreateAndStoreMyDidResponse{
		Verkey: didCreate.Verkey,
	})
}

// ListMyDidsWithMeta takes target for grpc client connection
func ListMyDidsWithMeta(target string, walHandle int64) ([]string, error) {
	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's ListMyDidsWithMeta() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	didList, listingErr := didClient.ListMyDidsWithMeta(context.Background(), &pb.ListMyDidsWithMetaRequest{
		WalletHandle: walHandle,
	})
	if listingErr != nil {
		lisRes, ok := status.FromError(listingErr)
		if ok {
			log.Println(lisRes.Code())
			log.Println(lisRes.Message())
			log.Println(lisRes.Details())

		}
		return nil, listingErr
	}

	return didList.Did, nil

}

// AbbreviateVerkey() takes target and verkey and returns metadata
func AbbreviateVerkey(target, did, verkey string) (abbVerKeyMetaData string) {
	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's AbbreviateVerkey() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	abbVerKey, abbVerErr := didClient.AbbreviateVerkey(context.Background(), &pb.AbbreviateVerkeyRequest{
		Did:        "",
		FullVerkey: "",
	})

	if abbVerErr != nil {
		abbVerRes, ok := status.FromError(abbVerErr)
		if ok {
			log.Fatalln(abbVerRes.Code())
			log.Fatalln(abbVerRes.Message())
			log.Fatalln(abbVerRes.Details())
			return ""
		}

	}
	abbVerKeyMetaData = abbVerKey.Metadata
	return abbVerKeyMetaData
}

// GetMyDidWithMeta() takes target for grpc conn, did and wallet handle and returns metadata with did + verkey

func GetMyDidWithMeta(target, did string, wallHandle int64) (didWithMeta string) {

	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's GetMyDidWithMeta() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	myDidInfo, err := didClient.GetMyDidWithMeta(context.Background(), &pb.GetMyDidWithMetaRequest{
		WalletHandle: wallHandle,
		Did:          did,
	})
	if err != nil {
		log.Fatalln("Couldn't get proper metadata response for your DID, ", err)
		myDIDreserr, ok := status.FromError(err)
		if ok {
			log.Fatalln(myDIDreserr.Code())
			log.Fatalln(myDIDreserr.Message())
			log.Fatalln(myDIDreserr.Details())
		}

	}

	return myDidInfo.Did

}

// GetDidMetadata takes target for grpc client connection , did and wallet handle for fetching DID metadata
func GetDidMetadata(target, did string, walletHandle int64) string {
	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's GetDidMetadata() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	didMetaRes, err := didClient.GetDidMetadata(context.Background(), &pb.GetDidMetadataRequest{
		WalletHandle: walletHandle,
		Did:          did,
	})

	if err != nil {
		log.Fatalln("Couldn't get the metadata information for DID ", err)
		didMetaRestErr, ok := status.FromError(err)
		if ok {
			log.Fatalln(didMetaRestErr.Code())
			log.Fatalln(didMetaRestErr.Message())
			log.Fatalln(didMetaRestErr.Details())
		}
	}
	return didMetaRes.Metadata
}

// SetDidMetadata() takes target , did, metadata and walletHandle as input and returns error code
func SetDidMetadata(target, did, metadata string, walletHandle int64) int64 {
	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's SetDidMetadata() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	setDidMetaRes, err := didClient.SetDidMetadata(context.Background(), &pb.SetDidMetadataRequest{
		WalletHandle: walletHandle,
		Did:          did,
		Metadata:     metadata,
	})

	if err != nil {
		setDidMetaResErr, ok := status.FromError(err)
		if ok {
			log.Fatalln(setDidMetaResErr.Code())
			log.Fatalln(setDidMetaResErr.Details())
			log.Fatalln(setDidMetaResErr.Message())
		}
	}
	return setDidMetaRes.Error
}

func KeyForLocalDid(target, did string, walletHandle, pHandle int64) string {
	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's SetDidMetadata() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	res, err := didClient.KeyForDid(context.Background(), &pb.KeyForDidRequest{
		PoolHandle:   pHandle,
		WalletHandle: walletHandle,
		Did:          did,
	})
	if err != nil {
		resErr, ok := status.FromError(err)
		if ok {
			log.Fatalln(resErr.Code())
			log.Fatalln(resErr.Message())
			log.Fatalln(resErr.Details())
		}
	}

	return res.Key
}

func ReplaceKeysStart(target, did string, wallHandle int64) string {
	myConn, clientErr := grpcConn.GrpcConn(target)
	if clientErr != nil {
		log.Println("DIDHandler's SetDidMetadata() context failed to make grpc connection", clientErr)
		panic(clientErr)
	}
	didClient := pb.NewDidServiceClient(myConn)

	res, err := didClient.ReplaceKeysStart(context.Background(), &pb.ReplaceKeysStartRequest{
		WalletHandle: wallHandle,
		Did:          did,
		IdentityJson: &pb.ReplaceKeysStartIdentityJsonMessage{
			Seed:       "",
			CryptoType: "",
		},
	})
	if err != nil {
		resErr, ok := status.FromError(err)
		if ok {
			log.Fatalln(resErr.Code())
			log.Fatalln(resErr.Message())
			log.Fatalln(resErr.Details())
		}
	}

	return res.Verkey

}
