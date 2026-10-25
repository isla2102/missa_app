from PIL import Image
im=Image.open('work/music-inputs/score_00.png')
im.crop((600,1180,2500,1650)).save('work/music-inputs/kyrie-row2.png')
