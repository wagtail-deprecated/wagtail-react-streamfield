from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.text import capfirst
from wagtail.core.blocks import Block

from wagtail_react_streamfield.exceptions import RemovedError
from wagtail_react_streamfield.widgets import get_non_block_errors


class NewBlock(Block):
    FIELD_NAME_TEMPLATE = 'field-__ID__'

    def get_default(self):
        default = self.meta.default
        if callable(default):
            default = default()
        return default

    def prepare_value(self, value, errors=None):
        """
        Returns the value as it will be displayed in react-streamfield.
        """
        return value

    def get_instance_html(self, value, errors=None):
        """
        Returns the HTML template generated for a given value.

        That HTML will be displayed as the block content panel
        in react-streamfield. It is usually not rendered
        """
        help_text = getattr(self.meta, 'help_text', None)
        non_block_errors = get_non_block_errors(errors)
        if help_text or non_block_errors:
            return render_to_string(
                'wagtailadmin/block_forms/blocks_container.html',
                {
                    'help_text': help_text,
                    'non_block_errors': non_block_errors,
                }
            )

    @cached_property
    def definition(self):
        definition = {
            'key': self.name,
            'label': capfirst(self.label),
            'required': self.required,
            'closed': self.meta.closed,
            'dangerouslyRunInnerScripts': True,
        }
        if self.meta.icon != Block._meta_class.icon:
            definition['icon'] = ('<i class="icon icon-%s"></i>'
                                  % self.meta.icon)
        if self.meta.classname is not None:
            definition['className'] = self.meta.classname
        if self.meta.group:
            definition['group'] = str(self.meta.group)
        if self.meta.default:
            definition['default'] = self.prepare_value(self.get_default())
        return definition

    def all_html_declarations(self):
        raise RemovedError

    def html_declarations(self):
        raise RemovedError
