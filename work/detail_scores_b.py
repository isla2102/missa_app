from PIL import Image
im=Image.open('work/music-inputs/score_07.png');im.crop((500,650,2650,1700)).resize((2150,1050)).save('work/music-inputs/detail_07b.png')
