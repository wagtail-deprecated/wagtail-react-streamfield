from wagtail.core.blocks import StaticBlock, Block

from ..constants import FIELD_NAME_TEMPLATE


class NewStaticBlock(StaticBlock):
    def get_definition(self):
        definition = Block.get_definition(self)
        definition.update(
            isStatic=True,
            html=self.render_form(self.get_default(),
                                  prefix=FIELD_NAME_TEMPLATE),
        )
        return definition
