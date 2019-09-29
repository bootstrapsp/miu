# Miu

Miu is a [gRPC](https://grpc.io/) based python server enabling developers to easily connect and develop [Hyperledger Indy](https://www.hyperledger.org/projects/hyperledger-indy) based clients using Hyperledger Indy SDK.

## Overview

Miu introduces all the goodness of gRPC and writing Indy client in your favourite programing language, the ones supported by gRPC. Extending the list of programing languages in which the Indy SDK is currently provided see [libindy SDK](https://github.com/hyperledger/indy-sdk)

## Motivation

Being able to code Indy clients in Golang. :D

## Concept

Miu is implemented in gRPC python using the [Indy SDK for Python](https://github.com/hyperledger/indy-sdk/blob/master/wrappers/python/README.md). This now allows us to build Hyperledger Indy SDK clients using gRPC which can communicate with Miu in high performant [Protobuf](https://developers.google.com/protocol-buffers/) protocol.

### Design Overview

Here's a quick concept overview [Miu-Approach](https://github.com/bootstrapsp/miu/files/3666644/Miu-Approach.pdf)

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

### Project structure

**grpc_server** folder contains Indy SDK module implementation in python

**identityLayer** folder contains all the proto files describing the gRPC structure with RPCs and messages

**config.json** used for configuring the indy node IP address and the pool transaction genesis file.

Note: You'll need to add pool_transactions_genesis file first before configuring in the config.json

## Installation and trying out

### Pre-req

You'll need Indy node / Server before going through with steps defined below. See [How to install Test network](https://github.com/hyperledger/indy-node#how-to-install-a-test-network). 

Once ready use following steps to start with Miu setup

1. Install python 3
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
```

2. Clone [miu](https://github.com/bootstrapsp/miu.git) repository

3. CD into the location where you have cloned

4. Create virtualenv:

```
python3 -m venv my_venv
```

5. Activate virtualenv

```
source ./my_venv/bin/activate
```

6. Install Dependencies

```
pip install -r requirements.txt
```

7. Run the miu interface
```
~/miu/pyserverforindy/grpc_server$ python server.py
```

This will start the server on localhost:50051. You then will have to connect your gRPC client to this. 

## What's next

Of course we'd appreciate help to further enhance this project. Post this alpha release we are looking to work on

* Fixing bugs to stablize this release
* Writing test cases for the Miu interface for automated testing
* Enhanced logging
* And more...
