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
