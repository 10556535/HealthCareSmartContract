pragma solidity ^0.8.0;

contract HealthCare {
 string public profession;

 constructor() public {
    profession = 'Doctor';
}

 function setProfession(string memory _profession) public {
    profession = _profession;
 }

 function myProfession() view public returns (string memory) {
    return profession;
 }
}
