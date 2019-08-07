from django.utils.functional import cached_property
from wagtail.core.blocks import StaticBlock, Block


class NewStaticBlock(StaticBlock):
    @cached_property
    def definition(self):
        definition = Block.definition.func(self)
        definition.update(
            isStatic=True,
            html=self.render_form(self.get_default(),
                                  prefix=self.FIELD_NAME_TEMPLATE),
        )
        return definition
