import json

from django.core.exceptions import NON_FIELD_ERRORS
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import Media
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
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
    return errors_data.get(NON_FIELD_ERRORS, ())


class NewBlockWidget(BlockWidget):
    def get_actions_icons(self):
        return {
            'moveUp': '<i class="icon icon-arrow-up"></i>',
            'moveDown': '<i class="icon icon-arrow-down"></i>',
            'duplicate': '<i class="icon icon-duplicate"></i>',
            'delete': '<i class="icon icon-bin"></i>',
            'grip': '<i class="icon icon-grip"></i>',
        }

    def render_with_errors(self, name, value, attrs=None, errors=None,
                           renderer=None):
        streamfield_config = {
            'required': self.block_def.required,
            'minNum': self.block_def.meta.min_num,
            'maxNum': self.block_def.meta.max_num,
            'icons': self.get_actions_icons(),
            'blockDefinitions': self.block_def.get_definition()['children'],
            'value': self.block_def.prepare_for_react(None, value,
                                                      errors=errors),
        }
        escaped_value = to_json_script(streamfield_config['value'],
                                       encoder=InputJSONEncoder)
        non_block_errors = get_non_block_errors(errors)
        non_block_errors = ''.join([
            mark_safe('<div class="help-block help-critical">%s</div>') % error
            for error in non_block_errors])
        return mark_safe("""
        <script type="application/json" data-streamfield="%s">%s</script>
        <textarea style="display: none;" name="%s">%s</textarea>
        %s
        """ % (name, to_json_script(streamfield_config),
               name, escaped_value, non_block_errors))

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
