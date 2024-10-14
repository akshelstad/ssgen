import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

class TestExtractMarkdownImages(unittest.TestCase):
    def test_one_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        extracted = extract_markdown_images(text)
        self.assertEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif')
            ],
            extracted
        )

    def test_two_links(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        self.assertEqual(
            [
                ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
            ],
            extracted
        )

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_one_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        extracted = extract_markdown_links(text)
        self.assertEqual(
            [
                ('to boot dev', 'https://www.boot.dev')
            ],
            extracted
        )

    def test_two_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted = extract_markdown_links(text)
        self.assertEqual(
            [
                ('to boot dev', 'https://www.boot.dev'),
                ('to youtube', 'https://www.youtube.com/@bootdotdev')
            ],
            extracted
        )

class TestSplitNodesImage(unittest.TestCase):
    def test_one_image(self):
        node = TextNode("This is a textnode with an ![image of a puppy](www.puppyshit.com)", text_type_text)
        self.assertEqual(
            [
                TextNode("This is a textnode with an ", text_type_text),
                TextNode("image of a puppy", text_type_image, "www.puppyshit.com")
            ],
            split_nodes_image([node])
        )

    def test_two_images(self):
        node = TextNode("This is a textnode with an ![image of a puppy](www.puppyshit.com) and an ![image of a cat](www.pussy.com)", text_type_text)
        self.assertEqual(
            [
                TextNode("This is a textnode with an ", text_type_text),
                TextNode("image of a puppy", text_type_image, "www.puppyshit.com"),
                TextNode(" and an ", text_type_text),
                TextNode("image of a cat", text_type_image, "www.pussy.com"),
            ],
            split_nodes_image([node])
        )

    def test_two_images_addtl_text(self):
        node = TextNode("This is a textnode with an ![image of a puppy](www.puppyshit.com) and an ![image of a cat](www.pussy.com) and additional text at the end.", text_type_text)
        self.assertEqual(
            [
                TextNode("This is a textnode with an ", text_type_text),
                TextNode("image of a puppy", text_type_image, "www.puppyshit.com"),
                TextNode(" and an ", text_type_text),
                TextNode("image of a cat", text_type_image, "www.pussy.com"),
                TextNode(" and additional text at the end.", text_type_text)
            ],
            split_nodes_image([node])
        )

class TestSplitNodesLink(unittest.TestCase):
    def test_one_link(self):
        node = TextNode("This is a textnode with a [link to youtube](www.youtube.com)", text_type_text)
        self.assertEqual(
            [
                TextNode("This is a textnode with a ", text_type_text),
                TextNode("link to youtube", text_type_link, "www.youtube.com")
            ],
            split_nodes_link([node])
        )

    def test_two_links(self):
        node = TextNode("This is a textnode with a [link to youtube](www.youtube.com) and a [link to google](www.google.com)", text_type_text)
        self.assertEqual(
            [
                TextNode("This is a textnode with a ", text_type_text),
                TextNode("link to youtube", text_type_link, "www.youtube.com"),
                TextNode(" and a ", text_type_text),
                TextNode("link to google", text_type_link, "www.google.com"),
            ],
            split_nodes_link([node])
        )

    def test_two_links_addtl_text(self):
        node = TextNode("This is a textnode with a [link to youtube](www.youtube.com) and a [link to google](www.google.com) and additional text at the end.", text_type_text)
        self.assertEqual(
            [
                TextNode("This is a textnode with a ", text_type_text),
                TextNode("link to youtube", text_type_link, "www.youtube.com"),
                TextNode(" and a ", text_type_text),
                TextNode("link to google", text_type_link, "www.google.com"),
                TextNode(" and additional text at the end.", text_type_text)
            ],
            split_nodes_link([node])
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            [
                TextNode("This is ", text_type_text), 
                TextNode("text", text_type_bold), 
                TextNode(" with an ", text_type_text), 
                TextNode("italic", text_type_italic), 
                TextNode(" word and a ", text_type_text), 
                TextNode("code block", text_type_code), 
                TextNode(" and an ", text_type_text), 
                TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", text_type_text), 
                TextNode("link", text_type_link, "https://boot.dev")
            ],
            text_to_textnodes(text)
        )

    def test_multi(self):
        text = "This is **text** with an *italic* word **and** a `code block` *and* an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            [
                TextNode("This is ", text_type_text), 
                TextNode("text", text_type_bold), 
                TextNode(" with an ", text_type_text), 
                TextNode("italic", text_type_italic), 
                TextNode(" word ", text_type_text), 
                TextNode("and", text_type_bold),
                TextNode(" a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" ", text_type_text),
                TextNode("and", text_type_italic), 
                TextNode(" an ", text_type_text), 
                TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"), 
                TextNode(" and a ", text_type_text), 
                TextNode("link", text_type_link, "https://boot.dev")
            ],
            text_to_textnodes(text)
        )


if __name__ == "__main__":
    unittest.main()