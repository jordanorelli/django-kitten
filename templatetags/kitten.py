import re
import string
from django import template
register = template.Library()

geometry_pat = re.compile(r'^(?P<width>\d+)?(?:[Xx](?P<height>\d+))?$')

class KittenNode(template.Node):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, context):
        return 'http://placekitten.com/%d/%d' % (self.width, self.height)

@register.tag
def kitten(parser, token):
    try:
        tag_name, dimensions = token.split_contents()
        match = geometry_pat.match(dimensions)
        if not match:
            raise ValueError
        width = int(match.group('width'))
        height = int(match.group('height'))
    except ValueError:
        raise template.TemplateSyntaxError('%r tag requires exactly one '
                                           'dimensions argument as a string. '
                                           'usage: {%% kitten "40x120" %%}'
                                           % token.contents.split()[0])
    return KittenNode(width, height)
