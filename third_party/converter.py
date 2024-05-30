import re

def fix(text: str):
    fixes = [
        ["\r", ""],
        ["&lt;", "<"],
        ["&gt;", ">"],
        ["&lrm;", "\u200e"],
        ["&rlm;", "\u200f"],
        ["&nbsp;", "\u00a0"],
        ["&amp;", "&"]
    ]
    for sf, r in fixes:
        text = text.replace(sf, r)
    text = re.sub("<\/?(([^/ibu>]{1})|([^/>]{2,}?))>", "", text)
    return text

class Converter:
    def __init__(self, file: str):
        self.name = file
        self.raw_name = ".".join(file.split(".")[:-1])

    def to_srt(self):
        new_lines = []
        subtitle_esp = re.compile(
            r"\s+".join([
                r"([\d\.:]+ \-\-\> [\d\.:]+)",
                r"position:[\d.\.]+%,\w+",
                r"align:(\w+)",
                r"size:[\d.\.]+%",
                r"line:([\d.\.]+)%\s+(.+)"
            ]), re.DOTALL | re.MULTILINE
        )
        file = open(self.name, "r", encoding="utf8").read()
        lines = file.split("\n\n")
        
        line_index = 1
        verical_pos = -1     
        line_pos_matrix = [
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"]
        ]
        
        for line in lines:
            subtitle = subtitle_esp.search(line)
            if not subtitle:
                continue
            time = subtitle.group(1).replace(".", ",")
            align_type = subtitle.group(2)
            line_value = float(subtitle.group(3))
            text = subtitle.group(4).strip()
            if line_value <= 25.00:
                verical_pos = 0
            elif line_value >= 75.00:
                verical_pos = 2
            else:
                verical_pos = 1
            horizontal_pos = {
                "middle": 1,
                "center": 1,
            }.get(align_type, -1)
            position = line_pos_matrix[verical_pos][horizontal_pos]
            new_lines.append(
                f"{line_index}\n" + f"{time}\n" + ("{\\an%s}" % position) \
                .replace("{\\an2}", "") + fix(text) + "\n\n"
            )
            line_index += 1
        with open(self.raw_name + ".srt", "w+", encoding="utf-8") as f:
            f.writelines(new_lines)
