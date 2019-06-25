from inspect import signature as sig
from functools import wraps


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        if not __debug__:
            return func

        fun_sig = sig(func)
        # 将签名与参数字典绑定
        bound_types = fun_sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 参数顺序字典
            bound_values = fun_sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate

# 限定第一个和第三个参数为str
@typeassert(str, z=str)
def add_three(x, y, z):
    print(x + str(y) + z)

# 正常情况
add_three("x", 2, "z")


# 触发异常
add_three(1, 2, 3)