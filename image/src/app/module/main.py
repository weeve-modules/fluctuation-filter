"""
All logic related to the module's main application
Mostly only this file requires changes
"""

from app.config import APPLICATION
from app.weeve.egress import send_data


window_data = []
stable_data = None
previous_window_data = None

def processing():
    global window_data
    global stable_data
    global previous_window_data

    flag = True
   
    if len(window_data) == APPLICATION['WINDOW_SIZE']:
        for index in range(len(window_data) - 1):
            if window_data[index] != window_data[index + 1]:
                flag = False
        
        if flag:
            stable_data = window_data[-1]
            
        if APPLICATION['SEND_ON_CHANGE']:
            if previous_window_data == None and stable_data != None:
                send_data(stable_data[APPLICATION['INPUT_LABEL']])
                previous_window_data = stable_data
               
            else:
                if previous_window_data != stable_data:
                    send_data(stable_data[APPLICATION['INPUT_LABEL']])
                    previous_window_data = stable_data
        
        else:
            if stable_data != None:
                send_data(stable_data[APPLICATION['INPUT_LABEL']])
        
        if len(window_data) > 0:
            window_data[:] = window_data[1:]

def module_main(data):
    """implement module logic here

    Args:
        parsed_data ([JSON Object]): [Data received by the module and validated by data_validation function]

    Returns:
        [string, string]: [data, error]
    """
    try:
        global window_data

        if type(data) == dict:
            window_data.append(data)
            processing()
        elif type(data) == list:
            for d in data:
                window_data.append(d)
                processing()
        
        return None, None
    except Exception:
        return None, "Unable to perform the module logic"
