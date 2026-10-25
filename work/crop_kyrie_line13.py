from PIL import Image
im=Image.open('work/music-inputs/score_00.png')
im.crop((600,1620,2500,2030)).save('work/music-inputs/kyrie-row3.png')
im.crop((600,740,2500,1190)).save('work/music-inputs/kyrie-row1.png')
