from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
html = (root/'review/02-ia-v5.html').read_text(encoding='utf-8').replace('검토 v5','검토 v6')
specs = {
 '입당 성가': {'kind':'hymn','source':'hymnSet','role':'entrance'},
 '성호경': {'kind':'fixed','source':'ordinary'},
 '인사': {'kind':'choice','source':'celebrant','guide':'사제가 선택한 인사 양식에 따라 참여합니다.'},
 '참회 예식': {'kind':'choice','source':'celebrant','guide':'사제가 선택한 참회 예식 양식에 따라 참여합니다.'},
 '자비송': {'kind':'fixed','source':'ordinary','condition':'선택한 예식에 따라 적용'},
 '대영광송': {'kind':'fixed','source':'ordinary','condition':'전례일에 따라 포함 여부 결정'},
 '본기도': {'kind':'proper','source':'liturgicalDay'},
 '제1독서': {'kind':'proper','source':'liturgicalDay'},
 '화답송': {'kind':'proper','source':'liturgicalDay'},
 '제2독서': {'kind':'proper','source':'liturgicalDay','condition':'전례일에 따라 적용'},
 '복음 환호송': {'kind':'proper','source':'liturgicalDay'},
 '복음': {'kind':'proper','source':'liturgicalDay'},
 '강론': {'kind':'choice','source':'celebrant','guide':'사제 또는 부제의 강론을 듣습니다.'},
 '신앙 고백': {'kind':'choice','source':'celebrant','guide':'적용되는 전례일에 선택된 신앙 고백 양식으로 참여합니다.'},
 '보편 지향 기도': {'kind':'choice','source':'parish','guide':'본당에서 준비한 기도 지향에 따라 함께 기도합니다.'},
 '예물 준비 · 봉헌 성가': {'kind':'hymn','source':'hymnSet','role':'offertory'},
 '예물 기도': {'kind':'proper','source':'liturgicalDay'},
 '감사 기도': {'kind':'choice','source':'celebrant','guide':'사제가 선택한 감사 기도 양식에 따라 참여합니다.'},
 '주님의 기도': {'kind':'fixed','source':'ordinary'},
 '평화 예식': {'kind':'choice','source':'celebrant','guide':'사제의 안내에 따라 평화 예식에 참여합니다.'},
 '영성체 예식 · 영성체 성가': {'kind':'proper','source':'liturgicalDay','role':'communion'},
 '영성체 후 기도': {'kind':'proper','source':'liturgicalDay'},
 '공지 사항': {'kind':'choice','source':'parish','guide':'본당 공지가 있으면 안내를 듣습니다.'},
 '강복': {'kind':'choice','source':'celebrant','guide':'사제가 선택한 강복 양식에 따라 참여합니다.'},
 '파견': {'kind':'choice','source':'celebrant','guide':'선택된 파견 양식에 따라 응답합니다.'},
 '파견 성가': {'kind':'hymn','source':'hymnSet','role':'recessional'}
}
model = 'const frameSpecs = '+json.dumps(specs,ensure_ascii=False)+';\n'
model += '''const mockParagraph = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.';
function renderItem(item) {
 const spec = frameSpecs[item.title];
 const section = document.createElement('section'); section.className = 'reader__item'; section.id = item.id; section.tabIndex = -1;
 const heading = document.createElement('h3'); heading.className = 'reader__item-title'; heading.textContent = item.title;
 if (item.id === selectedItem) { section.setAttribute('aria-current','location'); heading.textContent += ' · 현재 위치'; }
 section.append(heading);
 if (spec.kind === 'choice') {
  const guide = document.createElement('p'); guide.className = 'reader__item-text'; guide.textContent = spec.guide; section.append(guide);
 } else {
  const container = spec.kind === 'fixed' ? section : document.createElement('div');
  if (spec.kind !== 'fixed') { container.className = 'reader__content-card'; container.setAttribute('data-content-source',spec.source); }
  const paragraph = document.createElement('p'); paragraph.className = 'reader__item-text'; paragraph.lang = 'la'; paragraph.textContent = mockParagraph;
  container.append(paragraph);
  if (spec.kind !== 'fixed') section.append(container);
 }
 return section;
}
'''
html=html.replace('let selectedItem = null;',model+'\nlet selectedItem = null;')
start=html.index("  const h = document.createElement('h3'); h.className = 'reader__page-title';")
end=html.index("  find('book').append(page);", start)
html=html[:start]+'''  contents[part].filter(item => item.page === spread * 2 + i).forEach(item => page.append(renderItem(item)));
'''+html[end:]
html=html.replace('공통 주일 문서 · 공식 본문 미연동', '공통 주일 문서 · MOCK 본문(Lorem ipsum) · 공식 자료 미연동')
html=html.replace("text('현재 예식의 내용이 왼쪽→오른쪽 두 페이지로 이어집니다.","text('현재 예식의 내용이 왼쪽→오른쪽 두 페이지로 이어집니다.")
html=html.replace("  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');", '''  text('프레임 규칙: 각 순서의 타이틀 아래에 변동 본문은 카드, 고정 기도문은 카드 없는 본문, 선택 양식은 짧은 안내를 표시합니다. 모든 라틴어 본문은 Lorem ipsum mock입니다.');
  text('변동 본문 카드는 매일미사·전례집 자료 연결을 위한 자리입니다. 고정 본문은 통상문 자료를 사용합니다. 적용 여부와 선택 양식은 공식 데이터·본당 선택 확인 후 결정하며, 현재 분류는 프레임 검토용입니다.');
  text('입당·봉헌·영성체·파견 성가 편성은 회차별 HymnSet입니다. 매일미사의 입당송·영성체송 같은 공통 전례일 본문과 구분합니다. 현재 모든 자료 연동·성가 편집은 미구현입니다.');
  text('영성체 프레임은 공통 본문 카드 위치를 보여줍니다. 세부 통상문·영성체송·회차별 성가의 내부 구성은 후속 프레임에서 나눌 수 있습니다.');
  text('테마와 글자 크기는 이번 정보 구조 단계에서 확정하지 않습니다. 화면 조작은 승인으로 기록되지 않습니다.');''')
html=html.replace('--draft-gap: .75rem;', '--draft-item-gap: .75rem; --draft-content-inset: .625rem; --draft-gap: .75rem;')
html=html.replace('.reader__page-title { margin-block: 0 var(--draft-gap); }', '.reader__item { margin-block-end: var(--draft-item-gap); }\n .reader__item-title { margin-block: 0 var(--draft-toc-gap); }\n .reader__item-text { margin-block: 0; }\n .reader__content-card { border: 1px solid; padding: var(--draft-content-inset); }')
with (root/'review/02-ia-v6.html').open('w',encoding='utf-8',newline='\r\n') as f: f.write(html)
(root/'work/review-ia-v6-check.js').write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')
print('Created v6: all 26 items use titled frames and mock content')
