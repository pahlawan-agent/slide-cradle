import re

filepath = "/Users/pahlawan/workspaces/slide-cradle/slide_main.html"

with open(filepath, 'r') as f:
    content = f.read()

# 1. Separate header, slides, and footer
header_end = content.find('<section id="slide-1"')
slides_end = content.find('</div>\n    </div>\n\n    <script data-cfasync')

if header_end == -1 or slides_end == -1:
    print("Could not find boundaries.")
    exit(1)

header = content[:header_end]
slides_raw = content[header_end:slides_end]
footer = content[slides_end:]

# 2. Extract slides
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

slides_map = {}
for sec in sections:
    match = re.search(r'<section id="([^"]+)"', sec)
    if match:
        slides_map[match.group(1)] = sec

# 3. Create Org Chart Slide if not exists
if "slide-org-chart" not in slides_map and "slide-team" in slides_map:
    team_html = slides_map["slide-team"]
    org_start = team_html.find('<!-- Org Chart Structure -->')
    if org_start != -1:
        # find the end of the section
        org_end = team_html.rfind('</section>')
        org_chart_content = team_html[org_start:org_end]
        
        # update slide-team
        slides_map["slide-team"] = team_html[:org_start] + "</section>\n"
        
        # create slide-org-chart
        slides_map["slide-org-chart"] = f"""<section id="slide-org-chart">
                <div class="pad-sm" style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%;">
                    <span class="lbl" style="color:var(--gold);">Organization</span>
                    <h2 style="font-family:'DM Serif Display',serif; font-size:36px; color:var(--ink); letter-spacing:-0.8px; margin-bottom:8px;">
                        Organization Chart</h2>
                    <p style="font-size:14px; color:var(--muted); font-weight:300; line-height:1.7; margin-bottom:28px;">
                        A lean structure prioritizing product engineering and content.</p>
                    <div style="transform:scale(0.85); transform-origin:top center;">
                    {org_chart_content}
                    </div>
                </div>
            </section>\n"""

# 4. Define EXACT order based on the 19 points
new_order_ids = [
    # 1. Problem statement
    "slide-1",
    "slide-2",
    "slide-7",
    
    # 2. Solution
    "slide-8",
    
    # 3. Underlying technology & Innovation
    "slide-11",
    "slide-9",
    "slide-10",
    
    # 4. Features and functionalities
    "slide-14",
    "slide-15",
    "slide-feature-themes",
    "slide-core-features",
    "slide-demo-matchmaking",
    
    # 5. Uniqueness and Competitive advantage
    "slide-12",
    
    # 6. Competitors analysis
    "slide-11-copy-1781765125593",
    "slide-13",
    
    # 7. Value proposition
    "slide-13-vp1",
    
    # 8. Current stage of product development
    "slide-27",
    
    # 9. Development plan & project timeline
    "slide-project-timeline",
    
    # 10. Previous test or technological validation
    "slide-validation",
    
    # 11. Collaboration or partners
    "slide-31",
    "slide-32",
    
    # 12. Proposed revenue model and pricing model
    "slide-20",
    "slide-21",
    
    # 13. Go-to-market strategy
    "slide-29",
    "slide-30",
    "slide-strategy-timeline",
    
    # 14. Current traction and clients
    "slide-17",
    "slide-19",
    
    # 15. Future plan (roadmap/growth)
    "slide-28",
    "slide-roadmap-new",
    
    # 16. Historical financial details and projection
    "slide-financials",
    
    # 17. Details of other grants received previously
    "slide-23-grants",
    
    # 18. Management team
    "slide-24",
    "slide-team",
    
    # 19. organization chart
    "slide-org-chart",
    
    # Closing
    "slide-37"
]

final_slides_html = ""
for slide_id in new_order_ids:
    if slide_id in slides_map:
        final_slides_html += slides_map[slide_id]
        if not final_slides_html.endswith('\n'):
            final_slides_html += '\n'
    else:
        print(f"Warning: Missing slide {slide_id}")

# 5. Write back
with open(filepath, 'w') as f:
    f.write(header + final_slides_html + footer)

print("Slides perfectly ordered!")
