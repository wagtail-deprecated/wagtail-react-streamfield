from uuid import uuid4

from django.utils.text import capfirst
from wagtail.core.blocks import Block

from wagtail_react_streamfield.exceptions import RemovedError
from wagtail_react_streamfield.widgets import BlockData


class NewBlock(Block):
    SIMPLE = 'SIMPLE'
    COLLAPSIBLE = 'COLLAPSIBLE'

    def get_layout(self):
        return self.SIMPLE

    def prepare_value(self, value, errors=None):
        return value

    def prepare_for_react(self, parent_block, value,
                          type_name=None, errors=None):
        if type_name is None:
            type_name = self.name
        value = self.prepare_value(value, errors=errors)
        if parent_block is None:
            return value
        return BlockData({
            'id': str(uuid4()),
            'type': type_name,
            'hasError': bool(errors),
            'value': value,
        })

    def get_definition(self):
        definition = {
            'key': self.name,
            'label': capfirst(self.label),
            'required': self.required,
            'layout': self.get_layout(),
            'dangerouslyRunInnerScripts': True,
        }
        if self.meta.icon != Block._meta_class.icon:
            definition['icon'] = ('<i class="icon icon-%s"></i>'
                                  % self.meta.icon)
        if self.meta.classname is not None:
            definition['className'] = self.meta.classname
        if self.meta.group:
            definition['group'] = str(self.meta.group)
        return definition

    def all_html_declarations(self):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError
