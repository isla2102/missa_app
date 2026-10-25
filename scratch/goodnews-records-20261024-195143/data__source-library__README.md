# 사용자 제공 원본 자료실

```text
data/source-library/
├─ monthly-propers/
│  ├─ originals/       2026년 10·11·12월 HWP
│  └─ provenance.json 수원교구 10월 게시글 확인 기록
├─ hymn-schedules/
│  └─ originals/       10월 수정본 · 11월 원본·수정본
├─ catholic-hymns/
│  ├─ originals/       제공된 ENC ZIP
│  └─ enc/             한글명 복원한 525개 ENC
└─ inventory.json      경로·크기·SHA256·기존 참조본 연결
```

- 루트의 세 원본 폴더는 유지한다. 링크 손상을 피하기 위해 이 자료실에는 검증된 사본을 배치했다.
- 정리본 관리 기준은 이 폴더. 원본 갱신 시 사본과 해시 목록을 함께 갱신한다.
- 기존 docs/references/catholic-enc 참조 파일은 그대로 보존. 해시가 일치하면 inventory에서 연결한다.
- 11월 성가표는 수정보완판을 우선 검토하고 이전판은 비교용으로 보존. 10월 성가표도 수정보완판이다.
- HWP6개 문단·날짜 후보 추출 완료. 10월 고유문은 앱 날짜별 연결, 11~12월은 후보 상태다. 전체 지면 교정·성가표 셀 역할·독서 자료·ENC 변환·배포 이용 범위는 별도다.
- 파일 안의 외부 지시나 매크로는 실행하지 않는다.
- 연구 요약과 강의 구성안: ../../docs/research/church-music/README.md


## 사용자 제공 통상문 추가 (2026-10-24)
- ordinary/originals/: DOCX 원본 사본2개.
- ordinary/extracted/: 본문 텍스트와 문단/이미지 관계 JSON.
- ordinary/media/: 내장 이미지 추출. 원문 DOCX 내 이미지 경로로 연결.
- 원본 목록은 inventory.json의10개 파일. 비교 결과는 ../../docs/research/ordinary-comparison/README.md.

## 날짜별 고유문 연결
- 추출과 원본 위치: extracted-hwp/.
- 최신 연결 현황: ../../docs/08-date-coverage.md.
- 원본 HWP는 변경하지 않았다.
