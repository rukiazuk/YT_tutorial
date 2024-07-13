import requests
import uuid # allows to generate random strings for user_id

ENDPOINT = "https://todo.pixegami.io/"

# sanity test 
# if ENDPOINT is responding

def test_can_call_endopint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


# create new task and check if it was created by using GET

# python -m pytest -v -s to run and print

def test_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    # extract task id from response
    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]

    # sanity test if user_id value is not something different
    # assert get_task_data["user_id"] == "random user_id"


def test_can_update_task():
    # create new task

    # create new task payload
    payload = new_task_payload()
    # create new task 
    create_task_response = create_task(payload)
    # safe to check if new task was created
    assert create_task_response.status_code == 200
    # get the task id
    task_id = create_task_response.json()["task"]["task_id"]
    # update the task with changed payload

    # new payload
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True,
    }
    # actual task update with new_payload and check if task was updated
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes (if the content was updated and if is done is set to true)
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


# list all task for specified user - create 3 tasks for a user and list tasks ans make sure if 3 tasks are listed
def test_can_list_tasks():
    # create n tasks
    n = 3
    payload = new_task_payload()
    for _ in range(3):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    # list tasks and check that there are n (3) items
    user_id =  payload["user_id"]
    list_tasks_response = list_tasks(user_id)
    assert list_tasks_response.status_code == 200
    data = list_tasks_response.json()
    print(data) 
    
    # data is printed as list called 'tasks' - the list has 3 items but we want to confirm that
    tasks = data["tasks"]
    assert len(tasks) == n


# delete taks
def test_can_delete_task():
    # first, create new task 
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    # extract task id from response
    task_id = create_task_response.json()["task"]["task_id"]
    # delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    # get the task, check if it is not found
    get_task_response = get_task(task_id)
    # running below print to have exact ststus code printed - it is 2404
    print(get_task_response.status_code)
#
#
#
#
# helper functions

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def new_task_payload():
    # create random user_id using uuid. this is created as an object, so it needs to be converted to string - adding 'hex'
    user_id = f"test_user_{uuid.uuid4().hex}"
    # doing the same for content with uuid appended in the end
    content = f"test_content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False
    }

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")