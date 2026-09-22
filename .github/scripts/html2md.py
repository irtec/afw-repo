#!/usr/bin/env python3
"""Convert afw-repo gh-pages index.html into a clean README.md.

Pure stdlib (html.parser) so it runs on any GitHub runner with no deps.
Usage: html2md.py <input.html> <output.md>
"""
import html
import re
import sys
from html.parser import HTMLParser


class MDConverter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self._buf = []
        self._list = []
        self._in_pre = False
        self._pre = []
        self._skip = False

    def _flush_buf(self):
        text = "".join(self._buf).strip()
        self._buf = []
        return text

    def _emit(self, s):
        if s.strip():
            self.out.append(s.rstrip())

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "head"):
            self._skip = True
            return
        if tag == "pre":
            self._in_pre = True
            self._pre = []
            return
        if self._skip:
            return
        if tag in ("h1", "h2", "h3"):
            self._flush_buf()
        elif tag == "p":
            self._flush_buf()
        elif tag == "ul":
            self._flush_buf()
            self._list = []
        elif tag == "li":
            self._flush_buf()
        elif tag == "br":
            self._buf.append("\n")
        elif tag == "strong":
            self._buf.append("**")
        elif tag == "em":
            self._buf.append("*")
        elif tag == "code" and not self._in_pre:
            self._buf.append("`")
        elif tag == "a":
            href = dict(attrs).get("href", "")
            self._buf.append("\x00" + href + "\x01")

    def handle_endtag(self, tag):
        if tag in ("style", "head"):
            self._skip = False
            return
        if self._skip:
            return
        if tag == "pre":
            self._in_pre = False
            code = "".join(self._pre).rstrip("\n")
            lang = ""
            if re.search(r"(sudo|\$\b|apt|dnf|curl|systemctl|afw|echo\b|tee\b|rpm\b|gpg\b|add-apt-repository)", code):
                lang = "bash"
            self.out.append("```" + lang)
            self.out.append(code)
            self.out.append("```")
            self.out.append("")
            return
        if tag in ("h1", "h2", "h3"):
            text = self._flush_buf()
            level = {"h1": "#", "h2": "##", "h3": "###"}[tag]
            self._emit(f"{level} {text}")
            self.out.append("")
        elif tag == "p":
            text = self._flush_buf()
            if text:
                self.out.append(text)
                self.out.append("")
        elif tag == "ul":
            for item in self._list:
                self.out.append(f"- {item}")
            self.out.append("")
            self._list = []
        elif tag == "li":
            self._list.append(self._flush_buf())
        elif tag == "strong":
            self._buf.append("**")
        elif tag == "em":
            self._buf.append("*")
        elif tag == "code" and not self._in_pre:
            self._buf.append("`")
        elif tag == "a":
            self._buf.append("\x02")

    def handle_data(self, data):
        if self._skip:
            return
        if self._in_pre:
            self._pre.append(data)
            return
        self._buf.append(data)

    def finalize(self):
        md = "\n".join(self.out).rstrip() + "\n"
        md = re.sub(
            r"\x00([^\x01]*)\x01(.*?)\x02",
            lambda m: f"[{m.group(2).strip()}]({m.group(1)})",
            md,
        )
        md = md.replace("\x00", "").replace("\x01", "").replace("\x02", "")
        md = re.sub(r"\n{3,}", "\n\n", md)
        return md


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: html2md.py <input.html> <output.md>\n")
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as f:
        raw = f.read()
    c = MDConverter()
    c.feed(raw)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(c.finalize())
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
