import re
from pathlib import Path

from mako.lookup import TemplateLookup
import markdown2

from common import site_dir


lookup = TemplateLookup(directories=[str(site_dir)], strict_undefined=True)


def render_template(template_file, **kwargs):
    kwargs.update(
        PATH=site_dir / template_file,
        render_markdown_file=render_markdown_file,
        render_slides=render_slides,
    )
    tmpl = lookup.get_template(str(template_file))
    return tmpl.render(**kwargs)


def render_markdown_file(markdown_file):
    return markdown2.markdown(markdown_file.read_text())


def render_slides(markdown_file):
    text = markdown_file.read_text()
    text = replace_h1(text)
    html = markdown2.markdown(text)
    html = html.replace('<hr />', '</section>\n<section>')
    return '<section>\n{}\n</section>'.format(html)


def replace_h1(text):
    """
    Replace all h1 elements with h2 elements in the given markdown text
    (excluding the first h1). We do this because reveal.js renders h1 elements
    extremely large.

    """
    def gen():
        found_first = False
        for line in text.splitlines():
            if re.match(r'^# ', line):
                if found_first:
                    yield '#' + line
                    continue
                found_first = True

            yield line

    return '\n'.join(gen())