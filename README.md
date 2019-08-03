# Miu

Miu is a [gRPC](https://grpc.io/) based python server enabling developers to easily connect and develop [Hyperledger Indy](https://www.hyperledger.org/projects/hyperledger-indy) based clients using Hyperledger Indy SDK.

## Overview

Miu introduces all the goodness of gRPC and writing Indy client in your favourite programing language, the ones supported by gRPC. Extending the list of programing languages in which the Indy SDK is currently provided see [libindy SDK](https://github.com/hyperledger/indy-sdk)

## Motivation

Being able to code Indy clients in Golang. :D

## Concept

Miu is implemented in gRPC python using the [Indy SDK for Python](https://github.com/hyperledger/indy-sdk/blob/master/wrappers/python/README.md). This now allows us to build Hyperledger Indy SDK clients using gRPC which can communicate with Miu in high performant [Protobuf](https://developers.google.com/protocol-buffers/) protocol.

## Current state with this release

Current release covers implementation for most of the modules from Indy SDK, precisely speaking :

* Anoncreds
* Blob Storage
* Crypto
* DID
* Ledger
* NonSecret
* Pairwise
* Pool
* Wallet

### Project is structure

**grpc_server** folder contains Indy SDK module implementation in python

**identityLayer** folder contains all the proto files describing the gRPC structure with RPCs and messages

**config.json** used for configuring the indy node IP address and the pool transaction genesis file.

Note: You'll need to add pool_transactions_genesis file first before configuring in the config.json


## What's next

Of course we'd appreciate help to further enhance this project. Post this alpha release we are looking to work on

* Fixing bugs to stablize this release
* Writing test cases for the Miu server for automated testing

