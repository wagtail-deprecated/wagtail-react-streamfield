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
             child_block_data['id'])
            for child_block_data in data['value']
            if child_block_data['type'] in self.child_blocks
        ])

    def value_omitted_from_data(self, data, files, prefix):
        return data.get('value') is None
