from uuid import uuid4

from django.utils.functional import cached_property
from wagtail.core.blocks import BaseStreamBlock, StreamValue

from ..exceptions import RemovedError
from ..widgets import BlockData


class NewBaseStreamBlock(BaseStreamBlock):
    @cached_property
    def definition(self):
        definition = super(BaseStreamBlock, self).definition
        definition.update(
            children=[
                child_block.definition
                for child_block in self.child_blocks.values()
            ],
            minNum=self.meta.min_num,
            maxNum=self.meta.max_num,
        )
        html = self.get_instance_html([])
        if html is not None:
            definition['html'] = html
        return definition

    def sorted_child_blocks(self):
        raise RemovedError

    def render_list_member(self, *args, **kwargs):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError

    def js_initializer(self):
        raise RemovedError

    def render_form(self, *args, **kwargs):
        raise RemovedError

    def value_from_datadict(self, data, files, prefix):
        return StreamValue(self, [
            (child_block_data['type'],
             self.child_blocks[child_block_data['type']].value_from_datadict(
                 child_block_data, files, prefix,
             ),
             child_block_data.get('id', str(uuid4())))
            for child_block_data in data['value']
            if child_block_data['type'] in self.child_blocks
        ])

    def prepare_value(self, value, errors=None):
        if value is None:
            return []
        children_errors = ({} if errors is None
                           else errors.as_data()[0].params)
        prepared_value = []
        for i, stream_child in enumerate(value):
            child_errors = children_errors.get(i)
            child_block = stream_child.block
            child_value = stream_child.value
            html = child_block.get_instance_html(child_value,
                                                 errors=child_errors)
            child_value = BlockData({
                'id': stream_child.id or str(uuid4()),
                'type': child_block.name,
                'hasError': bool(child_errors),
                'value': child_block.prepare_value(child_value,
                                                   errors=child_errors),
            })
            if html is not None:
                child_value['html'] = html
            prepared_value.append(child_value)
        return prepared_value

    def value_omitted_from_data(self, data, files, prefix):
        return data.get('value') is None
