import json
from uuid import uuid4

from django.forms import Media
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from wagtail.core.blocks import (
    BlockWidget, StructBlock, ListBlock, FieldBlock, RichTextBlock,
    StreamBlock, Block, CharBlock, TextBlock, FloatBlock, DecimalBlock,
    RegexBlock, URLBlock, DateBlock, TimeBlock, DateTimeBlock, EmailBlock,
    IntegerBlock, StreamValue,
)


def to_json_script(data):
    return json.dumps(data).replace('<', '\\u003c')


def react_to_wagtail_data(block, block_data):
    block_value = block_data['value']
    if isinstance(block, StreamBlock):
        return StreamValue(block, [
            (child_block_data['type'],
             react_to_wagtail_data(
                 block.child_blocks[child_block_data['type']],
                 child_block_data),
             child_block_data['id'])
            for child_block_data in block_value
        ])
    if isinstance(block, StructBlock):
        return block._to_struct_value([
            (child_block_data['type'],
             react_to_wagtail_data(
                 block.child_blocks[child_block_data['type']],
                 child_block_data,
             ))
            for child_block_data in block_data['value']
        ])
    if isinstance(block, ListBlock):
        return [react_to_wagtail_data(
            block.child_block, child_block_data)
            for child_block_data in block_data['value']]
    if block_value == '':
        block_value = None
    return block.value_from_datadict({'value': block_value}, {}, 'value')


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
                     for k, v in value.items()]
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
        }
        if isinstance(block, FieldBlock):
            from wagtail.admin.rich_text import DraftailRichTextArea
            name = 'field-%s' % uuid4()
            data.update(
                name=name,
                html=block.render_form(value, prefix=name, errors=errors),
            )
            if value == '':
                value = None
            value = block.value_for_form(block.field.prepare_value(value))
            if isinstance(block, RichTextBlock) \
                    and isinstance(block.field.widget, DraftailRichTextArea):
                value = block.field.widget.translate_value(value)
        data['value'] = value
        return data

    @staticmethod
    def get_title_template(key, block):
        if isinstance(block, (CharBlock, TextBlock, FloatBlock,
                              DecimalBlock, RegexBlock, URLBlock,
                              DateBlock, TimeBlock, DateTimeBlock,
                              EmailBlock, IntegerBlock)):
            return '${%s}' % key

    @classmethod
    def get_definition(cls, key, block):
        block_definition = {
            'key': key,
            'label': capfirst(block.label),
            'required': block.required,
            'dangerouslyRunInnerScripts': True,
        }
        if block.meta.icon != Block._meta_class.icon:
            block_definition['icon'] = ('<i class=\"icon icon-%s\"></i>'
                                        % block.meta.icon),
        if block.meta.classname is not None:
            block_definition['className'] = block.meta.classname
        if isinstance(block, FieldBlock):
            block_definition['html'] = block.render_form(
                block.to_python(None), prefix=block.name)
            title_template = cls.get_title_template(block.name, block)
            if title_template is not None:
                block_definition['titleTemplate'] = title_template
        elif isinstance(block, StructBlock):
            block_definition['isStruct'] = True
            block_definition['children'] = [
                cls.get_definition(k, b)
                for k, b in block.child_blocks.items()
            ]
            for child_block_key, child_block in block.child_blocks.items():
                title_template = cls.get_title_template(child_block_key,
                                                         child_block)
                if title_template is not None:
                    block_definition['titleTemplate'] = title_template
                    break
        elif isinstance(block, ListBlock):
            block_definition['children'] = [
                cls.get_definition(block.name, block.child_block),
            ]
        elif isinstance(block, StreamBlock):
            block_definition['children'] = [
                cls.get_definition(k, b)
                for k, b in block.child_blocks.items()
            ]
        return block_definition

    def render_with_errors(self, name, value, attrs=None, errors=None):
        streamfield_config = {
            'blockDefinitions': [
                self.get_definition(key, block)
                for key, block in self.block_def.child_blocks.items()
            ],
            'value': self.prepare_value(None, self.block_def, value,
                                        errors=errors),
        }
        return mark_safe("""
        <script type="application/json" data-streamfield="%s">%s</script>
        """ % (name, to_json_script(streamfield_config)))

    @property
    def media(self):
        return Media(
            js=['js/wagtail-react-streamfield.js'],
            css={'all': [
                'css/wagtail-react-streamfield.css',
                'css/wagtail-react-streamfield-extra.css',
                'https://use.fontawesome.com/releases/v5.1.0/css/all.css'
            ]})

    def value_from_datadict(self, data, files, name):
        stream_field_data = json.loads(data.get(name))
        return react_to_wagtail_data(self.block_def,
                                     {'value': stream_field_data})
