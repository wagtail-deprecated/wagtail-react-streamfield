import json
from uuid import uuid4

from django.core.exceptions import NON_FIELD_ERRORS
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import Media
from django.utils.safestring import mark_safe
from wagtail.core.blocks import (
    BlockWidget, StructBlock, ListBlock, FieldBlock, StreamBlock,
)

from .constants import FIELD_NAME_TEMPLATE


class ConfigJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, BlockData):
            return o.data
        return super().default(o)


class InputJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, BlockData):
            return {'id': o['id'],
                    'type': o['type'],
                    'value': o['value']}
        return super().default(o)


def to_json_script(data, encoder=ConfigJSONEncoder):
    return json.dumps(
        data, separators=(',', ':'), cls=encoder
    ).replace('<', '\\u003c')


class BlockData:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value


class NewBlockWidget(BlockWidget):
    def prepare_value(self, parent_block, block, value, type_name=None,
                      errors=None):
        if type_name is None:
            type_name = block.name
        if isinstance(block, StructBlock):
            children_errors = ({} if errors is None
                               else errors.as_data()[0].params)
            value = [
                self.prepare_value(
                    block, block.child_blocks[k], v, type_name=k,
                    errors=children_errors.get(k))
                for k, v in value.items()
                if k in block.child_blocks]
        elif isinstance(block, ListBlock):
            children_errors = (None if errors is None
                               else errors.as_data()[0].params)
            if children_errors is None:
                children_errors = [None] * len(value)
            value = [
                self.prepare_value(
                    block, block.child_block, child_block_data,
                    errors=child_errors)
                for child_block_data, child_errors
                in zip(value, children_errors)]
        elif isinstance(block, StreamBlock):
            children_errors = ({} if errors is None
                               else errors.as_data()[0].params)
            value = [
                self.prepare_value(
                    block, child_block_data.block, child_block_data.value,
                    errors=children_errors.get(i))
                for i, child_block_data in enumerate(value)]
        if parent_block is None:
            return value
        data = BlockData({
            'id': str(uuid4()),
            'type': type_name,
            'hasError': bool(errors),
        })
        if isinstance(block, FieldBlock):
            if errors:
                data['html'] = block.render_form(
                    value, prefix=FIELD_NAME_TEMPLATE, errors=errors)
            if value == '':
                value = None
            value = block.prepare_for_react(value)
        data['value'] = value
        return data

    def get_actions_icons(self):
        return {
            'moveUp': '<i class="icon icon-arrow-up"></i>',
            'moveDown': '<i class="icon icon-arrow-down"></i>',
            'duplicate': '<i class="icon icon-duplicate"></i>',
            'delete': '<i class="icon icon-bin"></i>',
            'grip': '<i class="icon icon-grip"></i>',
        }

    def render_with_errors(self, name, value, attrs=None, errors=None,
                           renderer=None):
        streamfield_config = {
            'required': self.block_def.required,
            'minNum': self.block_def.meta.min_num,
            'maxNum': self.block_def.meta.max_num,
            'icons': self.get_actions_icons(),
            'blockDefinitions': self.block_def.get_definition()['children'],
            'value': self.prepare_value(None,
                                        self.block_def, value, errors=errors),
        }
        escaped_value = to_json_script(streamfield_config['value'],
                                       encoder=InputJSONEncoder)
        non_block_errors = (
            () if errors is None
            else errors.as_data()[0].params.get(NON_FIELD_ERRORS, ()))
        non_block_errors = ''.join([
            mark_safe('<div class="help-block help-critical">%s</div>') % error
            for error in non_block_errors])
        return mark_safe("""
        <script type="application/json" data-streamfield="%s">%s</script>
        <textarea style="display: none;" name="%s">%s</textarea>
        %s
        """ % (name, to_json_script(streamfield_config),
               name, escaped_value, non_block_errors))

    @property
    def media(self):
        return self.block_def.all_media() + Media(
            js=['js/wagtail-react-streamfield.js'],
            css={'all': [
                'css/wagtail-react-streamfield.css',
            ]})

    def value_from_datadict(self, data, files, name):
        stream_field_data = json.loads(data.get(name))
        return super().value_from_datadict({'value': stream_field_data},
                                           files, name)
