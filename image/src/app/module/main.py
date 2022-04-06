"""
All logic related to the module's main application
Mostly only this file requires changes
"""

from app.config import APPLICATION
#from app.weeve.egress import send_data
from queue import Queue

data_queue = Queue(maxsize = APPLICATION['WINDOW_SIZE'])
last_stable_data = None

def safely_add_data_to_queue(queue, data) -> None:
    """
    This function is called by the main function to add data to the queue.
    :param queue: The queue to add the data to
    :param data: The data to be added to the queue
    """
    if queue.full():
        queue.get()
    queue.put(data)


def empty_queue(queue) -> None:
    """
    Remove all elements from the queue

    :param queue: The queue to be emptied
    """
    while not queue.empty():
        queue.get()


def is_stable_value(queue) -> bool:
    """
    Return True if all items in the queue are equal to the first item in the queue

    :param queue: A queue of items
    :return: True if the queue is stable, False otherwise.
    """
    return all(item == queue.queue[0] for item in queue.queue)


def can_send_data(data) -> bool:
    """
    This function is called by the main function to check if the data should be sent to the next module.
    if __SEND_ON_CHANGE__ is set to True and data is different form last data.
    :param data: The data to be checked
    :return: True if the data should be sent, False otherwise
    """
    return not APPLICATION['SEND_ON_CHANGE'] or (APPLICATION['SEND_ON_CHANGE'] and data != last_stable_data)


def module_main(received_data):
    """implement module logic here
    Args:
        parsed_data ([JSON Object]): [Data received by the module and validated by data_validation function]
    Returns:
        [string, string]: [data, error]
    """
    global data_queue, last_stable_data

    try:
        if type(received_data) is dict:
            safely_add_data_to_queue(
                data_queue, received_data[APPLICATION['INPUT_LABEL']])
        elif type(received_data) is list:
            for item in received_data:
                safely_add_data_to_queue(data_queue, item[APPLICATION['INPUT_LABEL']])

        if data_queue.full():
            if is_stable_value(data_queue):
                if (can_send_data(data_queue.queue[0])):
                    last_stable_data = data_queue.queue[0]
                    empty_queue(data_queue)  
                    return last_stable_data, None
                else:
                    data_queue.get()

        return None, None
    except Exception as e:
        return None, str(e)
