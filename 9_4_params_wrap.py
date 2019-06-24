from functools import wraps
import logging


def logged(level, name=None, msg=None):
    '''
    # 带参数装饰器
    :param level:
    :param name:
    :param msg:
    :return:
    '''
    def decorate(func):
        '''
        # 装饰器外包函数
        :param func:
        :return:
        '''
        logname = name if name is not None else func.__module__
        log = logging.getLogger(logname)
        logmsg = msg if msg is not None else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            '''
            # 装饰器函数，直接传入所有参数给所包装的函数
            :param args:
            :param kwargs:
            :return:
            '''
            print("loged msg=%s" %logmsg)
            log.log(level, logmsg)
            return func(*args, **kwargs)

        return wrapper
    return decorate


@logged(logging.WARNING)
def added(a, b):
    print(a + b)


added(1, 3)