from django.utils.functional import cached_property
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.translation import ugettext_lazy as _
from wagtail.core.blocks import ListBlock, Block

from ..exceptions import RemovedError
from ..widgets import BlockData


class NewListBlock(ListBlock):
    def __init__(self, child_block, **kwargs):
        Block.__init__(self, **kwargs)

        self.child_block = (child_block() if isinstance(child_block, type)
                            else child_block)

        if not hasattr(self.meta, 'default'):
            self.meta.default = [self.child_block.get_default()]

        self.dependencies = [self.child_block]

    @cached_property
    def definition(self):
        definition = super(ListBlock, self).definition
        definition.update(
            children=[self.child_block.definition],
            minNum=self.meta.min_num,
            maxNum=self.meta.max_num,
        )
        html = self.get_instance_html([])
        if html is not None:
            definition['html'] = html
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

    def prepare_value(self, value, errors=None):
        children_errors = (None if errors is None
                           else errors.as_data()[0].params)
        if children_errors is None:
            children_errors = [None] * len(value)
        prepared_value = []
        for child_value, child_errors in zip(value, children_errors):
            html = self.child_block.get_instance_html(child_value,
                                                      errors=child_errors)
            child_value = BlockData({
                'id': str(uuid4()),
                'type': self.child_block.name,
                'hasError': bool(child_errors),
                'value': self.child_block.prepare_value(child_value,
                                                        errors=errors),
            })
            if html is not None:
                child_value['html'] = html
            prepared_value.append(child_value)
        return prepared_value

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
