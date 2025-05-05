# config.py //configure
value = True
def init():
    global value
    value = True

def set(x):
    global value
    value = x

def get():
    global value
    return value
