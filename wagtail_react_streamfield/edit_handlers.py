import logging, datetime

from wagtail.admin.edit_handlers import StreamFieldPanel
from guru.helpers.utils.object import pick

logger = logging.getLogger(__name__)


class NewStreamFieldPanel(StreamFieldPanel):
    
    def html_declarations(self):
        return ''
