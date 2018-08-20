from django.utils.six import wraps
from wagtail.core.blocks import BlockField

from .widget import NewBlockWidget


def _patch_block_field():
    def patch_init(original):
        @wraps(original)
        def inner(self, block=None, **kwargs):
            if 'widget' not in kwargs:
                kwargs['widget'] = NewBlockWidget(block)
            original(self, block=block, **kwargs)
        return inner

    BlockField.__init__ = patch_init(BlockField.__init__)


def patch():
    _patch_block_field()
