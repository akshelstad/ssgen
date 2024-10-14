import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    
    def test_text_type_text(self):
        text_node = TextNode("hello mfers", text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                        'hello mfers'
                        )
        
    def test_text_type_bold(self):
        text_node = TextNode("hello mfers", text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                        '<b>hello mfers</b>'
                        )
        
    def test_text_type_italic(self):
        text_node = TextNode("hello mfers", text_type_italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                        '<i>hello mfers</i>'
                        )
        
    def test_text_type_code(self):
        text_node = TextNode("hello mfers", text_type_code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                        '<code>hello mfers</code>'
                        )
        
    def test_text_type_link(self):
        text_node = TextNode("hello mfers", text_type_link, "www.fuck.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                        '<a href="www.fuck.com">hello mfers</a>'
                        )
        
    def test_text_type_img(self):
        text_node = TextNode("hello mfers", text_type_image, "www.fuck.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(),
                        '<img src="www.fuck.com" alt="hello mfers"></img>'
                        )

if __name__ == "__main__":
    unittest.main()