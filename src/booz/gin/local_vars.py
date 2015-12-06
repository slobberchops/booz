# Copyright 2015 Rafe Kaplan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .. import util
from .. import whiskey


class GetAttr(whiskey.Action):

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def invoke(self, *args, locals=None, **kwargs):
        if locals is None:
            raise TypeError('Must provide \'locals\' parameter')
        return getattr(locals, whiskey.invoke(self.__name, *args, locals=locals, **kwargs))

    def __getitem__(self, value):
        return SetAttr(self.__name, value)


class SetAttr(whiskey.Action):

    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    def invoke(self, *args, locals = None, **kwargs):
        if locals is None:
            raise TypeError('Must provide \'locals\' parameter')
        value = whiskey.invoke(self.__value)
        setattr(locals, whiskey.invoke(self.__name), value)
        return value


@util.singleton
class l:

    def __getattr__(self, name):
        return GetAttr(name)


class Vars:

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            raise ValueError('Invalid variable name "{}"'.format(name))
        self.__dict__[name] = value

    def __dir__(self):
        result = []
        for name in sorted(self.__dict__.keys()):
            if not name.startswith('_') or name:
                result.append(name)
        return result

    def __iter__(self):
        for name in dir(self):
            yield name, getattr(self, name)

    def __eq__(self, other):
        if not isinstance(other, Vars):
            return NotImplemented
        else:
            return list(self) == list(other)

    def __str__(self):
        vars = ', '.join(dir(self))
        return '<Vars {}>'.format(vars) if vars else '<Vars>'

    __repr__ = __str__


class LocalScope:

    def __init__(self, *args, **kwargs):
        self.__args = args
        self.__kwargs = kwargs
        self.__vars = Vars()

    @property
    def args(self):
        return self.__args

    @property
    def kwargs(self):
        return dict(self.__kwargs)

    @property
    def vars(self):
        return self.__vars
