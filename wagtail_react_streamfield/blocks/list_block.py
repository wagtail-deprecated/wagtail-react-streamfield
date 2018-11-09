from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from wagtail.core.blocks import ListBlock, Block

from ..exceptions import RemovedError


class NewListBlock(ListBlock):
    def __init__(self, child_block, **kwargs):
        Block.__init__(self, **kwargs)

        self.child_block = (child_block() if isinstance(child_block, type)
                            else child_block)

        if not hasattr(self.meta, 'default'):
            self.meta.default = [self.child_block.get_default()]

        self.dependencies = [self.child_block]

    def get_definition(self):
        definition = super(ListBlock, self).get_definition()
        definition.update(
            children=[self.child_block.get_definition()],
            minNum=self.meta.min_num,
            maxNum=self.meta.max_num,
        )
        return definition

    def render_list_member(self, *args, **kwargs):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError

    def js_initializer(self):
        raise RemovedError

    def render_form(self, *args, **kwargs):
        raise RemovedError

    def value_from_datadict(self, data, files, prefix):
        return [
            self.child_block.value_from_datadict(child_block_data, files,
                                                 prefix)
            for child_block_data in data['value']]

    def value_omitted_from_data(self, *args, **kwargs):
        raise RemovedError

    def clean(self, value):
        result = []
        errors = []
        for child_val in value:
            try:
                result.append(self.child_block.clean(child_val))
            except ValidationError as e:
                errors.append(ErrorList([e]))
            else:
                errors.append(None)

        if any(errors):
            raise ValidationError('Validation error in ListBlock',
                                  params=errors)

        if self.meta.min_num is not None and self.meta.min_num > len(value):
            raise ValidationError(
                _('The minimum number of items is %d') % self.meta.min_num
            )
        elif self.required and len(value) == 0:
            raise ValidationError(_('This field is required.'))

        if self.meta.max_num is not None and self.meta.max_num < len(value):
            raise ValidationError(
                _('The maximum number of items is %d') % self.meta.max_num
            )

        return result
