# MISSA 디자인 시스템 분석 명세서 (Design System Spec)

**버전:** v1.0 (8단계 검증 완료 기준)  
**최종 갱신:** 2026-10-25  
**쇼케이스 및 템플릿:** [design-system/index.html](file:///c:/Users/imsup/00_개인프로젝트/매일미사_예비신자앱/design-system/index.html)

---

## 1. 개요 및 설계 철학
MISSA 디자인 시스템은 전례(미사)의 거룩함과 경건한 분위기를 유지하면서도, 현대 디지털 독서 기기(태블릿 가로 2페이지 펼침)에서 신자들이 편안하고 직관적으로 기도에 몰입할 수 있도록 8단계의 검증 및 승인 절차를 거쳐 확정되었습니다.

* **서체 분리 (Serif for Content, Sans for UI):** 본문 기도문과 성경 독서는 장엄하고 우아한 명조(Batang), 조작 버튼 및 네비게이션은 가독성이 뛰어난 고딕(Sans) 적용.
* **시각적 위계 (Visual Hierarchy):** 조작 탭은 은은한 와인 틴트(12%), 신자 전체가 함께 바치는 합송(Assembly)은 짙은 와인 채움과 볼드로 강하게 구분.
* **태블릿 안전 영역 (Safe-Area & Gutters):** iPad 실기기 상단 상태바(시계/배터리)와 헤더 겹침을 방지하기 위한 40px 안전영역과 좌우 24px의 단정하고 안정감 있는 마진 구축.

---

## 2. 테마 & 색상 토큰 (Theme & Color Palette)

### 3종 전례 테마
| 테마 | 명칭 | 배경 (Canvas) | 지면 (Paper) | 글자 (Ink) | 와인 강조 (Accent) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Theme A (기본)** | 부드러운 미색 | `#EEE7DA` | `#F7F1E7` | `#25342E` | `#70283F` |
| **Theme B** | 짙은 종이색 (양피지) | `#E2D7C3` | `#EFE7D8` | `#2C261F` | `#7A2232` |
| **Theme C** | 편안한 다크 (미사 다크) | `#1C1819` | `#272223` | `#E8E2D9` | `#D47087` |

### 주요 시맨틱 토큰
* `--reader-theme-bg`: 앱 배경 캔버스
* `--reader-theme-surface`: 책 페이지 및 카드 지면색
* `--reader-theme-ink`: 본문 텍스트 색상
* `--reader-theme-accent`: 대제목 및 주요 포인트 와인색
* `--reader-theme-line`: 은은한 경계선 색상
* `--state-selected-surface`: 선택된 탭 배경 (와인 12% 믹스)
* `--assembly-surface`: 신자 합송 배경 (짙은 와인 #70283F)
* `--assembly-ink`: 신자 합송 글자색 (#FFFFFF)

---

## 3. 타이포그래피 계층 (Typography Scale)

* **대제목 (Part Title):** `1.5rem` (24px) / Line-height `1.3` / Bold 700 / 고딕
* **중제목 (Section Title):** `1.25rem` (20px) / Line-height `1.3` / Bold 700 / 고딕
* **본문 (Body Reading):** `1.125rem` (18px) / Line-height `1.6` / Regular 400 / 명조 (설정에서 고딕 전환 가능)
* **UI / 컨트롤 (Buttons & Inputs):** `1.0rem` (16px) / Line-height `1.6` / Regular 400 / 고딕
* **보조 안내 / 원문 지침 (Guidance):** `0.875rem` (14px) / Line-height `1.5` / Regular 400 / 고딕

---

## 4. 공간 및 레이아웃 (Spacings & Layout)

* **상단 상태바 안전영역:** `calc(var(--reader-system-space-4) + env(safe-area-inset-top, 24px))` = **40px**
* **좌우 베젤 여백:** `max(var(--reader-system-space-6), calc(var(--reader-system-space-4) + env(safe-area-inset-left, 0px)))` = **24px (1.5rem)**
* **하단 홈 바 안전영역:** `max(var(--reader-system-space-4), env(safe-area-inset-bottom, 0px))` = **16px**
* **모서리 곡률 (Radius):** `--reader-radius: 0.75rem` (12px)
* **그리드 간격 (Gap):** `--reader-gap: 1rem` (16px)

---

## 5. 핵심 컴포넌트 아키텍처

1. **버튼 (`.missa-button`)**:
   * 기본: 얇은 실선 테두리 + 종이 바탕
   * 선택 활성 (`[aria-pressed="true"]`): 은은한 와인 틴트 면 + 굵은 글씨
   * Primary (`.missa-button--primary`): 종이 바탕 + 와인 테두리/글자
2. **입력 폼 (`.missa-input`)**:
   * 종이 바탕 + 0.75rem 곡률 + 얇은 실선 테두리
3. **신자 합송 강조 (`.missa-response`)**:
   * 짙은 와인 배경 + 흰색 텍스트 + 볼드체로 미사 참여 유도
4. **전례문 2열 스피치 그리드 (`.reader__speech-row`)**:
   * 1열: 사제 기호(`+`, `✠`), 신자 기호(`◎`), 성경 절 번호(`17`, `18`)
   * 2열: 말씀 본문
5. **오버레이 모달 (`dialog.overlay`)**:
   * 중앙 팝업, 90dvh 높이, 딤드 백드롭, `.overlay__body` 내부 스크롤 보장

---

## 6. 재사용 스타터 템플릿 사용법
* 브라우저에서 [design-system/index.html](file:///c:/Users/imsup/00_개인프로젝트/매일미사_예비신자앱/design-system/index.html)을 열면 모든 컴포넌트의 실시간 렌더링을 확인하고, 우측 상단 **[코드 복사]** 버튼을 통해 즉시 새로운 페이지의 기본 뼈대로 사용할 수 있습니다.
