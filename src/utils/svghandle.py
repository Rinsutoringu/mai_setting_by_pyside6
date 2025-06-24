import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

class svgHandle:
    _executor = ThreadPoolExecutor(max_workers=2)

    def __init__(self, svg_file_path=None):
        self.svg_content = ""
        if svg_file_path:
            with open(svg_file_path, "r", encoding="utf-8") as f:
                self.svg_content = f.read()

    def changeSvgColor(self, label_name, target_color):
        try:
            ns = {
                'svg': 'http://www.w3.org/2000/svg',
                'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
            }
            ET.register_namespace('', ns['svg'])
            ET.register_namespace('inkscape', ns['inkscape'])

            root = ET.fromstring(self.svg_content)
            found = False
            for elem in root.iter():
                label = elem.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label')
                if label == label_name:
                    self._set_fill_recursive(elem, target_color)
                    found = True
                    break
            if not found:
                print(f"[svgHandle] Label '{label_name}' not found in SVG.")
            new_svg = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
            self.svg_content = new_svg  # 更新为最新内容
            return new_svg
        except Exception as e:
            print(f"[svgHandle] changeSvgColor error: {e}")
            return self.svg_content

    def _set_fill_recursive(self, elem, target_color):
        tag = elem.tag.split('}')[-1]
        if tag in ['path', 'rect', 'polygon', 'ellipse', 'circle']:
            self.set_fill(elem, target_color)
        for child in elem:
            self._set_fill_recursive(child, target_color)

    def set_fill(self, elem, target_color):
        elem.set('fill', target_color)
        style = elem.attrib.get('style')
        if style:
            styles = style.split(';')
            new_styles = []
            found = False
            for s in styles:
                if s.strip().startswith('fill:'):
                    new_styles.append(f'fill:{target_color}')
                    found = True
                elif s.strip():
                    new_styles.append(s)
            if not found:
                new_styles.append(f'fill:{target_color}')
            elem.set('style', ';'.join(new_styles))