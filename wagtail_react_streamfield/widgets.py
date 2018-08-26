import json
from uuid import uuid4

from django.forms import Media
from django.utils.safestring import mark_safe
from wagtail.core.blocks import (
    BlockWidget, StructBlock, ListBlock, FieldBlock, RichTextBlock,
    StreamBlock,
)


def to_json_script(data):
    return json.dumps(data).replace('<', '\\u003c')


class NewBlockWidget(BlockWidget):
    def prepare_value(self, parent_block, block, value, type_name=None,
                      errors=None):
        if type_name is None:
            type_name = block.name
        if isinstance(block, StructBlock):
            children_errors = ({} if errors is None
                               else errors.as_data()[0].params)
            value = [self.prepare_value(block, block.child_blocks[k], v,
                                        type_name=k,
                                        errors=children_errors.get(k))
                     for k, v in value.items()
                     if k in block.child_blocks]
        elif isinstance(block, ListBlock):
            children_errors = ([None] * len(value) if errors is None
                               else errors.as_data()[0].params)
            value = [self.prepare_value(block, block.child_block,
                                        child_block_data, type_name=block.name,
                                        errors=child_errors)
                     for child_block_data, child_errors
                     in zip(value, children_errors)]
        elif isinstance(block, StreamBlock):
            children_errors = ({} if errors is None
                               else errors.as_data()[0].params)
            value = [self.prepare_value(block, child_block_data.block,
                                        child_block_data.value,
                                        errors=children_errors.get(i))
                     for i, child_block_data in enumerate(value)]
        if parent_block is None:
            return value
        data = {
            'type': type_name,
            'hasError': bool(errors),
        }
        if isinstance(block, FieldBlock):
            from wagtail.admin.rich_text import DraftailRichTextArea
            data.update(
                id=str(uuid4()),
                html=block.render_form(value, prefix='field-__ID__',
                                       errors=errors),
            )
            if value == '':
                value = None
            value = block.value_for_form(block.field.prepare_value(value))
            if isinstance(block, RichTextBlock) \
                    and isinstance(block.field.widget, DraftailRichTextArea):
                value = block.field.widget.translate_value(value)
        data['value'] = value
        return data

    def render_with_errors(self, name, value, attrs=None, errors=None):
        streamfield_config = {
            'required': self.block_def.required,
            'minNum': self.block_def.meta.min_num,
            'maxNum': self.block_def.meta.max_num,
            'blockDefinitions': self.block_def.get_definition()['children'],
            'value': self.prepare_value(None,
                                        self.block_def, value, errors=errors),
        }
        return mark_safe("""
        <script type="application/json" data-streamfield="%s">%s</script>
        """ % (name, to_json_script(streamfield_config)))

    @property
    def media(self):
        return self.block_def.all_media() + Media(
            js=['js/wagtail-react-streamfield.js'],
            css={'all': [
                'css/wagtail-react-streamfield.css',
                'css/wagtail-react-streamfield-extra.css',
                'https://use.fontawesome.com/releases/v5.1.0/css/all.css'
            ]})

    def value_from_datadict(self, data, files, name):
        stream_field_data = json.loads(data.get(name))
        return super().value_from_datadict({'value': stream_field_data},
                                           files, name)
