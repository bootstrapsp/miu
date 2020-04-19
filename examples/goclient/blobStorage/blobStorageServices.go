package blobStorage

import (
	"bitbucket.org/scuridclient/grpcConn"
	pb "bitbucket.org/scuridclient/idproto"
	"google.golang.org/grpc/status"
	"log"
	"context"
)

/*
OpenReader() accepts target, type_ and config as string and returns int64
 */
func OpenReader(target, type_, config string) int64 {
	myConn, err := grpcConn.GrpcConn(target)
	if err != nil {

		log.Fatal("BlobStorage's OpenReader() context failed to make grpc connection ", err)

	}
	bsClient := pb.NewBlobStorageServiceClient(myConn)
	orRes, err := bsClient.OpenReader(context.Background(), &pb.OpenReaderRequest{
		Type_:  type_,
		Config: config,
	})

	if err != nil {
		resErr, ok := status.FromError(err)
		if ok {
			log.Println(resErr.Code())
			log.Println(resErr.Message())
			log.Println(resErr.Details())
		}
	}

	return orRes.Res

}

/*
OpenWriter() accepts target, type_ and config as string and returns int64
 */

func OpenWriter(target, type_, config string) int64 {
	myConn, err := grpcConn.GrpcConn(target)
	if err != nil {

		log.Fatal("BlobStorage's OpenWriter() context failed to make grpc connection ", err)

	}
	bsClient := pb.NewBlobStorageServiceClient(myConn)

	owRes, err :=bsClient.OpenWriter(context.Background(), &pb.OpenWriterRequest{
		Type_:  type_,
		Config: config,
	})

	if err != nil {
		owResErr,ok :=status.FromError(err)
		if ok{
			log.Println(owResErr.Code())
			log.Println(owResErr.Message())
			log.Println(owResErr.Details())
		}
	}

	return owRes.Res
}

