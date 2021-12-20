from _pytest.config import exceptions
from brownie import Lottery, accounts, config, network, exceptions
from toolz.itertoolz import get
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)
import time


def test_can_enter_rinkeby():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000000})
    assert lottery.players(0) == account


def test_can_pick_winner_rinkeby():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 10000000})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(120)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
