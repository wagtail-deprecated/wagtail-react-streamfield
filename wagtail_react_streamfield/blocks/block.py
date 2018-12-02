from django.utils.text import capfirst
from wagtail.core.blocks import Block

from wagtail_react_streamfield.exceptions import RemovedError


class NewBlock(Block):
    SIMPLE = 'SIMPLE'
    COLLAPSIBLE = 'COLLAPSIBLE'

    def get_layout(self):
        return self.SIMPLE

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
