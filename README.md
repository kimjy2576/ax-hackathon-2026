# 2026 AX HACKATHON — 지원서 & 서비스 구조도

두 팀의 2026 AX 해커톤 접수 자료 저장소입니다. **접수 마감: 2026-09-01 · 1차 발표(Top30): 09-04**

| 팀 | AI 서비스 | 유형 | 분야 |
|---|---|---|---|
| VirtualCycle선행Project | **THERMA-Crew** — 열시스템 가상 선행연구팀 (5 에이전트) | 가상팀 | 개발(HW) |
| 냉부해(냉동사이클을 부탁해) | **CYCLE-Master** — 사이클 진단 가상전문가 (토론+시뮬레이션 검증 루프) | 가상직원 | 개발(HW) |

## 저장소 구조

```
docs/                  지원서 원문 (Markdown) — 접수 사이트 복붙용
  ├── 팀1_THERMA-Crew_지원서.md
  ├── 팀2_CYCLE-Master_지원서.md
  └── AX_해커톤_지원서.md          # 두 팀 통합 작업 문서 (원본)
applications-html/     지원서 한눈에 보기 (HTML, 브라우저로 열기)
diagrams/
  ├── expert/          제출 규격 구조도 (860px JPG · 편집용 SVG · 캡처용 HTML)
  ├── simple/          일반인용 스토리형 (860px)
  ├── wide/            발표용 16:9 (1920×1080) — 메인 사용
  └── wide-detail/     발표용 16:9 상세 프로세스 — Q&A 백업 슬라이드
tools/                 SVG/HTML 생성 및 캡처 스크립트 (Python + Playwright)
```

## 남은 작업 (TODO)

- [ ] 문서 내 `[확인: …]` 수치 팀 확정 → 일괄 반영
- [ ] Section 3 ↔ Section 7 수치 동기화 (각 문서 하단 체크리스트 참조)
- [ ] 접수 사이트 입력 (SECTION 1~8) 및 구조도 JPG 업로드 (`diagrams/expert/`)

## 구조도 재생성 방법

```bash
cd tools
python3 make_svg.py      # 편집용 순수 SVG 재생성
node shot.js             # 860px 제출용 JPG 캡처 (Playwright + Chromium 필요)
```

문구 수정은 각 HTML/`make_svg.py`에서 텍스트만 고친 뒤 해당 캡처 스크립트를 재실행하면 됩니다.

> ⚠️ 사내 조직·업무 정보가 포함된 자료입니다. **반드시 Private 저장소로 유지하세요.**
