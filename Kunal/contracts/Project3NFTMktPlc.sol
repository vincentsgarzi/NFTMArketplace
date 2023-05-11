// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

/*
We use the ERC721Full contract to implement the token standard. The following code imports the ERC721Full contract and then creates a new ArtRegistry 
contract that inherits code from it. We use “ArtRegistryToken” for the first parameter and “ART” for the second parameter.
*/

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract ArtRegistry is ERC721Full {
    constructor() public ERC721Full("ArtRegistryToken", "ART") { }
    /*
    'struct' is to represent the artwork information, like the artwork name, the artist name, and the current appraisal value. 
    */

    struct Artwork {
        string name;
        string artist;
        uint256 appraisalValue;
    }

    /*
    Define a new mapping. */

    mapping(uint256 => Artwork) public artCollection;

    /*
    Create events to store value appriasals
    */

    event Appraisal(uint256 token_id, uint256 appraisalValue, string reportURI);

    /*
    Function to register a piece of artwork.
    */

    function registerArtwork(
        address owner,
        string memory name,
        string memory artist,
        uint256 initialAppraisalValue,
        string memory tokenURI) public returns (uint256) {

        // generate the next tokenID by using the totalSupply function
        uint256 tokenId=totalSupply();

        //Mint a new token for the owner address
        _mint(owner, tokenId);

        // Permanently associate the tokenURI value with the token
        _setTokenURI(tokenId, tokenURI);

        // associate all the other arguments that were passed to registerArtwork with the token. This is done using artCollection mapping and the ArtWork data
        // structure
        artCollection[tokenId] = Artwork(name, artist, initialAppraisalValue);
        
        return tokenId;
    }

    /*
    Function that allows us to add a new appraisal
    */

    function newAppraisal(uint tokenId, uint newAppraisalValue, string memory reportURI) public returns (uint256) {
        // we update the appraisal value of the token with the new appraisal value that was passed to our function
        artCollection[tokenId].appraisalValue = newAppraisalValue;

        // log the new appraisal value to the blockchain by firing the Appraisal event - 'emit' function is used to fire event and log the value
        emit Appraisal(tokenId, newAppraisalValue, reportURI);

        return artCollection[tokenId].appraisalValue;

    }

}