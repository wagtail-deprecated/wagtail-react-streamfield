from django.utils.six import wraps
from wagtail.core.blocks import (
    BlockField, Block, BaseStreamBlock, ListBlock, BaseStructBlock, FieldBlock,
    StaticBlock)

from wagtail_react_streamfield.blocks.static_block import NewStaticBlock
from .blocks.block import NewBlock
from .blocks.field_block import NewFieldBlock
from .blocks.list_block import NewListBlock
from .blocks.stream_block import NewBaseStreamBlock
from .blocks.struct_block import NewBaseStructBlock
from .widgets import NewBlockWidget


def _patch_with(original_class, new_class, *method_names):
    def patch_original(original_method, new_method):
        @wraps(original_method)
        def inner(*args, **kwargs):
            return new_method(*args, **kwargs)

        return inner

    for method_name in method_names:
        original_method = getattr(original_class, method_name, None)
        new_method = getattr(new_class, method_name)

        if original_method is not None and callable(original_method):
            new_method = patch_original(original_method, new_method)

        setattr(original_class, method_name, new_method)


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


def _patch_list_block():
    _patch_with(ListBlock, NewListBlock,
                '__init__', 'get_definition', 'render_list_member',
                'html_declarations', 'js_initializer', 'render_form',
                'value_from_datadict', 'value_omitted_from_data', 'clean')
    ListBlock._meta_class.min_num = None
    ListBlock._meta_class.max_num = None


def patch():
    _patch_streamfield_panel()
    _patch_block_widget()
    _patch_with(Block, NewBlock,
                'SIMPLE', 'COLLAPSIBLE', 'get_layout', 'get_definition',
                'html_declarations', 'all_html_declarations')
    _patch_with(BaseStreamBlock, NewBaseStreamBlock,
                'get_definition', 'sorted_child_blocks', 'render_list_member',
                'html_declarations', 'js_initializer', 'render_form',
                'value_from_datadict', 'value_omitted_from_data')
    _patch_list_block()
    _patch_with(BaseStructBlock, NewBaseStructBlock,
                '__init__', 'get_definition',
                'js_initializer', 'get_form_context', 'render_form',
                'value_from_datadict', 'value_omitted_from_data')
    _patch_with(FieldBlock, NewFieldBlock,
                'prepare_for_react', 'get_definition', 'get_title_template',
                'value_from_datadict')
    _patch_with(StaticBlock, NewStaticBlock, 'get_definition')
