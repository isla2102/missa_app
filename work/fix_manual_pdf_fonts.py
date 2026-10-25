from pathlib import Path
p=Path('work/engrave_manual_scores.py');s=p.read_text(encoding='utf-8').replace('from reportlab.graphics import renderPDF','from reportlab.graphics import renderPDF\nfrom reportlab.graphics.shapes import String')
s=s.replace("drawing=svg2rlg(io.BytesIO(svg.encode('utf-8')));W=", "drawing=svg2rlg(io.BytesIO(svg.encode('utf-8')))\n def korean_fonts(node):\n  if isinstance(node,String):node.fontName='Malgun'\n  for child in getattr(node,'contents',[]):korean_fonts(child)\n korean_fonts(drawing)\n W=")
p.write_text(s,encoding='utf-8',newline='\r\n')
