# -*- coding: utf-8 -*-
"""순수 SVG 구조도 생성 (편집 가능: rect/text 기반, foreignObject 미사용)"""

INK="#1F2430"; SUB="#6B7280"; BD="#E4E7EE"
RED="#E5484D"; RED_S="#FFF1F2"; RED_B="#F7B4B7"
IND="#6366F1"; IND_S="#F1F2FD"; IND_B="#C3C6F5"
GR_S="#F6F7F9"; GR_B="#C6CBD6"; ARROW="#9AA1AE"
FONT="Pretendard, 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif"

def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def rect(x,y,w,h,fill,stroke,rx=16,dash=None,sw=1.5):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

def txt(x,y,s,size,weight,fill,anchor="start",spans=None):
    if spans:
        inner=''.join(f'<tspan font-weight="{w}" fill="{c}">{esc(t)}</tspan>' for t,w,c in spans)
    else:
        inner=esc(s)
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{inner}</text>'

def lines(x,y,ls,size=11,fill=SUB,lh=17,weight=500):
    out=[]
    for i,l in enumerate(ls):
        if isinstance(l,list): out.append(txt(x,y+i*lh,None,size,weight,fill,spans=l))
        else: out.append(txt(x,y+i*lh,l,size,weight,fill))
    return ''.join(out)

def badge(x,y,label,bg="#FFFFFF",fg=IND,size=14,w=30,h=30,rx=9):
    return (rect(x,y,w,h,bg,"none",rx=rx,sw=0)+
            txt(x+w/2,y+h/2+size*0.36,label,size,800,fg,anchor="middle"))

def arrow(x1,y1,x2,y2,color=ARROW,sw=1.8,dash=None,marker="m-gray"):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} marker-end="url(#{marker})"/>'

DEFS=f'''<defs>
<marker id="m-gray" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 Z" fill="{ARROW}"/></marker>
<marker id="m-red" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0.5 L7,4 L0,7.5 Z" fill="{RED}"/></marker>
<marker id="m-ind" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L8,4.5 L0,9 Z" fill="{IND}"/></marker>
</defs>'''

def header(title, subtitle, team, W=860):
    return (txt(28,44,None,19,800,INK,spans=[(title,800,INK)])
           + txt(28+len(title)*0+ (19*0),0,'',0,0,'')  # noop
           + f'<text x="{28}" y="44" font-size="19" font-weight="800" fill="{INK}">{esc(title)}<tspan dx="8" font-size="13" font-weight="600" fill="{SUB}">{esc(subtitle)}</tspan></text>'
           + txt(W-28,44,team,12,800,RED,anchor="end")
           + f'<line x1="0" y1="71" x2="{W}" y2="71" stroke="{BD}" stroke-width="1"/>')

def legend(items,y,x0=28):
    out=[];x=x0
    for kind,label in items:
        if kind=="a": out.append(rect(x,y-11,15,15,IND_S,IND_B,rx=5))
        if kind=="h": out.append(rect(x,y-11,15,15,GR_S,GR_B,rx=8,dash="3 3"))
        if kind=="t": out.append(rect(x,y-11,15,15,"#fff",IND,rx=5))
        if kind=="k": out.append(rect(x,y-11,15,15,GR_S,BD,rx=5))
        if kind=="loop": out.append(f'<line x1="{x}" y1="{y-4}" x2="{x+22}" y2="{y-4}" stroke="{RED}" stroke-width="2.5"/>')
        w0=22 if kind=="loop" else 15
        out.append(txt(x+w0+7,y,label,11,600,SUB))
        x+= w0+7+len(label)*10.0+18
    return ''.join(out)

def chip(x,y,text,w=None,fg="#4B5563",bg="#fff",bd=BD,size=10.5):
    w = w or (len(text)*9.4+24)
    return rect(x,y,w,24,bg,bd,rx=12,sw=1)+txt(x+w/2,y+16,text,size,700,fg,anchor="middle"), w

# ================= C1 : EXACYCLE =================
OY=72; W=860; H1=OY+904+50
c1=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H1}" viewBox="0 0 {W} {H1}" font-family="{FONT}">',
    DEFS, rect(0.75,0.75,W-1.5,H1-1.5,"#fff",BD,rx=18),
    header("EXACYCLE 서비스 구조도","순방향(요구사양 → 설계안) · 과제 유형별 분기 → 공통 백본 수렴","EXACYCLE")]
def Y(y): return y+OY

