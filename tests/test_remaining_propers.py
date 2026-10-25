import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from link_remaining_propers import choose_group,web_body_prefix
from link_monthly_propers import split_antiphon

def group(label,sections=True):return {'sections':[{'title':'本기도'}] if sections else [],'paragraphs':[{'text':'12월25일'},{'text':label}]}
class Forms(unittest.TestCase):
 def test_default_matches_named_form(self):
  a,b=group('첫째 미사'),group('둘째 미사');self.assertIs(choose_group([a,b],'위령의 날 - 첫째 미사'),a)
 def test_morning_not_vigil(self):
  a,b=group(''),group('성탄 전야 미사');self.assertIs(choose_group([a,b],'12월24일'),a)
 def test_header_not_prayer_form(self):
  a,b=group('',False),group('');self.assertIs(choose_group([a,b],'12월17일'),b)
 def test_ambiguous_rejected(self):
  with self.assertRaises(ValueError):choose_group([group(''),group('')],'12월24일')
 def test_missing_named_form_rejected(self):
  with self.assertRaises(ValueError):choose_group([group('낮 미사')],'밤 미사')
 def test_abbreviated_ending_not_compared_as_body(self):self.assertEqual(web_body_prefix(['기도 본문','주님께서는 성부와 …….']),'기도 본문')
 def test_advent_instruction_separated(self):
  body,tail=split_antiphon([{'text':'입당송 본문'},{'text':'<대영광송 없음>'}]);self.assertEqual(len(body),1);self.assertEqual(len(tail),1)
 def test_lord_within_body_is_kept(self):self.assertEqual(web_body_prefix(['주님,','주님께서는 인자하시니','죄를 씻어 주소서.','우리 주 …….']),'주님, 주님께서는 인자하시니 죄를 씻어 주소서.')
if __name__=='__main__':unittest.main()
