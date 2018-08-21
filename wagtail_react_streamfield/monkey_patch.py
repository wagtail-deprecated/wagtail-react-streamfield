from django.utils.six import wraps
from wagtail.core.blocks import BlockField

from .widgets import NewBlockWidget


def _patch_streamfield_panel():
    from wagtail.admin.edit_handlers import StreamFieldPanel
    from .edit_handlers import NewStreamFieldPanel

    def patch_html_declarations(original):
        @wraps(original)
        def inner(self):
            return NewStreamFieldPanel.html_declarations(self)
        return inner

    StreamFieldPanel.html_declarations = \
        patch_html_declarations(StreamFieldPanel.html_declarations)


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
