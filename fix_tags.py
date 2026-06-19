import re

filepath = "/Users/pahlawan/workspaces/slide-cradle/slide_main.html"
with open(filepath, 'r') as f:
    content = f.read()

header_end = content.find('<section id="slide-1"')
slides_end = content.find('</div>\n    </div>\n\n    <script data-cfasync')

header = content[:header_end]
slides_raw = content[header_end:slides_end]
footer = content[slides_end:]

sections = []
current_section = ""
for line in slides_raw.splitlines(True):
    if line.strip().startswith('<section id=') and current_section:
        sections.append(current_section)
        current_section = line
    else:
        current_section += line
if current_section:
    sections.append(current_section)

fixed_sections = []
for sec in sections:
    s = sec.strip()
    if not s.endswith('</section>'):
        print("Missing </section> in a slide!")
        # It could be that </section> is followed by something else, but in Reveal it should end with </section>
        # Let's check if it has a </section> at all
        if s.rfind('</section>') == -1:
            sec = sec + "\n            </section>\n"
        else:
            # It has </section> but trailing stuff?
            # E.g. comments. That's fine.
            pass
    fixed_sections.append(sec)

with open(filepath, 'w') as f:
    f.write(header + "".join(fixed_sections) + footer)

print("Fixed closing tags.")
