import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# print('this')
# logging.debug('A debug message!')

TO_SHOW = True
def to_show_output_debug(show: bool = True):
    global TO_SHOW
    TO_SHOW = show

def debug_print(message: str):
    global TO_SHOW
    if not TO_SHOW:
        return
    logging.debug(" " + message)

def info_print(message: str):
    global TO_SHOW
    if not TO_SHOW:
        return
    logging.info(message)