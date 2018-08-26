from django.utils.text import capfirst
from wagtail.core.blocks import Block

from wagtail_react_streamfield.exceptions import RemovedError


class NewBlock(Block):
    def get_definition(self):
        definition = {
            'key': self.name,
            'label': capfirst(self.label),
            'required': self.required,
            'dangerouslyRunInnerScripts': True,
        }
        if self.meta.icon != Block._meta_class.icon:
            definition['icon'] = ('<i class=\"icon icon-%s\"></i>'
                                  % self.meta.icon)
        if self.meta.classname is not None:
            definition['className'] = self.meta.classname
        return definition

    def all_html_declarations(self):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError
