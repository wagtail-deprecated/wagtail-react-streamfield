from django.utils.six import wraps
from wagtail.core.blocks import (
    BlockField, Block, BaseStreamBlock, ListBlock, BaseStructBlock, FieldBlock,
)

from .blocks.block import NewBlock
from .blocks.field_block import NewFieldBlock
from .blocks.list_block import NewListBlock
from .blocks.stream_block import NewBaseStreamBlock
from .blocks.struct_block import NewBaseStructBlock
from .widgets import NewBlockWidget


def _patch_with(original_class, new_class, *method_names):
    for method_name in method_names:

        def patch_original(original_method, new_method):
            @wraps(original_method)
            def inner(*args, **kwargs):
                return new_method(*args, **kwargs)
            return inner

        original_method = getattr(original_class, method_name)
        new_method = getattr(new_class, method_name)
        setattr(original_class, method_name,
                patch_original(original_method, new_method))


def _patch_streamfield_panel():
    from wagtail.admin.edit_handlers import StreamFieldPanel
    from .edit_handlers import NewStreamFieldPanel

    _patch_with(StreamFieldPanel, NewStreamFieldPanel, 'html_declarations')


def _patch_block_widget():
    def patch_init(original):
        @wraps(original)
        def inner(self, block=None, **kwargs):
            if 'widget' not in kwargs:
                kwargs['widget'] = NewBlockWidget(block)
            original(self, block=block, **kwargs)
        return inner

    BlockField.__init__ = patch_init(BlockField.__init__)


def patch():
    _patch_streamfield_panel()
    _patch_block_widget()
    _patch_with(Block, NewBlock,
                'html_declarations', 'all_html_declarations')
    _patch_with(BaseStreamBlock, NewBaseStreamBlock,
                'sorted_child_blocks', 'render_list_member',
                'html_declarations', 'js_initializer', 'render_form',
                'value_from_datadict', 'value_omitted_from_data')
    _patch_with(ListBlock, NewListBlock,
                'render_list_member',
                'html_declarations', 'js_initializer', 'render_form',
                'value_from_datadict', 'value_omitted_from_data')
    _patch_with(BaseStructBlock, NewBaseStructBlock,
                'js_initializer', 'get_form_context', 'render_form',
                'value_from_datadict', 'value_omitted_from_data')
    _patch_with(FieldBlock, NewFieldBlock, 'value_from_datadict')
