"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

from logging import getLogger
from queue import Queue
from time import time
from os import getenv
from .params import PARAMS


log = getLogger("module")

data_queue = Queue(maxsize = PARAMS['WINDOW_SIZE'])
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
    return not PARAMS['SEND_ON_CHANGE'] or (PARAMS['SEND_ON_CHANGE'] and data != last_stable_data)


def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    global data_queue, last_stable_data

    try:
        if type(received_data) is dict:
            safely_add_data_to_queue(
                data_queue, received_data[PARAMS['INPUT_LABEL']])
        elif type(received_data) is list:
            for item in received_data:
                safely_add_data_to_queue(data_queue, item[PARAMS['INPUT_LABEL']])

        if data_queue.full():
            if is_stable_value(data_queue):
                if (can_send_data(data_queue.queue[0])):
                    last_stable_data = data_queue.queue[0]
                    empty_queue(data_queue)

                    return_body = {
                        PARAMS['INPUT_LABEL']: last_stable_data,
                        f"{getenv('MODULE_NAME')}Time": time()
                    }

                    return return_body, None
                else:
                    data_queue.get()

        return None, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"
