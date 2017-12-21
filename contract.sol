pragma solidity ^0.4.11;

contract Ransom {
    uint public demanded;
    address public sendTo;

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
        if (msg.value >= demanded) {
            ransoms[data] = msg.value;
            RansomPaid(data);
        } else {
            return false;
        }
    }

    function provideKey(int data, int key) public returns (bool){
        if (data + key == 0) { // Needs to be more complicated function
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