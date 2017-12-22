pragma solidity ^0.4.11;

contract Ransom {
    uint public demanded;
    address public sendTo;

    // Maps (encrypted) data from victim to the hash of the victim's data
    mapping (bytes32 => bytes32) public ransoms;

    event RansomPaid(bytes32 hash);
    event KeyGiven(bytes32 data, uint key, uint payout);

    function Ransom(uint _demand) public {
        demanded = _demand;
        sendTo = msg.sender;
    }
    // TODO some kind of payback mechanism?

    function payRansom(bytes32 data, bytes32 hash) public payable returns (bool) {
        // TODO some kind of return function?
        if (msg.value >= demanded) {
            ransoms[data] = hash;
            RansomPaid(hash);
        } else {
            return false;
        }
    }

    function provideKey(bytes32 data, uint8 key) public returns (bool){
        // Assuming key is 8-bit integer (0-255)
        // Run Caesar Decryption:
        bytes1[] memory decryptedData = new bytes1[](data.length);
        for (uint i = 0; i < decryptedData.length; i++) {
            decryptedData[i] = bytes1((uint8(data[i]) - key) % 256);
        }
        // Compute SHA256 hash to check if decryption is valid
        bytes32 decryptHash = sha256(bytesToBytes32(decryptedData));
        if (decryptHash == ransoms[data]) {
            KeyGiven(data, key, demanded);
            sendTo.transfer(demanded);
            return true;
        } else {
            return false;
        }

    }

    function bytesToBytes32(bytes1[] memory source) returns (bytes32 result) {
        assembly {
            result := mload(add(source, 32))
        }
    }
}
