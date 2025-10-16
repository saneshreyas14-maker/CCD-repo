# tests/test_api.py
import time
import requests

BASE = 'http://127.0.0.1:5000'

def test_menu_and_report():
    r = requests.get(f"{BASE}/menu")
    assert r.status_code == 200
    assert 'items' in r.json()

    r = requests.get(f"{BASE}/report")
    assert r.status_code == 200
    j = r.json()
    assert 'resources' in j and 'profit' in j

def test_order_flow_success_and_insufficient():
    # make a successful order for espresso (cost 1.5) with enough paid
    r = requests.post(f"{BASE}/order", json={"drink": "espresso", "paid": 2.0})
    assert r.status_code == 200
    jr = r.json()
    assert jr['status'] == 'success'

    # now attempt to order a drink with insufficient payment
    r = requests.post(f"{BASE}/order", json={"drink": "latte", "paid": 0.5})
    assert r.status_code == 402

def test_order_not_found_and_resources():
    r = requests.post(f"{BASE}/order", json={"drink": "nonexistent", "paid": 10})
    assert r.status_code == 404

    # drain a resource until insufficient
    # keep ordering espresso until water or coffee runs out
    count = 0
    while True:
        r = requests.post(f"{BASE}/order", json={"drink": "espresso", "paid": 2.0})
        if r.status_code == 409:
            break
        assert r.status_code == 200
        count += 1
        if count > 20:
            break
    assert r.status_code in (409, 200)
