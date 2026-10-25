import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from collect_goodnews_daily import parse
from link_goodnews_daily import split_reading
class GoodNews(unittest.TestCase):
 def test_date_mismatch_rejected(self):
  raw=Path('data/source-library/goodnews-daily/html/2026-10-24.html').read_bytes()
  with self.assertRaises(ValueError):parse(raw,'2026-10-25')
 def test_real_date(self):
  raw=Path('data/source-library/goodnews-daily/html/2026-10-24.html').read_bytes();p=parse(raw,'2026-10-24');self.assertIn('복음',p.sections);self.assertNotIn('제2독서',p.sections)
 def test_alternatives_do_not_merge(self):
  raw=Path('data/source-library/goodnews-daily/html/2026-10-11.html').read_bytes();p=parse(raw,'2026-10-11');options,notes=split_reading(p.sections['복음'],'복음');self.assertEqual(len(options),2);self.assertTrue(all(x.count('주님의 말씀입니다.')==1 for x in options))
 def test_missing_response_rejected(self):
  with self.assertRaises(ValueError):split_reading(['▥ 말씀','주님의 말씀입니다.'],'제1독서')
 def test_note_retained(self):
  o,n=split_reading(['▥ 말씀','주님의 말씀입니다.','◎ 하느님, 감사합니다.','<기념일 독서 가능>'],'제1독서');self.assertEqual(n,['<기념일 독서 가능>'])
 def test_notes_between_alternatives_not_in_body(self):
  o,n=split_reading(['✠ 루카가 전한 거룩한 복음입니다.','본문1','주님의 말씀입니다.','◎ 그리스도님, 찬미합니다.','<강론 후 잠시 묵상한다.>','<또는>','✠ 루카가 전한 거룩한 복음입니다.','본문2','주님의 말씀입니다.','◎ 그리스도님, 찬미합니다.'],'복음');self.assertEqual(len(o),2);self.assertNotIn('<강론 후 잠시 묵상한다.>',o[1]);self.assertIn('<강론 후 잠시 묵상한다.>',n)
if __name__=='__main__':unittest.main()
