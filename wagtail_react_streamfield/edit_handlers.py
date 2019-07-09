import logging, datetime

from wagtail.admin.edit_handlers import StreamFieldPanel
from guru.helpers.utils.object import pick

logger = logging.getLogger(__name__)


class NewStreamFieldPanel(StreamFieldPanel):
    
    def html_declarations(self):
        return ''


class BlockCacheStreamFieldPanel(NewStreamFieldPanel):
    ''' StreamField panel instance which uses a block cache to improve performance of page load
    '''
    def __init__(self, *args, **kwargs):
        super(BlockCacheStreamFieldPanel, self).__init__(*args, **kwargs)

    def on_instance_bound(self, *args, **kwargs):
        
        # Initialize new block cache
        if not hasattr(self, 'block_cache'):
            logger.debug('Initialize block cache')
            setattr(self, 'block_cache', kwargs.get('block_cache') or {})
        
        # Initialize block definition for the panel
        super(BlockCacheStreamFieldPanel, self).on_instance_bound(*args, **kwargs)

        # Attach block cache to root block definition
        setattr(self.block_def, 'block_cache', self.block_cache)
