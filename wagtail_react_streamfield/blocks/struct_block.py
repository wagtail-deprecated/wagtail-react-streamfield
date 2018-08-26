from wagtail.core.blocks import BaseStructBlock

from ..exceptions import RemovedError


class NewBaseStructBlock(BaseStructBlock):
    def get_definition(self):
        definition = super(BaseStructBlock, self).get_definition()
        definition.update(
            isStruct=True,
            children=[child_block.get_definition()
                      for child_block in self.child_blocks.values()],
        )
        for child_definition in definition['children']:
            if 'titleTemplate' in child_definition:
                definition['titleTemplate'] = child_definition['titleTemplate']
                break
        return definition

    def js_initializer(self):
        raise RemovedError

    def get_form_context(self, *args, **kwargs):
        raise RemovedError

    def render_form(self, *args, **kwargs):
        raise RemovedError

    def value_from_datadict(self, data, files, prefix):
        return self._to_struct_value([
            (child_block_data['type'],
             self.child_blocks[child_block_data['type']].value_from_datadict(
                 child_block_data, files, prefix,
             ))
            for child_block_data in data['value']
            if child_block_data['type'] in self.child_blocks
        ])

    def value_omitted_from_data(self, *args, **kwargs):
        raise RemovedError
