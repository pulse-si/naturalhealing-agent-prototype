from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
P=Path(__file__).parent
BLD=[278,333,474,556,556,889,722,238,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,333,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584]
def fit(s): return sum(BLD[ord(c)-32] for c in s)*16/1000*1.03+4
ink='#173B68';ground='#FBFFF5';primary='#17458B';muted='#607482';accent='#56734C'
font="Helvetica, Arial, 'Liberation Sans', sans-serif"
nodes=[('start',48,196,184,48,['Open AI Coach'],'terminal'),('choice',320,184,196,72,['Choose a','starting point'],'decision'),('ask',616,112,192,48,['Ask a question'],'process'),('report',616,288,192,48,['Select reports'],'process'),('chat',936,196,208,48,['Discuss with Coach'],'process'),('photo',936,424,208,72,['Add new photos?'],'decision'),('capture',616,424,208,72,['Capture face','or tongue'],'process'),('review',936,624,208,48,['Review summary'],'process'),('end',936,760,208,72,['Save or','continue chatting'],'terminal')]
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="884" viewBox="0 0 1200 884" role="img" aria-label="Proposed NaturalHealing AI Coach interaction flow"><title>NaturalHealing.ai — Proposed AI Coach flow</title><desc>Open the Coach, ask a question or select reports, discuss, optionally add photos, review a summary, then save or continue chatting. Proposed design, not a deployed workflow.</desc><rect width="1200" height="884" fill="{ground}"/>']
def txt(x,y,s,bold=False,anchor='middle',color=ink): return f'<text x="{x}" y="{y}" font-family="{font}" font-size="16" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{color}">{escape(s)}</text>'
svg.append(txt(48,64,'NaturalHealing.ai / Proposed AI Coach flow',True,'start'))
# Orthogonal connectors and independent arrowheads; line ends inside each arrowhead.
def edge(points,label,lx,ly):
    x,y=points[-1]; px,py=points[-2]; dx=0 if px==x else (1 if x>px else -1);dy=0 if py==y else (1 if y>py else -1)
    bx,by=x-dx*12,y-dy*12
    start=points[:-1]+[(bx+dx,by+dy)]
    svg.append(f'<path d="'+ ' '.join(('M' if i==0 else 'L')+f' {a} {b}' for i,(a,b) in enumerate(start))+f'" fill="none" stroke="{primary}" stroke-width="2" stroke-linecap="round"/>')
    svg.append(f'<path d="M {x} {y} L {bx-dy*5} {by+dx*5} L {bx+dy*5} {by-dx*5} Z" fill="{primary}"/>')
    svg.append(txt(lx+16 if lx==1040 else lx,ly,label,anchor='start' if lx==1040 else 'middle',color=muted))
edge([(232,220),(320,220)],'Start',276,204)
edge([(516,208),(564,208),(564,136),(616,136)],'No report',564,100)
edge([(516,232),(564,232),(564,312),(616,312)],'Use records',564,352)
edge([(808,136),(872,136),(872,208),(936,208)],'Question',864,116)
edge([(808,312),(872,312),(872,232),(936,232)],'Context',864,352)
edge([(1040,244),(1040,424)],'Continue',1040,332)
edge([(936,460),(824,460)],'Yes',880,444)
edge([(1040,496),(1040,624)],'Skip photos',1040,568)
edge([(720,496),(720,648),(936,648)],'Return to review',820,632)
edge([(1040,672),(1040,760)],'When ready',1040,724)
for id,x,y,w,h,lines,typ in nodes:
    assert len(' '.join(lines))<=32 and all(fit(s)+28<=w for s in lines),(id,lines)
    assert x-1>=47 and y-1>=47 and x+w+1<=1153 and y+h+1<=837
    fill='#E8F4DC' if typ=='decision' else '#FFFFFF'
    stroke=accent if typ=='decision' else primary
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{24 if typ=="terminal" else 8}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    baseline=y+h/2+(6 if len(lines)==1 else -4)
    for i,line in enumerate(lines):svg.append(txt(x+w//2,int(baseline+i*20),line,True))
svg.append('</svg>');out=''.join(svg);ET.fromstring(out);(P/'naturalhealing-ai-coach-flow.svg').write_text(out)
print('SVG validated: 9 nodes, 10 labeled orthogonal connectors; label fit and bounds pass.')