# 스파인·연결선
for (y1,y2) in [(68,90),(190,212),(444,464),(556,590),(684,702),(812,830)]:
    c1.append(arrow(540,Y(y1),540,Y(y2)))
c1.append(arrow(206,Y(330),298,Y(330),dash="4 4",sw=1.5))
c1.append(arrow(206,Y(496),298,Y(496),color=IND,marker="m-ind"))
c1.append(arrow(300,Y(526),208,Y(526),color=IND,marker="m-ind"))
c1.append(f'<path d="M 780,{Y(632)} L 806,{Y(632)} Q 814,{Y(632)} 814,{Y(624)} L 814,{Y(522)} Q 814,{Y(514)} 806,{Y(514)} L 786,{Y(514)}" stroke="{RED}" stroke-width="1.8" fill="none" marker-end="url(#m-red)"/>')

# 게이트 ①/②
for (gy,no,sm) in [(20,"①","과제 입력 · 설계 브리프 승인"),(834,"②","최종 검토 · 확정")]:
    c1.append(rect(425,Y(gy),230,46,GR_S,GR_B,rx=23,dash="4 4"))
    c1.append(txt(540,Y(gy)+20,f"사람 게이트 {no}",12.5,800,"#4B5563",anchor="middle"))
    c1.append(txt(540,Y(gy)+36,sm,10.5,600,SUB,anchor="middle"))

def agent_card(y,h,no,title,title_gray,ds_lines,ds_y):
    c1.append(rect(300,Y(y),480,h,IND_S,IND_B))
    c1.append(badge(316,Y(y)+14,no))
    sp=[(title,800,INK)]
    if title_gray: sp.append((" "+title_gray,600,SUB))
    c1.append(f'<text x="358" y="{Y(y)+30}" font-size="13.5">'+''.join(
        f'<tspan font-weight="{w}" fill="{c}" font-size="{13.5 if i==0 else 11}">{esc(t)}</tspan>' for i,(t,w,c) in enumerate(sp))+'</text>')
    c1.append(lines(358,Y(ds_y),ds_lines))

agent_card(90,100,"1","PM 에이전트",None,
  [[("과제 접수 → ",500,SUB),("과제 유형 분류(①~④)",800,INK),(" → 해석 조건 번역 · 설계 브리프 생성. 적용 범위",500,SUB)],
   "밖 과제는 한계 명시 후 사람에게 에스컬레이션."],142)

# 설계(플레이북) 그룹
c1.append(rect(300,Y(212),480,232,IND_S,IND_B))
c1.append(badge(316,Y(226),"2"))
c1.append(f'<text x="358" y="{Y(242)}" font-size="13.5"><tspan font-weight="800" fill="{INK}">설계 에이전트 — 과제 유형별 탐색 플레이북 </tspan><tspan font-size="11" font-weight="600" fill="{SUB}">(분기)</tspan></text>')
minis=[("①","제품 설계 검토",["설계변수 공간 탐색 — 열교환기·압축기·","운전조건, 민감도 분석으로 핵심 변수 선별"]),
       ("②","응용 냉동사이클 적용성",["사이클 구성 공간 탐색 — 다단·캐스케이드·","이젝터 등 구성 대안 성능·복잡도 비교"]),
       ("③","대체냉매 탐색",["냉매 후보 공간 탐색 — 물성 DB 스크리닝 후","성능·GWP·가연성 다목적 평가"]),
       ("④","신기술 연구개발",["기술 조사 → 모델 반영 → 적용 효과 정량화","및 연구 시나리오 도출"])]
