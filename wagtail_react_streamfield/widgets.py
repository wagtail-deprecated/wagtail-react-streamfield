import json

from django.core.exceptions import NON_FIELD_ERRORS
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import Media
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from wagtail.core.blocks import BlockWidget


class ConfigJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, BlockData):
            return o.data
        return super().default(o)


class InputJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, BlockData):
            return {'id': o['id'],
                    'type': o['type'],
                    'value': o['value']}
        return super().default(o)


def to_json_script(data, encoder=ConfigJSONEncoder):
    return json.dumps(
        data, separators=(',', ':'), cls=encoder
    ).replace('<', '\\u003c')


class BlockData:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return '<BlockData %s>' % self.data


def get_non_block_errors(errors):
    if errors is None:
        return ()
    errors_data = errors.as_data()
    if isinstance(errors, ErrorList):
        errors_data = errors_data[0].params
        if errors_data is None:
            return errors
    if isinstance(errors_data, dict):
        return errors_data.get(NON_FIELD_ERRORS, ())
    return ()


class NewBlockWidget(BlockWidget):
    def get_action_labels(self):
        return {
            'add': _('Add'),
            'moveUp': _('Move up'),
            'moveDown': _('Move down'),
            'duplicate': _('Duplicate'),
            'delete': _('Delete'),
        }

    def get_actions_icons(self):
        return {
            'add': '<i aria-hidden="true">+</i>',
            'moveUp': '<i class="icon icon-arrow-up" aria-hidden="true"></i>',
            'moveDown': '<i class="icon icon-arrow-down" aria-hidden="true"></i>',
            'duplicate': '<i class="icon icon-duplicate" aria-hidden="true"></i>',
            'delete': '<i class="icon icon-bin" aria-hidden="true"></i>',
            'grip': '<i class="icon icon-grip" aria-hidden="true"></i>',
        }

    def get_streamfield_config(self, value, errors=None):
        return {
            'required': self.block_def.required,
            'minNum': self.block_def.meta.min_num,
            'maxNum': self.block_def.meta.max_num,
            'icons': self.get_actions_icons(),
            'labels': self.get_action_labels(),
            'blockDefinitions': self.block_def.definition['children'],
            'value': self.block_def.prepare_value(value, errors=errors),
        }

    def render_with_errors(self, name, value, attrs=None, errors=None,
                           renderer=None):
        streamfield_config = self.get_streamfield_config(value, errors=errors)
        escaped_value = to_json_script(streamfield_config['value'],
                                       encoder=InputJSONEncoder)
        non_block_errors = get_non_block_errors(errors)
        non_block_errors = ''.join([
            mark_safe('<div class="help-block help-critical">%s</div>') % error
            for error in non_block_errors])
        return mark_safe("""
        <textarea style="display: none;" name="%s">%s</textarea>
        <script>window.streamField.init('%s', %s, document.currentScript)</script>
        %s
        """ % (name, escaped_value,
               name, to_json_script(streamfield_config),
               non_block_errors))

    @property
    def media(self):
        return self.block_def.all_media() + Media(
            js=['js/wagtail-react-streamfield.js'],
            css={'all': [
                'css/wagtail-react-streamfield.css',
            ]})

    def value_from_datadict(self, data, files, name):
        stream_field_data = json.loads(data.get(name))
        return super().value_from_datadict({'value': stream_field_data},
                                           files, name)
