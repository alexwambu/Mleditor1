from solcx import compile_standard, install_solc
import os, json, subprocess

install_solc("0.8.17")

ERC20_TEMPLATE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;
contract Token {
    string public name = "{{name}}";
    string public symbol = "{{symbol}}";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    event Transfer(address indexed from, address indexed to, uint256 value);
    constructor(uint256 supply) {
        totalSupply = supply * 10 ** uint256(decimals);
        balanceOf[msg.sender] = totalSupply;
    }
    function transfer(address to, uint256 value) public returns (bool success) {
        require(balanceOf[msg.sender] >= value);
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }
}
"""

def deploy_token(name, symbol, supply):
    code = ERC20_TEMPLATE.replace("{{name}}", name).replace("{{symbol}}", symbol)
    with open("Token.sol", "w") as f:
        f.write(code)
    compiled = compile_standard({
        "language": "Solidity",
        "sources": {"Token.sol": {"content": code}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode.object"]}}}
    })
    contract = compiled["contracts"]["Token.sol"]["Token"]
    return {"abi": contract["abi"], "bytecode": contract["evm"]["bytecode"]["object"]}
