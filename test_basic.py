import requests

ENDPOINT = "https://todo.pixegami.io/"

# sanity test 
# if ENDPOINT is responding

def test_can_call_endopint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200