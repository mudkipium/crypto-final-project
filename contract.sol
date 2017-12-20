pragma solidity ^0.4.11;

contract Ransom {
    uint public demanded;
    address public sendTo;

    mapping (uint => uint) public ransoms;

    event RansomPaid(uint data);
    event KeyGiven(uint data, uint key);

    function Ransom(uint _demand) public {
        demanded = _demand;
        sendTo = msg.sender;
    }

    function payRansom(uint data) public payable returns (bool) {
        if (msg.value >= demanded) {
            ransoms[data] = msg.value;
            RansomPaid(data);
        } else {
            return false;
        }
    }

    function provideKey(uint data, uint key) public returns (bool){
        if (data + key == 0) { // Needs to be more complicated function
            uint payout = ransoms[data];
            if(payout == 0) revert();
            ransoms[data] = 0;
            KeyGiven(data, key);
            sendTo.transfer(payout);
            return true;
        } else {
            return false;
        }
    }
}