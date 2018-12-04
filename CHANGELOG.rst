What’s new in wagtail-react-streamfield?
========================================

1.0.4
-----

- Makes block type styling consistent
- Maximizes the action buttons padding

1.0.3
-----

- Changes the teal color to the new color from Wagtail 2.3
- Improves margins and paddings consistency with Wagtail
- Fixes an issue on mobile devices with the panel for adding new blocks
  that jumps during its transition

1.0.2
-----

- Improves mobile layout
- Enlarges the clickable area of add buttons

1.0.1
-----

- Fixes a bug where ``COLLAPSIBLE`` blocks
  couldn’t be defined as open by default
- Fixes the version number

1.0.0
-----

- Changes the overall look to match latest design decisions
- Adds the ``SIMPLE`` layout
- Makes ``SIMPLE`` the new default layout
  for a better continuity with the old StreamField
- Allows to customize the layout by overwriting
  the ``Block.get_layout()`` method
- Use Wagtail icons instead of FontAwesome icons
- Fixes the remaining CSS integration issues

0.9.0
-----

- Adds Wagtail 2.3 support
- Adds support for block groups
- Adds support for static blocks
- Upgrades to react-beautiful-dnd 10, improving fluidity by 30%

0.8.6
-----

- Fixes default values support
- Removes Wagtail 2.0 & 2.1 support to fix chooser blocks

0.8.5
-----

- Adds ``min_num`` and ``max_num`` support for ``ListBlock``
- Fixes duplication of remaining unsupported blocks: ``ChooserBlock`` & ``DateBlock``
- Fixes rendering of errors on non-chooser blocks
- Fixes a Python error when migrations use combinations of ``ListBlock`` with ``StructBlock``
- Removes the confirm dialog shown when leaving the page without changes

0.8.4
-----

- Fixes loading of Draftail RichTextBlock in some *scenarii*

0.8.3
-----

- Fixes loading and duplication of TableBlock, Hallo.js RichTextBlocks
- Fixes Draftail RichTextBlock duplication
- Avoids showing a confirm when exiting an unmodified page
- Fixes handling of custom empty block values
- Fixes handling of extra undefined data

0.8.2
-----

- Adds ``max_num`` support
- Adds a transition when using move arrows
- Adds a transition on the panel listing the block types to add
- Fixes StructBlock as a StructBlock field

0.8.1
-----

- Automatically opens blocks with errors while adding a red highlight
- Fixes the load of JavaScript widgets such as RichTextField & ChooserPanels

0.8.0
-----

First working version with all essential features
