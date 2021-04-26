import pytest
import json
import json_reader as jr

# RUN THIS FILE WITH python -m pytest -s FROM ROOT DIRECTORY

def test_create_story():
    reader = jr.json_reader(file_path="pytest_data/input1.json")
    
    my_obj = {
                "id": 6,
                "priority": -1,
                "estimate": -1,
                "sprint": 2,
                "status": "",
                "assigned_to": "Caspar Popova",
                "user_type": "customer",
                "story": "I want to create a new story w pytest"
            }

    my_log = "current_sprint"
    reader.create(entry=my_obj, log=my_log)

    my_id = 6
    that_obj, that_log = reader.read(id=my_id, log=my_log)
    other_obj, other_log = reader.read(id=my_id, log=None)
    
    #reader.close() # omit close

    assert that_obj == my_obj
    assert that_log == my_log
    assert other_obj == my_obj
    assert other_log == my_log

def test_delete_story():
    reader = jr.json_reader(file_path="pytest_data/input2.json")

    expected_objs = [{
                    "id": 3,
                    "priority": 3,
                    "estimate": 4,
                    "sprint": 2,
                    "status": "to-do",
                    "assigned_to": "George Clooney",
                    "user_type": "customer",
                    "story": "I want to update a story."
                },
                {
                    "id": 2,
                    "priority": -1,
                    "estimate": -1,
                    "sprint": 2,
                    "status": "",
                    "assigned_to": "Jane Doe",
                    "user_type": "customer",
                    "story": "I want to update a story."
                }]
    expected_logs = ["sprint_backlog", "product_backlog"]

    x_obj, x_log = reader.delete(id=3, log=expected_logs[0])
    y_obj, y_log = reader.delete(id=2, log=None)
    #reader.close() # omit close

    actual_objs = []
    actual_logs = []
    actual_objs.append(x_obj); actual_objs.append(y_obj)
    actual_logs.append(x_log); actual_logs.append(y_log)

    for i in range(2):
        assert expected_objs[i] == actual_objs[i]
        assert expected_logs[i] == actual_logs[i]
    
def test_update_story():
    reader = jr.json_reader(file_path="pytest_data/input3.json")
    new_objs = [{
                "id": 3,
                "priority": 3,
                "estimate": 4,
                "sprint": 2,
                "status": "to-do",
                "assigned_to": "Replaced customer name",
                "user_type": "customer",
                "story": "I want to update a story."
            },
            {
                "id": 5,
                "priority": 3,
                "estimate": 4,
                "sprint": 1,
                "status": "completed",
                "assigned_to": "Miley Cyrus",
                "user_type": "customer",
                "story": "I want to update a story."
            }]
    expected_logs = ["sprint_backlog", "previous_sprints"]

    x_obj, x_log = reader.update(id=3, new_entry=new_objs[0], log=expected_logs[0])
    y_obj, y_log = reader.update(id=5, new_entry=new_objs[1], log=None)
    #reader.close() # omit close

    actual_objs = []
    actual_logs = []
    actual_objs.append(x_obj); actual_objs.append(y_obj)
    actual_logs.append(x_log); actual_logs.append(y_log)

    for i in range(2):
        # update return the new entry and the log where the update occured
        assert new_objs[i] == actual_objs[i]
        assert expected_logs[i] == actual_logs[i]

def test_move_story():
    reader = jr.json_reader(file_path="pytest_data/input4.json")
    expected_obj, expected_log = reader.read(id=5)
    actual_obj, actual_src_log = reader.move(id=5, dest_log="archived")
    #reader.close()

    assert actual_obj == expected_obj
    assert actual_src_log == expected_log

def test_search():
    reader = jr.json_reader(file_path="data/scrum_board.json")
    expected_log = "current_sprint"
    expected_obj = {"id": 4,
            "priority": 3,
            "estimate": 4,
            "sprint": 2,
            "status": "in-progress",
            "assigned_to": "Hannah Montana",
            "user_type": "customer",
            "story": "I want to update a story." }
    list1 = reader.search(lookup="want to update", log="current_sprint")
    assert len(list1) == 1  # 1 entry found
    found1 = list1[0]       # Take entry out of list
    assert len(found1) == 2 # [obj, log]
    assert found1[0] == expected_obj
    assert found1[1] == expected_log

    ## test something that shows up in multiple places
    list2= reader.search(lookup="want to update")
    assert len(list2) == 4
    # Extract IDs
    actual_ids = []
    for tuple in list2:
        actual_ids.append(tuple[0]["id"])
    assert actual_ids == [2,3,4,5]

    ## test search using integer
    list3= reader.search(lookup=4, field="estimate")
    assert len(list3) == 3
    # Extract IDs
    actual_ids = []
    for tuple in list3:
        actual_ids.append(tuple[0]["id"])
    assert actual_ids == [3,4,5]

    ### test a bad search: you can find 4 in the ID field or estimate field
    list4= reader.search(lookup=4)
    assert len(list4) == 3
    # Extract IDs
    actual_ids = []
    for tuple in list4:
        actual_ids.append(tuple[0]["id"])
    assert actual_ids == [3,4,5]
    

def test_read_log():
    reader = jr.json_reader(file_path="data/scrum_board.json")

    expected_list = []
    for i in [1,2]: # Get ids 1,2 currently in the product backlog
        x_obj, _  = reader.read(id=i)
        expected_list.append(x_obj)

    expected_file = None
    with open(file="data/scrum_board.json", mode="r") as f:
        expected_file = json.load(f)

    actual_list = reader.read_log(log="product_backlog")
    actual_file = reader.read_log(log=None)
    #reader.close()

    assert expected_list == actual_list
    assert expected_file == actual_file