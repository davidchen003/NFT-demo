[course TOC, code, and resources](https://github.com/smartcontractkit/full-blockchain-solidity-course-py/blob/main/README.md#lesson-11-nfts)

[clone the repository](https://github.com/PatrickAlphaC/nft-mix) - `brownie bake nft-mix`

[ERC-721 NFT Standard](https://eips.ethereum.org/EIPS/eip-721)

[How to Make an NFT and Render it on the OpenSea Marketplace](https://www.freecodecamp.org/news/how-to-make-an-nft-and-render-on-opensea-marketplace/)

[Dungeons and Dragons Example](https://github.com/PatrickAlphaC/dungeons-and-dragons-nft), done in **truffle** (instead of brownie)

- NFT: hybrid smart contract:
  - have off-chain component interaction with random numbers, and
  - restoring their meta data with **IPFS**

## Setup

- `$mkdir nft-demo`
- `$brownie init`

## SimpleCollectible.sol

- instead of copy/paste [ERC-721 NFT Standard](https://eips.ethereum.org/EIPS/eip-721) and recoding, we'll be using
- [OpenZeppelin ERC-721 3.x](https://docs.openzeppelin.com/contracts/3.x/erc721)

  - `import "@openzeppelin/contracts/token/ERC721/ERC721.sol"`
  - add dependencies and compiler info in `brownie-config.yaml`
  - inherit from ERC721.sol: `contract SimpleCollectible is ERC721 {`

- `img/pug.png`

- `scripts/simple_collectible/deploy_and_create.py`
- `scripts/helpful_scripts.py`
- `__init__.py`, `.env`, `brownie-config.yaml`

- `brownie run scripts/simple_collectible/deploy_and_create.py --network rinkeby`
  - Awesome, you can view your NFT at https://testnets.opensea.io/assets/0x151EE60035f1cdC2Fa8f39535A8536a894FD6902/0

**Commit 1**

## Unit test

- `tests/unit/test_simple_collectible.py`
- `$brownie test`

- What we didn't do:
  - didn't upload an image to IPFS ourselves
  - why is IPFS decentralized?
  - Anyone can min an NFT - no verifiably scarce or random

## AdvancedCollectible.sol

- Where the tokenURI can be one of 3 different dogs, randomly selected
- `contracts/AdvancedCollectible.sol`
- `import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";` for random number
  - add corresponding dependencies and compiler info in `brownie-config.yaml`
- `contract AdvancedCollectible is ERC721, VRFConsumerBase {`
- best practice: to emit events when you update mappings
- `brownie compile` to make sure no errors in the contract

## deploy_and_create.py

- `scripts/advanced_collectible/deploy_and_create.py`
- add Rinkeby network info `vrf_coordinator, link_token, keyhash` in brownie-confi from [chainlink VRF] (https://docs.chain.link/docs/vrf-contracts/)
- add `get_contract` (same as brownie_lottery project) to `helpful_scripts.py`. It is smart enough to determine wether we need to deploy a mock or just grab from an actual contract.
- `deploy_mocks()`, add `contract_to_mock` map
- `fund_with_link`

- !!!
  - **don't forget to add `/contracts/test/LinkToken.sol and VRFCoordinatorMock.sol`** (same as brownie_lottery project). Otherwise, runtime error, for `from brownie import VRFCoordinatorMock, LinkToken` in helpful_sxripts.py
    - `ImportError: cannot import name 'VRFCoordinatorMock' from 'brownie' (/home/david/.local/lib/python3.8/site-packages/brownie/__init__.py)`, or `ImportError: cannot import name 'VRFCoordinatorMock' from 'brownie' (/home/david/.local/lib/python3.8/site-packages/brownie/__init__.py)` if LinkToken listed ahead of VRFCoordinatorMock
- !!!

- `brownie run scripts/advanced_collectible/deploy_and_create.py`
- `brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby`
  - we can see the record as rinkeby etherscan by 0xA29f528880c8250659b6cFC7D95E200A47879897

**Commit 2**

## create_collectible.py

- `scripts/advanced_collectible/create_collectible.py`
- `brownie run scripts/advanced_collectible/create_collectible.py --network rinkeby`

- to (flatten and) publish code

  - add a line in our .env file `export ETHERSCAN_TOKEN=my etherscan.io API Key`
  - modify deploy_fund_me(), `fund_me=FundMe.deploy({'from':account}, publish_source=True)`
  - add `verify: true` to Rinkeby in brownie-config

- deploy contract and run create_collectible again
  - `brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby`
  - `brownie run scripts/advanced_collectible/create_collectible.py --network rinkeby`
  - use address 0xaab25a0520e9622B3040f538Fa3182B6956e8c9E, to see the transaction, source code, and interact with contract/functions (Rinkeby etherscan -> Contract -> Read Contract), e.g. (be aware it may take a while for the transaction to go through)
    - tokenCounter, will see it increased from 1 to 2)
    - tokenToBreed, will see token id 0 has breed index 1, token id 1 has breed index 0

**Commit 3**

## Unit / Integration tests

**Unit test**

- `tests/unit/test_advanced_collectible.py`
- add `creating_tx` in `return advanced_collectible, creating_tx` of deploy_and_create()
- remove `publish_source=True` from deploy_and_create(), or better
- change it to `publish_source=config["networks"][network.show_active()].get("verify")`
- `$brownie test -k test_can_create_advanced_collectible`

**Integration test**

- `tests/integration/test_advanced_collectible_integration.py`
- the differences are:
  - we are not going to be the one who calls back with a random #
  - we don't need requestId either since the chainlink node is going to be responding
  - and we need to wait for the transaction to get call back
- `$brownie test -k test_advanced_collectible_integration.py --network rinkeby` (failed!)

## Creating Metadata & IPFS

- don't host metadata on a centralized server
- [FileCoin](https://filecoin.io/) - further improvement over IPFS. IPFS is going to be able to hook up to FileCoin in future. It's a good enough solution for us now.

- `scripts/advanced_collectible/create_metadata.py`
- `metadata/sample_metadata.py`
- `metadata/rinkeby/` to save the metadata for rinkeby
- `upload_to_ipfs(filepath):`

**uploading to IPFS**

- [IFPF download commandline](https://docs.ipfs.io/install/command-line/#system-requirements)
- there is also a [desktop version](https://docs.ipfs.io/install/ipfs-desktop/) for manual operations
- [IPFS HTTP API](https://docs.ipfs.io/reference/http/api/#getting-started)
  - [/api/v0/add](https://docs.ipfs.io/reference/http/api/#api-v0-add) for add file/directory to IPFS
- we'll upload the images to our own IPFS node, which we can run it by:
  - `$ipfs init`, then `$ipfs daemon`, which shows
    - WebUI: http://127.0.0.1:5001/webui
- **keep the node running**, open another terminal to continue

- `$brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby`, will see our image is uploaded to:
  - https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png

**Commit 4**

## Pinata (an alternative to IPFS)

- `scripts/upload_to_pinata.py`
- sign up at Pinata, create API key, and enter PINATA_API_KEY and PINATA_API_SECRET in `.env`
- `$brownie run scripts/upload_to_pinata.py`
  - we can see from our [pinata](https://app.pinata.cloud/pinmanager), the image is uploaded there.
- so now, if you want, you can use Pinata's image uri instead of using `upload_to_ipfs()` to get it

**Commit 5**

- upload JSON metadata file to IPFS also
  - `$brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby` (make sure ipfs daemon is still running in another terminal)
    - https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png
    - https://ipfs.io/ipfs/QmW4qPbedTL7DS3AgdzMnrw7YKYZB2miLAywJBNZe97kTz?filename=0-ST_BERNARD.json
  - `./metadata/rinkeby/0-ST_BERNARD.json` is also save

**Commit 6**

**refactor to not re-upload to IPFS**

- add `export UPLOAD_IPFS = false` to .env
- add `breed_to_image_uri` dictionary in create_matadata.py

## setTokenURI()

- `scripts/advanced_collectible/set_tokenuri.py`

## Test

- run unit test `$brownie test`
- run scripts manually one by one (make sure MetaMask is open, on Rinkeby, have some ETH and LINK)

  - `$ brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby`
    - 0xfc321692F8D934edC21450B30930C0Be93D6D743
    - use it on rinkeby etherscan to find detailed info, and interact with the contract (Contract -> Read Contract)
  - `$brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby`
    - ./metadata/rinkeby/0-ST_BERNARD.json already exists! Delete it to overwrite
  - so let's run `$brownie run scripts/advanced_collectible/create_collectible.py --network rinkeby`
  - then run again `$brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby`

- paste the above contract address at [testnet OpenSea](https://testnets.opensea.io/), you'll find items (not yet!?, but following individual url show item, w/o images) there, but w/o images, so
- `brownie run scripts/advanced_collectible/set_tokenuri.py --network rinkeby`
  - now the images should be there (only two out of the three individual urls, nothing showed up by contract #)

---

Working on rinkeby
You have 3 tokenIds
Setting tokenURI of 0
Transaction sent: 0x96ac5e561277ee6f4dc1d8035121353137881997c6da3a56510039c4e1cefe98
Gas price: 1.000000008 gwei Gas limit: 132306 Nonce: 101
AdvancedCollectible.setTokenURI confirmed Block: 9843710 Gas used: 120279 (90.91%)

AdvancedCollectible.setTokenURI confirmed Block: 9843710 Gas used: 120279 (90.91%)

Awesome! You can view your NFT at https://testnets.opensea.io/assets/0xfc321692F8D934edC21450B30930C0Be93D6D743/0
Please wait up to 20 minutes, and hit the refresh metadata button
Setting tokenURI of 1
Transaction sent: 0x54ee8919fc2bd6380bbac87929a323b23044efb596ba3c29e263c692f1ee89ab
Gas price: 1.000000008 gwei Gas limit: 132306 Nonce: 102
AdvancedCollectible.setTokenURI confirmed Block: 9843711 Gas used: 120279 (90.91%)

AdvancedCollectible.setTokenURI confirmed Block: 9843711 Gas used: 120279 (90.91%)

Awesome! You can view your NFT at https://testnets.opensea.io/assets/0xfc321692F8D934edC21450B30930C0Be93D6D743/1
Please wait up to 20 minutes, and hit the refresh metadata button
Setting tokenURI of 2
Transaction sent: 0x67590c5c52f1a5735cdf8ab7df5e657cb6062cdd00e7ec61390218d5ad03f6f8
Gas price: 1.000000008 gwei Gas limit: 132227 Nonce: 103
AdvancedCollectible.setTokenURI confirmed Block: 9843712 Gas used: 120207 (90.91%)

AdvancedCollectible.setTokenURI confirmed Block: 9843712 Gas used: 120207 (90.91%)

Awesome! You can view your NFT at https://testnets.opensea.io/assets/0xfc321692F8D934edC21450B30930C0Be93D6D743/2
Please wait up to 20 minutes, and hit the refresh metadata button

**Commi 7**
