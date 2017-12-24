pragma solidity ^0.4.11;

contract Ransom {
    uint public demanded;
    address public sendTo;

    // Maps (encrypted) data from victim to the amount the victim has paid
    mapping (int => uint) public ransoms;

    event RansomPaid(int hash);
    event KeyGiven(int data, int key, uint payout);

    function Ransom(uint _demand) public {
        demanded = _demand;
        sendTo = msg.sender;
    }
    // TODO some kind of payback mechanism?

    function payRansom(int data, int hash) public payable returns (bool) {
        // TODO some kind of return function?
        // NO LONGER Allows multiple payments

		ransoms[data] = hash;

		if msg.value >= demanded {
			RansomPaid(hash);
		} else {
			return false;
		}

        // ransoms[data] += msg.value;
        // if (ransoms[data] >= demanded) {
            // RansomPaid(data);
        // } else {
            // return false;
        // }
    }

    function provideKey(bytes32 data, int key) public returns (bool){
		// Assuming key is 8-bit integer (0-255)
		// Run Caesar Decryption:
		bytes32 decryptedData = data;
		for (uint i = 0; i < decryptedData.length; i++) {
			decryptedData[i] = (decryptedData[i] - key) % 256;
		}
		// Compute SHA256 Hash
		decryptHash = sha256(decryptedData);
		if (decryptHash == ransoms[data]) { //if decrypted hash == hash of original data before decryption
			uint payout = ransoms[data]; // TODO 0 checks?
            ransoms[data] = 0;
            KeyGiven(data, key, payout);
            sendTo.transfer(payout);
            return true;
        } else {
            return false;
		}

        // TODO more robust key checking function
        // if (data + key == 0) { // Check validity of key
            // uint payout = ransoms[data]; // TODO 0 checks?
            // ransoms[data] = 0;
            // KeyGiven(data, key, payout);
            // sendTo.transfer(payout);
            // return true;
        // } else {
            // return false;
        // }
    }
}