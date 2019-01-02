from wagtail.core.blocks import BaseStructBlock, Block

from ..exceptions import RemovedError


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

    def get_definition(self):
        definition = super(BaseStructBlock, self).get_definition()
        definition.update(
            isStruct=True,
            children=[child_block.get_definition()
                      for child_block in self.child_blocks.values()],
        )
        html = self.get_blocks_container_html()
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

    def prepare_for_react(self, parent_block, value,
                          type_name=None, errors=None):
        data = super(BaseStructBlock, self).prepare_for_react(
            parent_block, value, type_name=type_name, errors=errors)
        if errors is not None:
            data['html'] = self.get_blocks_container_html(errors=errors)
        return data

    def prepare_value(self, value, errors=None):
        children_errors = ({} if errors is None
                           else errors.as_data()[0].params)
        return [
            child_block.prepare_for_react(
                self, value.get(k, child_block.get_default()),
                type_name=k, errors=(None if children_errors is None
                                     else children_errors.get(k)))
            for k, child_block in self.child_blocks.items()]

    def value_omitted_from_data(self, *args, **kwargs):
        raise RemovedError
