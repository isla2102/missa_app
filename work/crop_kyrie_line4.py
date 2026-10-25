from PIL import Image
im=Image.open('work/music-inputs/score_00.png')
im.crop((600,2050,2500,2480)).save('work/music-inputs/kyrie-row4.png')
