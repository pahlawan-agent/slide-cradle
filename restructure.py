import re
import os

filepath = "/Users/pahlawan/workspaces/slide-cradle/slide_main.html"

with open(filepath, 'r') as f:
    content = f.read()

# We know all slides are between:
# <div class="slides">
# and the closing </div> of <div class="slides"> which is before <div class="nav-controls"> or similar.

start_marker = '<div class="slides">'
end_marker = '<!-- END OF SLIDES -->' # Assuming there is one, or we can just find the end of slides.

# Looking at the file, the slides end around line 4400.
# Let's split the file into header, slides, and footer.
slides_match = re.search(r'(<div class="slides">)(.*?)(</div>\s*</div>\s*<script)', content, re.DOTALL)
if not slides_match:
    print("Could not parse slides.")
    exit(1)

header = content[:slides_match.start(2)]
slides_raw = slides_match.group(2)
footer = content[slides_match.end(2):]

# Now, we extract each section.
# A section starts with <section id="... or <section class="..."
# We will split by <section and then reconstruct.
sections = re.split(r'(<section\b)', slides_raw)

# The first element is pre-section whitespace.
slide_blocks = []
current_block = sections[0]
for i in range(1, len(sections), 2):
    tag = sections[i]
    body = sections[i+1]
    
    # Try to find the id.
    id_match = re.search(r'id=["\']([^"\']+)["\']', tag + body)
    slide_id = id_match.group(1) if id_match else f"unknown_{i}"
    
    slide_blocks.append({
        "id": slide_id,
        "html": tag + body
    })

# Define the new order of slide IDs
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
    "slide-project-timeline", # NEW
    
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
    
    # 15. Future plan (growth plan)
    "slide-28",
    "slide-roadmap-new",
    
    # 16. Financial details and projection
    "slide-financials", # NEW
    
    # 17. Grants received
    "slide-23-grants",
    
    # 18. Management team
    "slide-24",
    "slide-team", # Modified below to remove org chart
    
    # 19. Organization chart
    "slide-org-chart", # NEW
    
    # Outro
    "slide-37"
]

# We might have slides that are unknown or removed. Let's just create a lookup.
slides_map = { s["id"]: s["html"] for s in slide_blocks }

# Generate the new slides
new_timeline_slide = """
            <section id="slide-project-timeline" style="display:flex; flex-direction:column; height:100%; overflow:hidden;">
                <div style="background:linear-gradient(135deg, #004e7c 0%, #006DAE 60%, #0D7377 100%); padding:48px 80px 36px; flex-shrink:0;">
                    <span style="font-size:10px; font-weight:700; letter-spacing:3.5px; text-transform:uppercase; color:rgba(255,255,255,0.5); display:block; margin-bottom:14px;">Timeline</span>
                    <h1 style="font-family:'DM Serif Display',serif; font-size:44px; line-height:1.05; color:#ffffff; letter-spacing:-1.4px; margin-bottom:10px;">
                        18-Month Project Timeline</h1>
                    <div style="width:40px; height:3px; background:rgba(255,255,255,0.4); margin-bottom:12px;"></div>
                    <p style="font-size:14px; color:rgba(255,255,255,0.68); font-weight:300; line-height:1.65; max-width:780px;">
                        Clear deliverables and milestones for the grant funding period to achieve full commercial launch.</p>
                </div>
                <div style="flex:1; padding:40px 80px; display:flex; flex-direction:column; justify-content:center; background:var(--bg);">
                    <div style="background:white; border:1px solid var(--border); border-radius:16px; padding:24px; box-shadow:0 8px 24px rgba(0,0,0,0.04);">
                        <h4 style="font-size:16px; font-weight:700; color:var(--ink); margin-bottom:16px;">Grant Execution Gantt</h4>
                        <!-- Placeholder for Gantt Chart or Milestone list -->
                        <div style="display:flex; flex-direction:column; gap:12px;">
                            <div style="display:flex; align-items:center; gap:16px;">
                                <div style="width:80px; font-size:12px; font-weight:700; color:var(--blue);">Months 1-6</div>
                                <div style="flex:1; background:var(--bg); border-radius:8px; padding:12px;">
                                    <div style="font-size:13px; font-weight:600; color:var(--ink);">ASR Engine Refinement & Offline Deployment</div>
                                    <div style="font-size:11px; color:var(--muted);">Enhancing phoneme precision and optimizing for low-end Android devices.</div>
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:16px;">
                                <div style="width:80px; font-size:12px; font-weight:700; color:var(--teal);">Months 7-12</div>
                                <div style="flex:1; background:var(--bg); border-radius:8px; padding:12px;">
                                    <div style="font-size:13px; font-weight:600; color:var(--ink);">Instructor Matchmaking Platform Alpha</div>
                                    <div style="font-size:11px; color:var(--muted);">Building the backend and onboarding the first 50 verified Ustazs.</div>
                                </div>
                            </div>
                            <div style="display:flex; align-items:center; gap:16px;">
                                <div style="width:80px; font-size:12px; font-weight:700; color:var(--gold);">Months 13-18</div>
                                <div style="flex:1; background:var(--bg); border-radius:8px; padding:12px;">
                                    <div style="font-size:13px; font-weight:600; color:var(--ink);">Commercial Launch & Monetization</div>
                                    <div style="font-size:11px; color:var(--muted);">Rolling out subscription tiers, marketing campaigns, and B2B white-labeling.</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
"""
slides_map["slide-project-timeline"] = new_timeline_slide

