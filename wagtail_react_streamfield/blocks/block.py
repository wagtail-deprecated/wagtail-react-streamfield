from uuid import uuid4

from django.template.loader import render_to_string
from django.utils.text import capfirst
from wagtail.core.blocks import Block, StreamValue

from wagtail_react_streamfield.exceptions import RemovedError
from wagtail_react_streamfield.widgets import BlockData, get_non_block_errors


class NewBlock(Block):
    FIELD_NAME_TEMPLATE = 'field-__ID__'

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
        if isinstance(value, StreamValue.StreamChild):
            block_id = value.id
            value = value.value
        else:
            block_id = str(uuid4())
        value = self.prepare_value(value, errors=errors)
        if parent_block is None:
            return value
        return BlockData({
            'id': block_id,
            'type': type_name,
            'hasError': bool(errors),
            'value': value,
        })

    def get_blocks_container_html(self, errors=None):
        help_text = getattr(self.meta, 'help_text', None)
        non_block_errors = get_non_block_errors(errors)
        if help_text or non_block_errors:
            return render_to_string(
                'wagtailadmin/block_forms/blocks_container.html',
                {
                    'help_text': help_text,
                    'non_block_errors': non_block_errors,
                }
            )

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
        if self.meta.default:
            definition['default'] = self.prepare_value(self.get_default())
        return definition

    def all_html_declarations(self):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError
