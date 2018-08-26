from wagtail.core.blocks import (
    FieldBlock, CharBlock, TextBlock, FloatBlock, DecimalBlock, RegexBlock,
    URLBlock, DateBlock, TimeBlock, DateTimeBlock, EmailBlock, IntegerBlock,
)


class NewFieldBlock(FieldBlock):
    def get_definition(self):
        definition = super(FieldBlock, self).get_definition()
        definition['html'] = self.render_form(self.get_default(),
                                              prefix='field-__ID__')
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
