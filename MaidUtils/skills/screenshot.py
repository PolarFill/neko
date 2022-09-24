def runSave():
    import pyscreeze, datetime, os
    import platform
    from config import path

    if os.path.isdir(f'{path}/UserData/Userspace/Screenshots') == False:
        os.mkdir(f'{path}/UserData/Userspace/Screenshots')
        
    pyscreeze.screenshot('{}/UserData/Screenshots/Screenshot-{}.png'.format(path, datetime.datetime.now()))