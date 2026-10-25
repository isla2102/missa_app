# Agent Core Directives
1. 작업 시작 전 handoff.md와 Project_Status.md를 먼저 읽고 Next Actions를 확인한다.
2. handoff.md의 타겟 파일과 design.md를 참조하고 무단 전체 스캔을 금지한다.
3. PowerShell 명령 형식을 준수하고, 수정 전 scratch/에 백업하며 CRLF를 유지한다.
4. CLI 명령, 의존성, 마일스톤 변경 시 README.md를 최신화한다.
5. 웹디자인은 사용자가 제공한 8단계 워크플로우를 따른다. docs/progress.md에서 재개하며 각 단계는 질문 3~5개 → 단일 review HTML → 명시적 사용자 승인 → 시스템 검수 → 확정 파일 기록 순으로 진행한다. 단계 밖 작업을 하지 않는다.
6. 4단계 이후 DESIGN.md와 styles/tokens.css를 함께 관리하고 검수한다. CSS 레이어, BEM, 반응형 단일 파일, WCAG 2.2 AA 및 자동 검사 규칙을 준수한다. 상세 웹디자인 작업 전 web-d SKILL.md를 읽는다.
