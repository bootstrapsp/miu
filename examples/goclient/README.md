# README

## Compiling Proto to generate gRPC GO Client structure
e.g. navigate to \miu\examples\goclient>


```bash


protoc -I ./identitylayer ./identitylayer/identitylayer.proto --go_out=plugins=grpc:identitylayer
```

## What's in client examples

It provides sample implementation structure in Golang, how different gRPC can be invoked

## What's not in client examples

Currently, client only holds examples in Golang. Of course, client implementation is supported in as many languages as supported by gRPC, see https://grpc.io/docs/tutorials/ for supported languages.

Also, in current state what client examples does not provide is a main function. Will add this once all the examples are covered in a sequenced call within that main.