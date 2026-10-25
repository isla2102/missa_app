import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from link_monthly_propers import split_prayer, split_antiphon, group_observance

def rows(*texts):return [{'text':t,'stream':'BodyText/Section0','recordOffset':i} for i,t in enumerate(texts)]
class Boundaries(unittest.TestCase):
 def test_prayer_keeps_body(self):
  body,tail=split_prayer(rows('하느님,','우리 주 그리스도를 통하여 비나이다.'));self.assertEqual(len(body),2);self.assertEqual(tail,[])
 def test_preface_separated(self):
  body,tail=split_prayer(rows('기도 본문','우리 주 그리스도를 통하여 비나이다.','감사송 <제목>','감사송 본문'));self.assertEqual(len(body),2);self.assertEqual(len(tail),2)
 def test_rubric_separated(self):
  body,tail=split_prayer(rows('기도 본문','성자께서는 영원히 살아 계시며 다스리시나이다.','<신경>'));self.assertEqual(len(tail),1)
 def test_no_ending_rejected(self):
  with self.assertRaises(ValueError):split_prayer(rows('중간에서 끝난 기도'))
 def test_two_endings_rejected(self):
  with self.assertRaises(ValueError):split_prayer(rows('비나이다.','비나이다.'))
 def test_unexpected_tail_rejected(self):
  with self.assertRaises(ValueError):split_prayer(rows('비나이다.','정체를 알 수 없는 다음 문구'))
 def test_internal_rubric_rejected(self):
  with self.assertRaises(ValueError):split_prayer(rows('기도 본문','<별도 지시>','비나이다.'))
 def test_antiphon_unchanged(self):
  body,tail=split_antiphon(rows('주님을 찬미하여라.'));self.assertEqual(len(body),1);self.assertEqual(tail,[])
 def test_gloria_separated(self):
  body,tail=split_antiphon(rows('입당송 본문','<대영광송>'));self.assertEqual(len(body),1);self.assertEqual(len(tail),1)
 def test_observance_multiple_lines(self):
  g={'paragraphs':rows('10월 11일','녹','연중 제28주일','군인 주일','입당송 시편')};self.assertEqual(group_observance(g),'연중 제28주일 · 군인 주일')
if __name__=='__main__':unittest.main()
