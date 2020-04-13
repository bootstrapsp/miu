package grpcConn

import (
	"google.golang.org/grpc"
	"log"
)

/*
GrpcConn() takes Miu's connection string <host>:<port>, returns grpc client conn or error
*/
func GrpcConn(target string) (grpcConn *grpc.ClientConn, err error) {

	if target == "" {
		target = "localhost:50051"
		log.Println("No target received, trying default ", target)
	}
	grpcConn, err = grpc.Dial(target, grpc.WithInsecure())
	if err != nil {
		log.Fatalln("Couldn't dial connection to Miu see :", err)
		return nil, err
	}
	return grpcConn, nil
}