for i,(no,mn,md) in enumerate(minis):
    mx=316+(i%2)*229; my=Y(266)+(i//2)*92
    c1.append(rect(mx,my,219,82,"#fff",BD,rx=12))
    c1.append(rect(mx+11,my+11,18,18,RED_S,"none",rx=6,sw=0))
    c1.append(txt(mx+20,my+24,no,10.5,800,RED,anchor="middle"))
    c1.append(txt(mx+35,my+24,mn,11.5,800,INK))
    c1.append(lines(mx+11,my+45,md,size=10,lh=15))

agent_card(466,90,"3","해석 에이전트","(공통 백본으로 수렴)",
  ["유형별 탐색 계획을 받아 케이스 자동 생성 → 1D 엔진 일괄 실행 → 수렴·실패 관리","→ 후처리."],518)
agent_card(594,90,"4","검증 에이전트",None,
  [[("에너지 밸런스 · 물성 유효범위 · 경향성 검사. 기준 위반 시 ",500,SUB),("반려(재해석 지시),",800,RED)],
   "통과 결과만 보고로 전달."],646)
agent_card(706,106,"5","보고 에이전트",None,
  ["파레토 프론트 · 검토 보고서 초안 생성.",
   [("유형별 산출물",800,INK),(" — ① 추천 설계안 · ② 구성 비교표 · ③ 냉매 후보 순위표 · ④ 연구개발",500,SUB)],
   "보고서"],758)

# 좌측 레일
c1.append(rect(24,Y(262),182,136,GR_S,BD))
c1.append(txt(39,Y(284),"지식 자산",12,800,INK))
c1.append(lines(39,Y(305),["· 과거 검토 사례·설계 지식","  (RAG)","· 냉매 물성 · 규제(GWP) DB","→ 유형별 플레이북의 근거"],lh=18))
c1.append(rect(24,Y(466),182,90,"#fff",IND))
c1.append(f'<text x="39" y="{Y(488)}" font-size="12.5" font-weight="800" fill="{IND}">1D 사이클 해석 엔진</text>')
c1.append(rect(160,Y(477),34,15,IND,"none",rx=6,sw=0)); c1.append(txt(177,Y(488),"MCP",9,800,"#fff",anchor="middle"))
c1.append(lines(39,Y(510),["자체 개발 해석 프로그램","해석 호출 ⇄ 결과 반환"],lh=17))

# 라벨
c1.append(rect(548,Y(566),108,18,"#fff","none",rx=6,sw=0))
c1.append(txt(552,Y(579),"검증 통과 결과만",10,700,SUB))
c1.append(rect(786,Y(566),56,36,RED_S,RED_B,rx=8,sw=1))
c1.append(txt(814,Y(580),"반려",10,700,RED,anchor="middle"))
c1.append(txt(814,Y(594),"재해석",10,700,RED,anchor="middle"))

# 범례
c1.append(f'<line x1="0" y1="{OY+904}" x2="{W}" y2="{OY+904}" stroke="{BD}" stroke-width="1"/>')
c1.append(legend([("a","AI 에이전트 (5)"),("h","사람 개입 게이트 (2곳)"),("t","도구 · MCP"),("k","지식 자산"),("loop","검증·반려 루프")],OY+904+31))
c1.append('</svg>')
open('EXACYCLE_구조도.svg','w',encoding='utf-8').write(''.join(c1))

# ================= C2 : CYCLE-Master =================
H2=OY+612+50
c2=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H2}" viewBox="0 0 {W} {H2}" font-family="{FONT}">',
    DEFS, rect(0.75,0.75,W-1.5,H2-1.5,"#fff",BD,rx=18),
    header("CYCLE-Master 서비스 구조도","역방향(데이터 → 원인) · 하나의 진단 루프(4단계)","냉부해(냉동사이클을 부탁해)")]

# 연결선
c2.append(arrow(420,Y(166),420,Y(186)))
c2.append(arrow(420,Y(292),420,Y(322)))
c2.append(arrow(484,Y(322),484,Y(298),color=RED,marker="m-red"))
c2.append(arrow(420,Y(442),420,Y(462)))
c2.append(arrow(226,Y(118),246,Y(118)))
c2.append(arrow(226,Y(240),246,Y(240),dash="4 4",sw=1.5))
c2.append(arrow(652,Y(218),672,Y(218)))
c2.append(arrow(672,Y(252),652,Y(252)))
c2.append(arrow(652,Y(360),672,Y(360),color=RED,marker="m-red"))
c2.append(arrow(672,Y(406),652,Y(406),color=RED,marker="m-red"))
c2.append(arrow(652,Y(506),672,Y(506),dash="4 4",sw=1.5))

# 시나리오 칩
c2.append(txt(24,Y(33),"동일 프로세스가 적용되는 사용 시나리오 —",10.5,700,SUB))
cx=278
for t in ["개발 시험 이상 진단","신뢰성 시험 판정","필드 이슈 분석","성능 미달 원인규명"]:
    s,w=chip(cx,Y(18),t); c2.append(s); cx+=w+8

