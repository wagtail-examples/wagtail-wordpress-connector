from wagtail import blocks


class HeadingBlock(blocks.StructBlock):
    level = blocks.ChoiceBlock(
        required=True,
        choices=[
            ("h1", "H1"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("h4", "H4"),
            ("h5", "H5"),
            ("h6", "H6"),
        ],
        help_text="Level of heading",
    )
    text = blocks.CharBlock(required=True, help_text="Text to display")

    class Meta:
        icon = "title"
        template = "home/blocks/heading_block.html"


class BlockQuoteBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True, help_text="Quote to display")
    attribution = blocks.CharBlock(required=False, help_text="Attribution for quote")

    class Meta:
        icon = "openquote"
        template = "home/blocks/blockquote_block.html"


class DefinitionListBlock(blocks.StructBlock):
    list = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("term", blocks.CharBlock(required=True, help_text="Term to define")),
                (
                    "definition",
                    blocks.TextBlock(required=True, help_text="Definition of term"),
                ),
            ]
        )
    )

    class Meta:
        icon = "list-ul"
        template = "home/blocks/definition_list_block.html"


class StreamBlocks(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
    heading = HeadingBlock()
    blockquote = BlockQuoteBlock()
    definition_list = DefinitionListBlock()