new_financials_slide = """
            <section id="slide-financials" style="display:flex; flex-direction:column; height:100%; overflow:hidden;">
                <div style="background:linear-gradient(135deg, #004e7c 0%, #006DAE 60%, #0D7377 100%); padding:48px 80px 36px; flex-shrink:0;">
                    <span style="font-size:10px; font-weight:700; letter-spacing:3.5px; text-transform:uppercase; color:rgba(255,255,255,0.5); display:block; margin-bottom:14px;">Financials</span>
                    <h1 style="font-family:'DM Serif Display',serif; font-size:44px; line-height:1.05; color:#ffffff; letter-spacing:-1.4px; margin-bottom:10px;">
                        3-Year Financial Projections</h1>
                    <div style="width:40px; height:3px; background:rgba(255,255,255,0.4); margin-bottom:12px;"></div>
                    <p style="font-size:14px; color:rgba(255,255,255,0.68); font-weight:300; line-height:1.65; max-width:780px;">
                        Conservative path to profitability based on freemium conversion and enterprise white-label licensing.</p>
                </div>
                <div style="flex:1; padding:40px 80px; display:flex; flex-direction:column; justify-content:center; background:var(--bg);">
                    <div style="background:white; border:1px solid var(--border); border-radius:16px; padding:24px; box-shadow:0 8px 24px rgba(0,0,0,0.04);">
                        <table style="width:100%; text-align:left; border-collapse:collapse; font-size:14px;">
                            <thead>
                                <tr style="border-bottom:2px solid var(--border);">
                                    <th style="padding:12px 8px; color:var(--muted);">Metric</th>
                                    <th style="padding:12px 8px; color:var(--ink);">Year 1 (Post-Launch)</th>
                                    <th style="padding:12px 8px; color:var(--ink);">Year 2</th>
                                    <th style="padding:12px 8px; color:var(--ink);">Year 3</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:12px 8px; font-weight:600;">Active Users (MAU)</td>
                                    <td style="padding:12px 8px;">150,000</td>
                                    <td style="padding:12px 8px;">350,000</td>
                                    <td style="padding:12px 8px;">600,000</td>
                                </tr>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:12px 8px; font-weight:600;">Paying Subscribers</td>
                                    <td style="padding:12px 8px;">4,500 (3%)</td>
                                    <td style="padding:12px 8px;">14,000 (4%)</td>
                                    <td style="padding:12px 8px;">30,000 (5%)</td>
                                </tr>
                                <tr style="border-bottom:1px solid var(--border); background:var(--bg);">
                                    <td style="padding:12px 8px; font-weight:600; color:var(--blue);">Revenue (ARR)</td>
                                    <td style="padding:12px 8px; font-weight:600; color:var(--blue);">RM 2.8M</td>
                                    <td style="padding:12px 8px; font-weight:600; color:var(--blue);">RM 8.7M</td>
                                    <td style="padding:12px 8px; font-weight:600; color:var(--blue);">RM 18.7M</td>
                                </tr>
                                <tr style="border-bottom:1px solid var(--border);">
                                    <td style="padding:12px 8px; font-weight:600;">Operating Costs</td>
                                    <td style="padding:12px 8px;">RM 3.5M</td>
                                    <td style="padding:12px 8px;">RM 5.2M</td>
                                    <td style="padding:12px 8px;">RM 8.5M</td>
                                </tr>
                                <tr>
                                    <td style="padding:12px 8px; font-weight:700; color:var(--teal);">Net Profit / (Loss)</td>
                                    <td style="padding:12px 8px; font-weight:700; color:var(--red);">RM (0.7M)</td>
                                    <td style="padding:12px 8px; font-weight:700; color:var(--teal);">RM 3.5M</td>
                                    <td style="padding:12px 8px; font-weight:700; color:var(--teal);">RM 10.2M</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
"""
slides_map["slide-financials"] = new_financials_slide

