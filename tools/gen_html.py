# -*- coding: utf-8 -*-
"""팀별 지원서 MD → 접수 사이트 톤 HTML 변환"""
import re, html

CSS = """
:root{--ink:#1F2430;--sub:#6B7280;--bd:#E4E7EE;--red:#E5484D;--red-s:#FFF1F2;--red-b:#F7B4B7;--ind-b:#C3C6F5;
--ind:#6366F1;--ind-s:#F1F2FD;--ind-b:#C3C6F5;--gr:#F6F7F9;--gr-b:#C6CBD6;--amber:#8A6D1D;--amber-s:#FBF6E7;--amber-b:#E4D3A1}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;background:#EDEFF3;color:var(--ink);
word-break:keep-all;line-height:1.7;padding:40px 16px 80px}
.wrap{max-width:920px;margin:0 auto}
.hero{background:#fff;border:1px solid var(--bd);border-radius:18px;padding:30px 34px;margin-bottom:20px;
display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.hero .k{font-size:11px;font-weight:800;letter-spacing:.12em;color:var(--red);margin-bottom:6px}
.hero h1{font-size:25px;font-weight:800;letter-spacing:-.01em;line-height:1.35}
.hero .team{font-size:13px;font-weight:700;color:var(--sub);margin-top:6px}
.hero .team b{color:var(--red)}
.score{background:var(--gr);border:1px solid var(--bd);border-radius:14px;padding:12px 16px;font-size:11px;color:var(--sub);min-width:230px}
.score b{color:var(--ink)}
.toc{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:22px}
.toc a{display:flex;align-items:center;gap:7px;background:#fff;border:1px solid var(--bd);border-radius:999px;
padding:7px 14px 7px 8px;font-size:11.5px;font-weight:700;color:var(--sub);text-decoration:none}
.toc a span{width:22px;height:22px;border-radius:999px;background:var(--gr);display:flex;align-items:center;justify-content:center;
font-size:11px;font-weight:800;color:var(--sub)}
.toc a:hover{border-color:var(--red-b);color:var(--ink)}
.sec{background:#fff;border:1px solid var(--bd);border-radius:18px;padding:28px 34px;margin-bottom:18px}
.sec>.shead{display:flex;align-items:center;gap:12px;margin-bottom:16px;padding-bottom:14px;border-bottom:1px solid var(--bd)}
.sec>.shead .no{width:32px;height:32px;border-radius:999px;background:var(--red);color:#fff;display:flex;align-items:center;
justify-content:center;font-size:14px;font-weight:800;flex:none}
.sec>.shead h2{font-size:17px;font-weight:800}
.sec h3{font-size:13.5px;font-weight:800;margin:20px 0 8px;display:flex;align-items:center;gap:8px}
.sec h3::before{content:"";width:4px;height:14px;border-radius:2px;background:var(--ind);flex:none}
.sec p{font-size:13px;color:#374151;margin:8px 0}
.sec ul{margin:8px 0 8px 4px;list-style:none}
.sec ul li{font-size:13px;color:#374151;padding-left:16px;position:relative;margin:5px 0}
.sec ul li::before{content:"·";position:absolute;left:2px;color:var(--ind);font-weight:800}
.kv{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:4px}
.kv .cell{background:var(--gr);border:1px solid var(--bd);border-radius:12px;padding:11px 14px;font-size:12.5px}
.kv .cell.full{grid-column:1/-1}
.kv .cell b{display:block;font-size:10.5px;color:var(--sub);letter-spacing:.04em;margin-bottom:3px}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:12.5px}
th,td{border:1px solid var(--bd);padding:8px 12px;text-align:left}
th{background:var(--gr);font-weight:800;font-size:11.5px;color:var(--sub)}
td b{color:var(--red)}
.flow{display:grid;grid-template-columns:1fr 34px 1fr;gap:0 6px;align-items:start;margin-top:8px}
.flow .colh{font-size:11px;font-weight:800;letter-spacing:.06em;margin-bottom:8px}
.flow .colh.a{color:var(--sub)} .flow .colh.b{color:var(--ind)}
.step{border-radius:12px;padding:9px 12px 9px 10px;margin-bottom:8px;display:flex;gap:9px;align-items:flex-start;font-size:12px;line-height:1.55}
.step .n{flex:none;width:20px;height:20px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:10.5px;font-weight:800}
.step.a{background:var(--gr);border:1.5px dashed var(--gr-b)}
.step.a .n{background:#fff;color:var(--sub)}
.step.b{background:var(--ind-s);border:1.5px solid var(--ind-b)}
.step.b .n{background:#fff;color:var(--ind)}
.step .rep{display:inline-block;background:#fff;border:1px solid var(--ind-b);color:var(--ind);border-radius:999px;
font-size:10px;font-weight:800;padding:1px 8px;margin-top:5px}
.mid{display:flex;align-items:center;justify-content:center;height:100%;color:var(--gr-b);font-size:18px;padding-top:30px}
.note{background:var(--amber-s);border:1px solid var(--amber-b);border-radius:12px;padding:12px 16px;font-size:12px;color:var(--amber);margin:12px 0}
.note b{color:var(--amber)}
.chk{background:var(--red-s);border:1px solid var(--red-b);border-radius:12px;padding:12px 16px;font-size:12px;color:#8A2A2E;margin:12px 0}
mark{background:var(--red-s);color:var(--red);font-weight:700;border-radius:4px;padding:0 3px}
.srcnote{font-size:12.5px;color:#4B5563;margin:2px 0 2px 8px;line-height:1.65}
.srcnote.lbl0{margin-top:10px;font-weight:800;color:#374151}
.svgbox{border:1px solid var(--bd);border-radius:14px;overflow:hidden;margin-top:10px}
.svgbox svg{display:block;width:100%;height:auto}
.foot{font-size:11px;color:var(--sub);text-align:center;margin-top:26px}
"""

