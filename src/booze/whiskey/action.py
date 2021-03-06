# Copyright 2015 Rafe Kaplan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import operator

from .. import util


class Action:

    def invoke(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return Call(self, *args, **kwargs)

    def __pos__(self):
        return pos_(self)

    def __neg__(self):
        return neg_(self)

    def __invert__(self):
        return invert_(self)

    # Comparison operators
    def __lt__(self, other):
        return lt_(self, other)

    def __le__(self, other):
        return le_(self, other)

    def __eq__(self, other):
        return eq_(self, other)

    def __ne__(self, other):
        return ne_(self, other)

    def __ge__(self, other):
        return ge_(self, other)

    def __gt__(self, other):
        return gt_(self, other)

    # Mathmatical operators
    def __add__(self, other):
        return add_(self, other)

    def __iadd__(self, other):
        return iadd_(self, other)

    def __sub__(self, other):
        return sub_(self, other)

    def __isub__(self, other):
        return isub_(self, other)

    def __mul__(self, other):
        return mul_(self, other)

    def __imul__(self, other):
        return imul_(self, other)

    def __floordiv__(self, other):
        return floordiv_(self, other)

    def __ifloordiv__(self, other):
        return ifloordiv_(self, other)

    def __mod__(self, other):
        return mod_(self, other)

    def __imod__(self, other):
        return imod_(self, other)

    def __pow__(self, other):
        return pow_(self, other)

    def __ipow__(self, other):
        return ipow_(self, other)

    def __truediv__(self, other):
        return truediv_(self, other)

    def __itruediv__(self, other):
        return itruediv_(self, other)

    # Bitwise functions
    def __and__(self, other):
        return and__(self, other)

    def __iand__(self, other):
        return iand_(self, other)

    def __or__(self, other):
        return or__(self, other)

    def __ior__(self, other):
        return ior_(self, other)

    def __lshift__(self, other):
        return lshift_(self, other)

    def __ilshift__(self, other):
        return ilshift_(self, other)

    def __rshift__(self, other):
        return rshift_(self, other)

    def __irshift__(self, other):
        return irshift_(self, other)

    def __xor__(self, other):
        return xor_(self, other)

    def __ixor__(self, other):
        return ixor_(self, other)


def invoke(value, *args, **kwargs):
    if isinstance(value, Action):
        return value.invoke(*args, **kwargs)
    else:
        return value


class Arg(Action):

    def __init__(self, index):
        self.__index = index

    @property
    def index(self):
        return self.__index

    def invoke(self, *args, **kwargs):
        index = invoke(self.__index, *args, **kwargs)
        try:
            return args[index]
        except IndexError:
            raise TypeError('Positional argument {} out of range'.format(index))


class KwArg(Action):

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def invoke(self, *args, **kwargs):
        return kwargs[self.__name]


@util.singleton
class p:

    def __getitem__(self, index):
        if isinstance(index, int):
            return Arg(index)
        elif isinstance(index, str):
            return KwArg(index)
        else:
            raise TypeError('Index must be int or str')

    def __getattr__(self, name):
        return KwArg(name)


class Call(Action):

    def __init__(self, real_func, *args, **kwargs):
        self.__func = real_func
        self.__args = args
        self.__kwargs = kwargs

    @property
    def func(self):
        return self.__func

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return dict(self.__kwargs)

    def invoke(self, *args, **kwargs):
        real_func = invoke(self.__func, *args, **kwargs)
        args = [invoke(a, *args, **kwargs) for a in self.args]
        kwargs = {k: invoke(v, *args, **kwargs) for k, v in self.kwargs.items()}
        return real_func(*args, **kwargs)


def func(real_func):
    class Func(Call):

        __func__ = real_func

        def __init__(self, *args, **kwargs):
            super(Func, self).__init__(real_func, *args, **kwargs)
    return Func


# Unary functions
pos_ = func(operator.pos)
neg_ = func(operator.neg)
invert_ = func(operator.invert)
abs_ = func(operator.abs)

# Comparison functions
lt_ = func(operator.lt)
le_ = func(operator.le)
eq_ = func(operator.eq)
ne_ = func(operator.ne)
ge_ = func(operator.ge)
gt_ = func(operator.gt)

# Mathematical functions
add_ = func(operator.add)
iadd_ = func(operator.iadd)
sub_ = func(operator.sub)
isub_ = func(operator.isub)
mul_ = func(operator.mul)
imul_ = func(operator.imul)
floordiv_ = func(operator.floordiv)
ifloordiv_ = func(operator.ifloordiv)
mod_ = func(operator.mod)
imod_ = func(operator.imod)
pow_ = func(operator.pow)
ipow_ = func(operator.ipow)
truediv_ = func(operator.truediv)
itruediv_ = func(operator.itruediv)

# Bitwise functions
and__ = func(operator.and_)
iand_ = func(operator.iand)
or__ = func(operator.or_)
ior_ = func(operator.ior)
lshift_ = func(operator.lshift)
ilshift_ = func(operator.ilshift)
rshift_ = func(operator.rshift)
irshift_ = func(operator.irshift)
xor_ = func(operator.xor)
ixor_ = func(operator.ixor)
