What’s new in wagtail-react-streamfield?
========================================

1.3.0
-----

- Dropped Wagtail < 2.6 support
- Removes layouts, only a single layout exists now, a mix of the best parts of
  the former ``SIMPLE`` of ``COLLAPSIBLE``
- Adds ``closed`` attribute in the ``Meta`` of blocks to set by block type
  whether they should be closed on page editor load (defaults to ``False``)
- Adds support for collapsible nested struct blocks
- Speeds up server-side page editor load
- Fixes two issues with radio buttons
- Fixes an issue with missing IDs in StreamBlocks
  (including the root StreamBlock)
- Fixes callable default values
- Fixes the dynamic title of the children of a ``ListBlock``
- Fixes minor CSS details


1.2.0
-----

- Dropped Wagtail 2.2 & 2.3 support, but it may work perfectly with both these
  versions, it was not tested on these
- Moves the plusses between blocks (they were in the left gutter)
- Adds the duplicate icon that was missing from the MANIFEST.in
- Fixes ``COLLAPSIBLE`` block content previews on non-struct blocks
- Rewrites the SCSS using BEM to avoid clashes with external CSS
- Countless minor visual fixes
- Major rewrite to improve code quality and extensibility

1.1.1
-----

- Fixes a bug was introduced in 1.1.0 when validation fails while saving
- Removes a rectangle visible on Safari due to a weird unicode character
  added by accident

1.1.0
-----

- Automatically collapses blocks on small/mobile devices
- Increases the size of block type selection buttons while making the labels
  uppercase
- Adds support for help text in StreamBlock, ListBlock & StructBlock
- Adds support for default values in StreamBlock, ListBlock & StructBlock
- Adds support for non-block errors in non-root StreamBlock, ListBlock
  & StructBlock
- Applies default values to missing sub-blocks of already saved StructBlocks
- Fixes the remaining edge cases found by updating tests upstream,
  in https://github.com/wagtail/wagtail/pull/4942

1.0.6
-----

Fixes a formatting issue with ``AdminDateInput`` & ``AdminDateTimeInput``
due to Wagtail’s custom formatting
(``WAGTAIL_DATE_FORMAT`` & ``WAGTAIL_DATETIME_FORMAT``)

1.0.5
-----

- Adds a real duplicate icon
- Fix a recently introduced bug raising a 500 error when saving a page
  with validation errors

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
