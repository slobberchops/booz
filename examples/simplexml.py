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

from booze.gin import *
from booze.whiskey import *

@func
def xml_doc(name, children=()):
    return (name, children) if children else (name,)


start_tag = Rule(AttrType.STRING)
end_tag = Rule(AttrType.UNUSED)
empty_tag = Rule(AttrType.STRING)
xml = Rule()
document = Rule(AttrType.OBJECT)

tag_name = lexeme[+alpha]

start_tag %= '<' << tag_name << '>'
end_tag   %= omit['</' << String(p[0]) << '>']
empty_tag %= '<' << tag_name << '/>'
xml       %= ((start_tag[l.name[p[0]]] << -+xml << end_tag(l.name))  [xml_doc(p[0], p[1])]
           | empty_tag                                               [xml_doc(p[0])])
document  %= xml << eoi

if __name__ == '__main__':
    import io

    def print_xml(unparsed_string, xml_parser=document):
        s = io.StringIO(unparsed_string)
        print(unparsed_string, '=', xml_parser.parse(s, ' \n')[1])
        remaining = s.read()
        if remaining:
            print('Parse Error: "{}"'.format(remaining))

    print_xml('<document></document>')
    print_xml("""
            <document>
                <a/>
                <b>
                    <c/>
                </b>
            </document>
            """)
