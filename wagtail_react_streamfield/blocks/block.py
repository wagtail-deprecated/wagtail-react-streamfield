from wagtail.core.blocks import Block

from wagtail_react_streamfield.exceptions import RemovedError


class NewBlock(Block):
    def all_html_declarations(self):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError
