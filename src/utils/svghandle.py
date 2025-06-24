import xml.etree.ElementTree as ET

class svgHandle:

    def __init__(self, svg_file_path=None):
        self.svg_content = ""
        if svg_file_path:
            with open(svg_file_path, "r", encoding="utf-8") as f:
                self.svg_content = f.read()

    def changeSvgColor(self, label_name, target_color):
        """
        修改SVG字符串中指定 inkscape:label 的元素及其子元素的颜色（包括style属性中的fill），返回修改后的SVG字符串
        :param label_name: inkscape:label 的值
        :param target_color: 目标颜色（如 "#ff0000"）
        :return: 修改后的SVG字符串
        """
        ns = {
            'svg': 'http://www.w3.org/2000/svg',
            'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
        }
        ET.register_namespace('', ns['svg'])
        ET.register_namespace('inkscape', ns['inkscape'])

        root = ET.fromstring(self.svg_content)
        # 查找 inkscape:label=label_name 的元素
        for elem in root.iter():
            label = elem.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label')
            if label == label_name:
                for child in elem.iter():
                    tag = child.tag.split('}')[-1]
                    if tag in ['path', 'rect', 'polygon', 'ellipse', 'circle']:
                        self.set_fill(child, target_color)
                break
        # 返回修改后的SVG字符串
        return ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')

    def set_fill(self, elem, target_color):
        # 直接设置fill属性
        elem.set('fill', target_color)
        # 处理style属性
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



# 用法示例
if __name__ == "__main__":
    svg_handler = svgHandle("d:/dev/orderProject/maiSetting/resources/drawing.svg")
    new_svg = svg_handler.changeSvgColor("E8", "#00ff00")
    # 可以直接传递 new_svg 给 QSvgRenderer.load(QByteArray(new_svg.encode("utf-8")))
    with open("d:/dev/orderProject/maiSetting/resources/drawing_modified.svg", "w", encoding="utf-8") as f:
        f.write(new_svg)