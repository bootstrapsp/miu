# README

## Compiling Proto to generate gRPC GO Client structure
e.g. navigate to \miu\examples\goclient>

```bash
protoc -I ./identitylayer ./identitylayer/identitylayer.proto --go_out=plugins=grpc:identitylayer
```