from pathlib import Path
import sys,json,copy
sys.path.insert(0,'work/schema-deps')
from jsonschema import Draft202012Validator,FormatChecker
schema=json.loads(Path('schemas/mass-document.schema.json').read_text(encoding='utf-8'));doc=json.loads(Path('data/days/2026-10-18.json').read_text(encoding='utf-8'));Draft202012Validator.check_schema(schema);v=Draft202012Validator(schema,format_checker=FormatChecker());v.validate(doc)
for mutate in [lambda x:x.update(date='2026-02-30'),lambda x:x.update(bodyOverride='other'),lambda x:x['sections'][0].update(paragraphs=[])]:
 bad=copy.deepcopy(doc);mutate(bad);assert list(v.iter_errors(bad))
assert next(s for s in doc['sections'] if s['id']=='gospel')['paragraphs'][1]['text'].startswith('✠')
assert len(next(s for s in doc['sections'] if s['id']=='intercessions')['paragraphs'])==9
print('PASS JSON Schema valid fixture and 3 invalid cases; Gospel heading and 4 petition extraction.')
