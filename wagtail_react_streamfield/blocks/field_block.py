from django.utils.functional import cached_property
from wagtail.core.blocks import (
    FieldBlock, CharBlock, TextBlock, FloatBlock, DecimalBlock, RegexBlock,
    URLBlock, DateBlock, TimeBlock, DateTimeBlock, EmailBlock, IntegerBlock,
    RichTextBlock, Block,
)


class NewFieldBlock(FieldBlock):
    def prepare_value(self, value, errors=None):
        from wagtail.admin.rich_text import DraftailRichTextArea
        from wagtail.admin.widgets import AdminDateInput, AdminDateTimeInput

        value = self.value_for_form(self.field.prepare_value(value))
        widget = self.field.widget
        if isinstance(self, RichTextBlock) \
                and isinstance(widget, DraftailRichTextArea):
            value = widget.format_value(value)
        if isinstance(widget, (AdminDateInput, AdminDateTimeInput)):
            value = widget.format_value(value)
        return value

    def get_instance_html(self, value, errors=None):
        if errors:
            return self.render_form(value, prefix=Block.FIELD_NAME_TEMPLATE,
                                    errors=errors)

    @cached_property
    def definition(self):
        definition = super(FieldBlock, self).definition
        definition['html'] = self.render_form(self.get_default(),
                                              prefix=self.FIELD_NAME_TEMPLATE)
        title_template = self.get_title_template()
        if title_template is not None:
            definition['titleTemplate'] = title_template
        return definition

    def get_title_template(self):
        if isinstance(self, (CharBlock, TextBlock, FloatBlock,
                             DecimalBlock, RegexBlock, URLBlock,
                             DateBlock, TimeBlock, DateTimeBlock,
                             EmailBlock, IntegerBlock)) and self.name:
            return '${%s}' % self.name

    def value_from_datadict(self, data, files, prefix):
        return self.value_from_form(
            self.field.widget.value_from_datadict(
                {'value': data.get('value', self.get_default())},
                files, 'value'))
