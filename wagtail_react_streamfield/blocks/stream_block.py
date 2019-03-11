from uuid import uuid4

from wagtail.core.blocks import BaseStreamBlock, StreamValue

from ..exceptions import RemovedError


class NewBaseStreamBlock(BaseStreamBlock):
    def get_definition(self):
        definition = super(BaseStreamBlock, self).get_definition()
        definition.update(
            children=[
                child_block.get_definition()
                for child_block in self.child_blocks.values()
            ],
            minNum=self.meta.min_num,
            maxNum=self.meta.max_num,
        )
        html = self.get_blocks_container_html()
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

    def prepare_for_react(self, parent_block, value,
                          type_name=None, errors=None):
        data = super(BaseStreamBlock, self).prepare_for_react(
            parent_block, value, type_name=type_name, errors=errors)
        if parent_block is not None and errors is not None:
            data['html'] = self.get_blocks_container_html(errors=errors)
        return data

    def prepare_value(self, value, errors=None):
        if value is None:
            return []
        children_errors = ({} if errors is None
                           else errors.as_data()[0].params)
        return [
            child_block_data.block.prepare_for_react(
                self, child_block_data, errors=children_errors.get(i))
            for i, child_block_data in enumerate(value)]

    def value_omitted_from_data(self, data, files, prefix):
        return data.get('value') is None
