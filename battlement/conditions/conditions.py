# coding: utf-8
import functools
from inspect import Signature
from typing import Callable, Any, Union, List


def precondition(check: Callable[[Any], bool], key: str, pos: int = None):
    """
    This function will check the preconditions of a parameter of the decorated function

    :param check: a lambda or function taking in a single value and returning a boolean
    :param key: named parameter to check with this precondition
    :param pos: the position if this parameter for this precondition is given positionally
    """

    def conditioner(func):
        @functools.wraps(func)
        def check_condition(*args, **kwargs):
            f_sig = [i[0] for i in Signature.from_callable(func).parameters.items()]
            try:
                v = kwargs[key]
            except KeyError:
                if pos:
                    v = args[pos]
                else:
                    v = args[f_sig.index(key)]

            if check(v):
                return func(*args, **kwargs)
            else:
                raise AssertionError(f"Precondition failed for {func.__name__}({key} = {v})")

        return check_condition

    return conditioner


def post_condition(check: Callable[[Any, Any], bool], cap_ctx: Union[List[str], str]):
    """
    Checks if the return value of a function is the expected one

    :param check: a callable that takes the context and the returned value and returns an bool
    :param cap_ctx: context to capture from calls to the function
    """

    def conditioner(func):
        @functools.wraps(func)
        def check_condition(*args, **kwargs):
            sig_params = {}
            f_sig = [i[0] for i in Signature.from_callable(func).parameters.items()]
            for (k, v) in Signature.from_callable(func).parameters.items():
                sig_params[k] = (k, v)

            old = {}
            if isinstance(cap_ctx, list):
                for ctx_i in cap_ctx:
                    try:
                        old[ctx_i] = kwargs[ctx_i]
                    except KeyError:
                        try:
                            old[ctx_i] = args[f_sig.index(sig_params[ctx_i][0])]
                        except IndexError:
                            old[ctx_i] = sig_params[ctx_i][1].default
            else:
                try:
                    old[cap_ctx] = kwargs[cap_ctx]
                except KeyError:
                    try:
                        old[cap_ctx] = args[sig_params[cap_ctx][0]]
                    except IndexError:
                        old[cap_ctx] = sig_params[cap_ctx][1].default

            new = func(*args, **kwargs)
            if check(old, new):
                return new
            else:
                raise AssertionError(
                    f"Post condition failed for {func.__name__} with an old context of {old}, returned {new}")

        return check_condition

    return conditioner
