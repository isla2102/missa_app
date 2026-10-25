from pathlib import Path
import shutil,re
p=Path('review/02-ia-v27.html');s=p.read_text(encoding='utf-8');s=s.replace(' .reader__turns {',' .reader__turn-boundary[data-next-part="true"] { font-weight: var(--draft-response-weight); text-decoration: underline; }\n .reader__turns {',1).replace('data-js="page-next"','class="reader__turn-boundary" data-js="page-next"');p.write_text(s,encoding='utf-8',newline='\r\n');Path('work/review-ia-v27-check.js').write_text(re.search(r'<script>([\s\S]*?)</script>',s)[1],encoding='utf-8')
entry='''\n## 2026-10-19 페이지 연속 이동 v27\n- 전례별 마지막 펼침에서 다음 전례의 첫 두 페이지, 첫 펼침에서 이전 전례의 마지막 두 페이지로 이동. 미사 전체 첫/끝에서만 해당 방향 비활성화.\n- 다음 순서 안내만 들어가는 빈 페이지를 없애기 위해 전례 전환 블록 제거. 마지막 본문 펼침의 다음 버튼에 정적 강조+느린 3회 강조 애니메이션. 모션 감소 설정은 애니메이션 생략.\n- 뷰어 좌우 Pointer 드래그(64px 이상/가로 우세) 페이지 넘김. 세로 스크롤·조작 버튼·취소 제스처 제외, 이미지 기본 드래그 방지. 클릭 버튼 조작 유지.\n- 감사기도 제2양식의 짧은 사제/합송(각 80자 이하) 3쌍을 2열 묶음으로 배치, 긴 기도는 기존 흐름 유지.\n- node --check 및 test-reader-v27 전체 회귀 통과: 전례 양방향 경계, 전환 블록 없음, 짧은 대화 3쌍, 가로/세로/컨트롤/취소 제스처 검사. 실제 브라우저 Pointer/치수 시각 QA 미실행. 2단계 보완, 최신 review/02-ia-v27.html.\n'''
for name in ['docs/progress.md','design.md']:
 p=Path(name);shutil.copy2(p,'scratch/'+p.name+'.before-v27');p.write_text(p.read_text(encoding='utf-8')+entry,encoding='utf-8',newline='\r\n')
print('v27 history saved.')
