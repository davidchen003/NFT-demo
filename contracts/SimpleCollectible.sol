// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor() public ERC721("Dogie", "DOG") {
        //"Dogie" is the name, and "DOG" is symbol
        tokenCounter = 0;
    }

    //this NFT contract is what's known as factory contract
    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId); // _safeMind() in ERC721.sol
        _setTokenURI(newTokenId, tokenURI); // _setTokenURI() in ERC721.sol
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
