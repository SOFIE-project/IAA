# Identity, Authentication, and Authorization Component
## Description


### Architecture Overview



### Relation with SOFIE

Nore information about this component and its relation to the SOFIE project can be found in [D2.5 Federation Framework, SOFIE deliverable](https://media.voog.com/0000/0042/0957/files/SOFIE_D2.5-Federation_Framework%2C_2nd_version.pdf)


### Key Technologies



## Usage


## Installation

### Prerequisites
Python 3, Hyperledger Indy SDK and the python wrapper, PyJWT are required. Use the following commands to install the prerequisites in Ubuntu 18.04 

* sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE7709D068DB5E88
* sudo add-apt-repository "deb https://repo.sovrin.org/sdk/deb bionic stable"
* sudo apt-get update
* sudo apt-get install -y libindy
* pip3 install python3-indy pyjwt web3 


### Configuration
A sample configuration file is provided at conf/sample.conf

### Execution from source
From the root directory run `python3 IAA/iaa.py <configuration file>` e.g., `python3 IAA/iaa.py conf/iaa.conf`

### Dockerized version
In order to build IAA image, execute the script `docker-build.sh`. Then you can run IAA using, for example,  `docker run -tid --rm -p 9000:9000 iaa`. You can verfiry that IAA is running properly be executing the script `examples/validate_token.sh`

### Usage
The executed script creates an HTTP server that listens for REST API calls at port 9000. The REST API of IAA component is documented in 

https://app.swaggerhub.com/apis-docs/nikosft/SOFIE-PDS-IAA/1.0.0#/IAA/vertoken 

Please select **schema** to see all available API parameters and their documentation.

#### Examples
Verifying a DID (see also tests/test_api.py)
```python
user = {
        'wallet_config': json.dumps({'id': 'user_wallet',"storage_config":{"path":"tests/indy_wallets"}}),
        'wallet_credentials': json.dumps({'key': 'user_wallet_key'}),
        'did' : '4qk3Ab43ufPQVif4GAzLUW'
    }
payload = {'token-type':'DID', 'token':user['did']}
response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
response =json.loads(response)
assert(response['code'] == 401)
challenge = response['challenge']
wallet_handle = await wallet.open_wallet(user['wallet_config'], user['wallet_credentials'])
verkey = await did.key_for_local_did(wallet_handle, user['did'])
signature = await crypto.crypto_sign(wallet_handle, verkey, challenge.encode())
signature64 = base64.b64encode(signature)
payload = {'token-type':'DID', 'token':user['did'], 'challenge': challenge, 'proof':signature64}
response  = requests.post("http://localhost:9000/verifytoken", data = payload).text
response =json.loads(response)
assert(response['code'] == 200)
await wallet.close_wallet(wallet_handle)
```

## Testing

### Prerequisites

Tests are executed using pytest and pytest-asyncio. To install it execute 

* pip3 install -U pytest 
* pip3 install pytest-asyncio

### Running the tests
From the root directory run `python3 -m pytest -s  tests/`


## Integration

To be provided.

## Deployment

To be provided.

## Known/Open Issues

No known issues

## Contact info

Please contact Nikos Fotiou or Dimitris Dimopoulos (AUEB) in case of any questions.

***