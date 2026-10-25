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


앱의 보기 설정 → 본당명에서 개인 표시명을 직접 저장할 수 있습니다.기본 본당명 사용으로 이 파일의 name으로 되돌립니다.개인 표시명 변경은 일정·성가를 변경하지 않습니다.다른 본당 일정 프로필 검색·선택은 아직 제공하지 않습니다.


`automaticSelection: nearest-start`는오늘날짜초기선택시현재기기시각과가장가까운시작시간의미사를고릅니다.동률은이후시각.오늘아닌날은defaultSession또는첫회차.같은날짜의수동선택유지.시간은필터에표시하지않고계산에만사용합니다.


sessions.shortLabel은세로필터축약명입니다.가로에서는label을사용하고,값이없으면세로도label로표시합니다.
