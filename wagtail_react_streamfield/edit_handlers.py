from wagtail.admin.edit_handlers import StreamFieldPanel


class NewStreamFieldPanel(StreamFieldPanel):
    def html_declarations(self):
        return ''