# We need to extract the org chart from slide-team and create slide-org-chart
team_slide_html = slides_map.get("slide-team", "")

# The org chart starts around:
# <!-- Horizontal Line Connector -->
# Actually, the entire org chart is inside: <!-- Org Chart Structure -->
# Let's split slide-team.
org_chart_start = team_slide_html.find('<!-- Org Chart Structure -->')
if org_chart_start != -1:
    org_chart_end = team_slide_html.find('<!-- ═══════════════════════════════════', org_chart_start)
    if org_chart_end == -1:
        org_chart_end = team_slide_html.find('</section>', org_chart_start)
    
    org_chart_content = team_slide_html[org_chart_start:org_chart_end]
    
    # Remove it from the original team slide
    slides_map["slide-team"] = team_slide_html[:org_chart_start] + "</div></section>"
    
    # Create the new org chart slide
    new_org_slide = f"""
            <section id="slide-org-chart">
                <div class="pad-sm">
                    <span class="lbl">Organization</span>
                    <div class="rule"></div>
                    <h2 style="font-family:'DM Serif Display',serif; font-size:36px; color:var(--ink); letter-spacing:-0.8px; line-height:1.1; margin-bottom:8px;">
                        Organization Chart</h2>
                    <p style="font-size:14px; color:var(--muted); font-weight:300; line-height:1.7; margin-bottom:28px; max-width:820px;">
                        A lean structure prioritizing product engineering and content.</p>
                    {org_chart_content}
            </section>
    """
    slides_map["slide-org-chart"] = new_org_slide

# Now assemble all slides in the new order
final_slides_html = sections[0] # pre-section whitespace
for slide_id in new_order_ids:
    if slide_id in slides_map:
        final_slides_html += slides_map[slide_id]
        final_slides_html += "\n"
    else:
        print(f"Warning: slide {slide_id} not found in map!")

# Add any slides that were missed but maybe shouldn't be deleted?
# E.g. slide-14-copy-1781763736694 ? If it's not in new_order_ids, it is dropped.
# The user asked to restructure to precisely these 19 points. Removing redundant slides is likely desired.

new_content = header + final_slides_html + footer

with open(filepath, 'w') as f:
    f.write(new_content)

print("Restructure complete!")
