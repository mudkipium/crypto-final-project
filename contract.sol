pragma solidity ^0.4.11;

contract Ransom {
    uint public demanded;
    address public sendTo;

    // Maps (encrypted) data from victim to the amount the victim has paid
    mapping (int => uint) public ransoms;

    event RansomPaid(int data);
    event KeyGiven(int data, int key, uint payout);

    function Ransom(uint _demand) public {
        demanded = _demand;
        sendTo = msg.sender;
    }
    // TODO some kind of payback mechanism?

    function payRansom(int data) public payable returns (bool) {
        // TODO some kind of return function?
        // Allows multiple payments
        ransoms[data] += msg.value;
        if (ransoms[data] >= demanded) {
            RansomPaid(data);
        } else {
            return false;
        }
    }

    function provideKey(int data, int key) public returns (bool){
        // TODO more robust key checking function
        if (data + key == 0) { // Check validity of key
            uint payout = ransoms[data]; // TODO 0 checks?
            ransoms[data] = 0;
            KeyGiven(data, key, payout);
            sendTo.transfer(payout);
            return true;
        } else {
            return false;
        }
    }
}
