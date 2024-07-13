import requests

ENDPOINT = "https://todo.pixegami.io/"

# sanity test 
# if ENDPOINT is responding

def test_can_call_endopint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


# create new task and check if it was created by using GET

# python -m pytest -v -s to run and print

def test_create_task():
    payload = {
        "content": "test content",
        "user_id": "test user_id",
        # "task_id": "test task_id", -- task ID generated server side, can be omitted
        "is_done": False
    }
    create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

    # sanity test if user_id value is not something different
    # assert get_task_data["user_id"] == "random user_id"
    