def step(y,h,no,title,title_red,ds):
    c2.append(rect(246,Y(y),406,h,IND_S,IND_B))
    c2.append(badge(262,Y(y)+14,no))
    t=f'<text x="304" y="{Y(y)+30}" font-size="13.5"><tspan font-weight="800" fill="{INK}">{esc(title)}</tspan>'
    if title_red: t+=f'<tspan dx="4" font-size="11" font-weight="600" fill="{RED}">{esc(title_red)}</tspan>'
    c2.append(t+'</text>')
    c2.append(lines(304,Y(y)+52,ds))

step(70,96,"1","즉시 판독",None,["데이터 업로드 즉시 이상 패턴 식별 · 1차 소견 제시 — 전문가 소집 대기","구간이 소멸."])
step(186,106,"2","가설 토론",None,["원인 가설을 우선순위·물리적 근거와 함께 제시하고, 엔지니어의 현장 정보","·반박을 반영해 가설을 갱신."])
step(324,118,"3","시뮬레이션 자가 검증","= 가상 재시험",["가설대로 1D 시뮬레이션을 스스로 실행, 실측 잔차로 가설을 채택/기각.","가설이 갈리면 판별력이 큰 추가 확인 항목을 역제안."])
step(462,112,"4","원인 확정 · 진단 리포트",None,["검증 이력·근거·권고 대책이 포함된 리포트 자동 생성. 모든 가설의 확신도","미달 시 결론을 강요하지 않고 쟁점 정리 후 이관."])

# 좌측 레일
c2.append(rect(24,Y(70),202,96,GR_S,BD))
c2.append(txt(39,Y(92),"사이클 시험 데이터",12,800,INK))
c2.append(lines(39,Y(113),["P-h 선도 · 시계열 거동 업로드","(전 부서 공통 입력)"],lh=17))
c2.append(rect(24,Y(186),202,134,GR_S,BD))
c2.append(txt(39,Y(208),"지식 자산",12,800,INK))
c2.append(lines(39,Y(229),["· 고장 시그니처 라이브러리","  (시뮬레이션 고장 주입 생성)","· 전문가 경험 지식 (RAG)"],lh=18))

# 우측 레일
c2.append(rect(672,Y(186),164,106,GR_S,GR_B,dash="4 4"))
c2.append(txt(687,Y(208),"엔지니어 (전 부서)",12,800,INK))
c2.append(lines(687,Y(229),["선행·개발·신뢰성·생산","현장 정보 제공 · 반박"],lh=17))
c2.append(rect(672,Y(324),164,118,"#fff",IND))
c2.append(f'<text x="687" y="{Y(346)}" font-size="12" font-weight="800" fill="{IND}">1D 사이클</text>')
c2.append(f'<text x="687" y="{Y(362)}" font-size="12" font-weight="800" fill="{IND}">시뮬레이션</text>')
c2.append(rect(754,Y(350),34,15,IND,"none",rx=6,sw=0)); c2.append(txt(771,Y(361),"MCP",9,800,"#fff",anchor="middle"))
c2.append(lines(687,Y(384),["가설대로 사이클 재현"],lh=17))
c2.append(lines(687,Y(402),["가설 → 재현 / 잔차 → 판정"],size=10.5,fill=RED,weight=700,lh=16))
c2.append(rect(672,Y(462),164,112,GR_S,GR_B,dash="4 4"))
c2.append(txt(687,Y(484),"전문가 에스컬레이션",12,800,INK))
c2.append(lines(687,Y(505),["확신도 미달 시","쟁점 정리 후 이관"],lh=17))

# 기각 라벨 칩
c2.append(rect(498,Y(297),132,22,RED_S,RED_B,rx=8,sw=1))
c2.append(txt(564,Y(312),"기각 시 가설 갱신 ↺",10,700,RED,anchor="middle"))
c2.append(txt(246,Y(596),"성능 검증 — 원인 확정 과거 이슈 블라인드 테스트 · 1순위 가설 일치율 80%+ 목표 (생성은 시뮬레이션, 검증은 전문가·실측)",10,700,SUB))

# 범례
c2.append(f'<line x1="0" y1="{OY+612}" x2="{W}" y2="{OY+612}" stroke="{BD}" stroke-width="1"/>')
c2.append(legend([("a","가상전문가의 진단 단계 (1→4)"),("h","사람 (엔지니어·전문가)"),("t","도구 · MCP"),("k","입력 데이터 · 지식 자산"),("loop","시뮬레이션 검증 루프")],OY+612+31))
c2.append('</svg>')
open('CYCLE-Master_구조도.svg','w',encoding='utf-8').write(''.join(c2))
print("svg written")
