from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_payment_approved_example(): 
    gateway = Mock() 
    gateway.charge.return_value = True 
    amount = OrderService(gateway).checkout(Order(100)) 
    assert amount == 100 
    gateway.charge.assert_called_once_with(100) 

def test_payment_rejected_vip():
    gateway = Mock()
    gateway.charge.return_value = False 
    service = OrderService(gateway)
    pedido_vip = Order(200, vip=True)
    with pytest.raises(RuntimeError, match="payment rejected"):
        service.checkout(pedido_vip)        
    gateway.charge.assert_called_once_with(170)

def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))
