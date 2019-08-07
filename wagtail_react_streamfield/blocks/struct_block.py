from uuid import uuid4

from django.utils.functional import cached_property
from wagtail.core.blocks import BaseStructBlock, Block

from ..exceptions import RemovedError
from ..widgets import BlockData


class NewBaseStructBlock(BaseStructBlock):
    def __init__(self, local_blocks=None, **kwargs):
        self._constructor_kwargs = kwargs

        Block.__init__(self, **kwargs)

        self.child_blocks = self.base_blocks.copy()
        if local_blocks:
            for name, block in local_blocks:
                block.set_name(name)
                self.child_blocks[name] = block

        self.dependencies = self.child_blocks.values()

    @cached_property
    def definition(self):
        definition = super(BaseStructBlock, self).definition
        definition.update(
            isStruct=True,
            children=[child_block.definition
                      for child_block in self.child_blocks.values()],
        )
        html = self.get_instance_html({})
        if html is not None:
            definition['html'] = html
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

    def prepare_value(self, value, errors=None):
        children_errors = ({} if errors is None
                           else errors.as_data()[0].params)
        prepared_value = []
        for k, child_block in self.child_blocks.items():
            child_errors = (None if children_errors is None
                            else children_errors.get(k))
            child_value = value.get(k, child_block.get_default())
            html = child_block.get_instance_html(child_value,
                                                 errors=child_errors)
            child_value = BlockData({
                'id': str(uuid4()),
                'type': k,
                'hasError': bool(child_errors),
                'value': child_block.prepare_value(child_value, errors=errors),
            })
            if html is not None:
                child_value['html'] = html
            prepared_value.append(child_value)
        return prepared_value

    def value_omitted_from_data(self, *args, **kwargs):
        raise RemovedError
