from wagtail import blocks


class StreamBlocks(blocks.StreamBlock):
    paragraph = blocks.RichTextBlock()
