from wagtail import VERSION as wagtail_version
from wagtail.core.blocks import (
    FieldBlock, CharBlock, TextBlock, FloatBlock, DecimalBlock, RegexBlock,
    URLBlock, DateBlock, TimeBlock, DateTimeBlock, EmailBlock, IntegerBlock,
    RichTextBlock,
)

from ..constants import FIELD_NAME_TEMPLATE


class NewFieldBlock(FieldBlock):
    def prepare_for_react(self, value):
        from wagtail.admin.rich_text import DraftailRichTextArea

        value = self.value_for_form(self.field.prepare_value(value))
        widget = self.field.widget
        if isinstance(self, RichTextBlock) \
                and isinstance(widget, DraftailRichTextArea):
            value = (widget.translate_value(value) if wagtail_version < (2, 3)
                     else widget.format_value(value))
        return value

    def get_definition(self):
        definition = super(FieldBlock, self).get_definition()
        definition.update(
            default=self.prepare_for_react(self.get_default()),
            html=self.render_form(self.get_default(),
                                  prefix=FIELD_NAME_TEMPLATE),
        )
        title_template = self.get_title_template()
        if title_template is not None:
            definition['titleTemplate'] = title_template
        return definition

    def get_title_template(self):
        if isinstance(self, (CharBlock, TextBlock, FloatBlock,
                             DecimalBlock, RegexBlock, URLBlock,
                             DateBlock, TimeBlock, DateTimeBlock,
                             EmailBlock, IntegerBlock)):
            return '${%s}' % self.name

    def value_from_datadict(self, data, files, prefix):
        return self.value_from_form(
            self.field.widget.value_from_datadict(
                {'value': data['value']}, files, 'value'))
