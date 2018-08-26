from wagtail.core.blocks import ListBlock

from ..exceptions import RemovedError


class NewListBlock(ListBlock):
    def render_list_member(self, *args, **kwargs):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError

    def js_initializer(self):
        raise RemovedError

    def render_form(self, *args, **kwargs):
        raise RemovedError

    def value_from_datadict(self, data, files, prefix):
        return [
            self.child_block.value_from_datadict(child_block_data, files,
                                                 prefix)
            for child_block_data in data['value']]

    def value_omitted_from_data(self, *args, **kwargs):
        raise RemovedError