HIGHLIGHTS = ['40시간','1,920시간','2,400시간','3,840시간','960시간','5,760~6,240시간','6,240시간','3.3명','12건','60건','432 Hr','2,160 Hr','90%','50% 이상','12명','25명','80명','105명','8조원','800억원','3조원','500만원','연 20회','1.0억원','300만원','연 10건','0.3억원','1.3억원','효과율 1%','효율 1%']

def inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[확인: *(.*?)\]', r'<mark>확인 필요: \1</mark>', t)
    t = re.sub(r'_\((.+?)\)_', r'<i style="color:var(--sub)">(\1)</i>', t)
    _terms = sorted(HIGHLIGHTS, key=len, reverse=True)
    for i, term in enumerate(_terms):
        t = t.replace(term, f'\x00{i}\x01')
    for i, term in enumerate(_terms):
        t = t.replace(f'\x00{i}\x01', f'<mark>{term}</mark>')
    return t

def render_body(md, svg_inline, team_no):
    lines = md.split('\n'); out=[]; i=0; sec_open=False; secno=0
    sec_titles={}
    def close():
        nonlocal sec_open
        if sec_open: out.append('</div>')
        sec_open=False
    while i < len(lines):
        l = lines[i]
        if l.startswith('## SECTION'):
            close()
            m = re.match(r'## SECTION (\d+)\. (.+)', l); secno=int(m.group(1)); title=m.group(2)
            out.append(f'<div class="sec" id="s{secno}"><div class="shead"><div class="no">{secno}</div><h2>{html.escape(title)}</h2></div>')
            sec_open=True; sec_titles[secno]=title
        elif l.startswith('### '):
            t=l[4:]
            if 'AS-IS 워크플로우' in t:
                # AS-IS 블록과 이어지는 TO-BE 블록을 함께 파싱
                asis=[]; i+=1
                while i<len(lines) and not lines[i].startswith('### '):
                    m=re.match(r'(\d+)\. (.+)', lines[i].strip())
                    if m: asis.append((m.group(1), m.group(2)))
                    i+=1
                tobe_title=lines[i][4:]; i+=1; tobe=[]
                while i<len(lines) and not lines[i].startswith('### '):
                    m=re.match(r'(\d+)\. (.+)', lines[i].strip())
                    if m: tobe.append((m.group(1), m.group(2)))
                    i+=1
                out.append(f'<div class="flow"><div><div class="colh a">AS-IS · {html.escape(t.split("(")[-1].rstrip(")"))}</div>')
                for n,txt in asis:
                    out.append(f'<div class="step a"><div class="n">{n}</div><div>{inline(txt)}</div></div>')
                out.append('</div><div class="mid">→</div><div>')
                out.append(f'<div class="colh b">TO-BE · {html.escape(tobe_title.split("(")[-1].rstrip(")"))}</div>')
                for n,txt in tobe:
                    m2=re.search(r'—\s*\*(대체: .+?)\*\s*$', txt)
                    rep=''; body=txt
                    if m2: rep=f'<span class="rep">{html.escape(m2.group(1))}</span>'; body=txt[:m2.start()]
                    out.append(f'<div class="step b"><div class="n">{n}</div><div>{inline(body)}{rep}</div></div>')
                out.append('</div></div>')
                continue
            elif 'AI 서비스 구조도' in t:
                out.append(f'<h3>{html.escape(t)}</h3>')
                i+=1
                while i<len(lines) and not (lines[i].startswith('## ') or lines[i].startswith('# ')):
                    if lines[i].strip(): out.append(f'<p>{inline(lines[i].strip())}</p>')
                    i+=1
                out.append(f'<div class="svgbox">{svg_inline}</div>')
                continue
            else:
                out.append(f'<h3>{inline(t)}</h3>')
        elif l.startswith('| '):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not set(''.join(cells)) <= set('-: '): rows.append(cells)
                i+=1
            out.append('<table><tr>'+''.join(f'<th>{inline(c)}</th>' for c in rows[0])+'</tr>')
            for r in rows[1:]: out.append('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in r)+'</tr>')
            out.append('</table>')
            continue
        elif l.startswith('[산출 근거]'):
            out.append('<p class="srcnote lbl0">[산출 근거]</p>'); i+=1
            while i<len(lines) and lines[i].startswith('· '):
                out.append(f'<p class="srcnote">· {inline(lines[i][2:])}</p>'); i+=1
            continue
        elif l.startswith('> '):
            out.append(f'<div class="chk"><b>✓ 팀 확정 필요 — </b>{inline(l[2:].replace("동기화 필요: ",""))}</div>')
        elif l.startswith('- '):
            items=[]
            while i<len(lines) and lines[i].startswith('- '):
                items.append(lines[i][2:]); i+=1
            out.append('<ul>'+''.join(f'<li>{inline(x)}</li>' for x in items)+'</ul>')
            continue
        elif re.match(r'\d+\. ', l.strip()):
            items=[]
            while i<len(lines) and re.match(r'\d+\. ', lines[i].strip()):
                items.append(re.match(r'\d+\. (.+)', lines[i].strip()).group(1)); i+=1
            out.append('<ul>'+''.join(f'<li>{inline(x)}</li>' for x in items)+'</ul>')
            continue
        elif l.startswith('**서비스가 담당하는'):
            out.append(f'<div class="note">{inline(l)}</div>')
        elif l.strip() and not l.startswith('#') and not l.startswith('---'):
            out.append(f'<p>{inline(l.strip())}</p>')
        i+=1
    close()
    return ''.join(out), sec_titles

def build(team_md_file, svg_file, out_file, team_no, service, teamname, field, ptype):
    md = open(team_md_file, encoding='utf-8').read()
    body_md = md.split('\n## SECTION 2')[1]
    body_md = '## SECTION 2' + body_md.split('# 공통 전략 메모')[0]
    # 기본정보(섹션1) 카드용 정보는 인자로
    svg = open(svg_file, encoding='utf-8').read()
    svg = re.sub(r'width="\d+" height="\d+"', '', svg, count=1)
    body, titles = render_body(body_md, svg, team_no)
    toc = ''.join(f'<a href="#s{n}"><span>{n}</span>{html.escape(t)}</a>'
                  for n,t in [(1,'기본 정보')]+sorted(titles.items()))
    sec1 = f'''<div class="sec" id="s1"><div class="shead"><div class="no">1</div><h2>기본 정보</h2></div>
    <div class="kv">
      <div class="cell"><b>팀명</b>{html.escape(teamname)}</div>
      <div class="cell"><b>AI서비스(Agent)명</b>{html.escape(service)}</div>
      <div class="cell"><b>업무 분야</b>{html.escape(field)}</div>
      <div class="cell"><b>제안 유형</b>{html.escape(ptype)}</div>
    </div></div>'''
    page = f'''<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>2026 AX HACKATHON — {html.escape(service)} 지원서</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>{CSS}</style></head><body><div class="wrap">
<div class="hero"><div>
  <div class="k">2026 AX HACKATHON · 지원서</div>
  <h1>{html.escape(service)}</h1>
  <div class="team">팀 <b>{html.escape(teamname)}</b> · {html.escape(field)} · {html.escape(ptype)}</div>
</div>
<div class="score"><b>심사 배점(70)</b> — 문제정의 10 · 중요도 10 · 구성계획 10 · AI 필요성 10 · 활용확대 10 · <b>절감시간 15</b> · 경영기여 5</div>
</div>
<div class="toc">{toc}</div>
{sec1}
{body}
<div class="foot">2026 AX HACKATHON 지원서 초안 · [확인 필요] 표시는 팀 확정 후 접수 사이트 입력 전 반영</div>
</div></body></html>'''
    open(out_file,'w',encoding='utf-8').write(page)
    print(out_file, 'written')

build('팀1_EXACYCLE_지원서.md','EXACYCLE_구조도.svg','팀1_EXACYCLE_지원서.html',
      1,'EXACYCLE','EXACYCLE','개발(HW)','가상팀 (Virtual Team)')
build('팀1_EXACYCLE_지원서_근거포함.md','EXACYCLE_구조도.svg','팀1_EXACYCLE_지원서_근거포함.html',
      1,'EXACYCLE (근거 주석판)','EXACYCLE','개발(HW)','가상팀 (Virtual Team)')
build('팀1_EXACYCLE_지원서_접수최적.md','EXACYCLE_구조도.svg','팀1_EXACYCLE_지원서_접수최적.html',
      1,'EXACYCLE (접수 최적판)','EXACYCLE','개발(HW)','가상팀 (Virtual Team)')
build('팀2_CYCLE-Master_지원서.md','CYCLE-Master_구조도.svg','팀2_CYCLE-Master_지원서.html',
      2,'CYCLE-Master','냉부해(냉동사이클을 부탁해)','개발(HW)','가상직원 (Virtual Employee)')
