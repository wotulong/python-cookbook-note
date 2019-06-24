from functools import partial, wraps
import logging

# 给装饰器附加属性，将函数func当成属性，附加给装饰器obj
def attach_wrapper(obj, func=None):
    if func is None:
        # partial 固定部分参数
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, msg=None):
    def decorate(func):
        logname = name if name is not None else func.__module__
        log = logging.getLogger(logname)
        logmsg = msg if msg is not None else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            print("logedd name=%s, level=%d, msg=%s" % (logname, level, logmsg))
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        # wrapper为需要附加属性的方法
        def set_level(new_level):
            # nonlocal 外部变量
            nonlocal level
            level = new_level

        @attach_wrapper(wrapper)
        def set_msg(new_msg):
            nonlocal logmsg
            logmsg = new_msg

        return wrapper
    return decorate

@logged(logging.WARNING, name="log", msg="old msg")
def add_two(a, b):
    print(a + b)


add_two(1, 2)

add_two.set_level(logging.ERROR)
add_two.set_msg("new msg")

add_two(3, 4)


