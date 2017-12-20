
pragma solidity ^0.4.0;

contract Elf {

    mapping (uint => uint) public hashes;

    event NewHash(uint key, uint value);

    function hash(uint amount) public returns (uint) {
        if (hashes[amount] == 0) {
            hashes[amount] = amount + 5;
            NewHash(amount, amount + 5);
        }
        return hashes[amount];
    }

}