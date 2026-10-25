import subprocess
for key in ['gloria-a','gloria-b','gloria-c','gloria-d','sanctus','memorial-ordinary','memorial-lent','memorial-easter']:
 subprocess.run(['pdftoppm','-scale-to','1500','-png','-singlefile','output/pdf/'+key+'-reengraved.pdf','work/music-manual/'+key+'-proof'],check=True)
