# 본당 미사 일정 설정

`parish.json` 수정 후 `node tools/build-prototype.cjs`로 빌드하고 배포합니다. 외부 일정 자동 수집은 아닙니다.

- name: 본당 표시명
- scheduleStatus: 확인 전 unconfirmed, 실제 일정 확인 후 confirmed
- defaultSession: 기본 회차 ID
- sessions: id / label / weekdays / time
- weekdays: 일요일0~토요일6 배열. null은 요일 미확인으로 기존 회차를 매일 표시하는 호환 상태.
- time: 확인된 24시간 HH:mm, 미확인은 null.
- id는 영문 소문자로 시작하는 최대 40자의 영문 소문자·숫자·하이픈입니다. 기존 dawn/main/youth ID는 저장 편성 호환을 위해 유지하세요. 새 ID는 별도 성가 편성 저장을 사용하며 교중미사 전용 악보는 main에만 연결됩니다.
- 특정 날짜 휴일·특전미사·임시변경은 아직 지원하지 않습니다.
- 일정 없는 날짜는 선택 날짜 미사 일정 없음으로 표시하며 원문 날짜는 바꾸지 않습니다.
