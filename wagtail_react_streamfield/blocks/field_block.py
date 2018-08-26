from wagtail.core.blocks import FieldBlock


class NewFieldBlock(FieldBlock):
    def value_from_datadict(self, data, files, prefix):
        return self.value_from_form(
            self.field.widget.value_from_datadict(
                {'value': data['value']}, files, 'value'))
