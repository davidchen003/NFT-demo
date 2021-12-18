[course TOC, code, and resources](https://github.com/smartcontractkit/full-blockchain-solidity-course-py/blob/main/README.md#lesson-11-nfts)

[clone the repository](https://github.com/PatrickAlphaC/nft-mix) - `brownie bake nft-mix`

[ERC-721 NFT Standard](https://eips.ethereum.org/EIPS/eip-721)

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
