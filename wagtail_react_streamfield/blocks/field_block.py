from wagtail import VERSION as wagtail_version
from wagtail.core.blocks import (
    FieldBlock, CharBlock, TextBlock, FloatBlock, DecimalBlock, RegexBlock,
    URLBlock, DateBlock, TimeBlock, DateTimeBlock, EmailBlock, IntegerBlock,
    RichTextBlock, Block,
    StreamValue)


class NewFieldBlock(FieldBlock):
    def prepare_value(self, value, errors=None):
        from wagtail.admin.rich_text import DraftailRichTextArea
        from wagtail.admin.widgets import AdminDateInput, AdminDateTimeInput

        value = self.value_for_form(self.field.prepare_value(value))
        widget = self.field.widget
        if isinstance(self, RichTextBlock) \
                and isinstance(widget, DraftailRichTextArea):
            value = (widget.translate_value(value) if wagtail_version < (2, 3)
                     else widget.format_value(value))
        if isinstance(widget, (AdminDateInput, AdminDateTimeInput)):
            value = widget.format_value(value)
        return value

    def prepare_for_react(self, parent_block, value,
                          type_name=None, errors=None):
        data = super(FieldBlock, self).prepare_for_react(
            parent_block, value, type_name=type_name, errors=errors)
        if errors:
            if isinstance(value, StreamValue.StreamChild):
                value = value.value
            data['html'] = self.render_form(
                value, prefix=Block.FIELD_NAME_TEMPLATE, errors=errors)
        return data

    def get_definition(self):
        definition = super(FieldBlock, self).get_definition()
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
                             EmailBlock, IntegerBlock)):
            return '${%s}' % self.name

    def value_from_datadict(self, data, files, prefix):
        return self.value_from_form(
            self.field.widget.value_from_datadict(
                {'value': data.get('value', self.get_default())},
                files, 'value'))
