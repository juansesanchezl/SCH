import subprocess
import random  
import string  

# INSTALL FFMPEG WINDOWS
# https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/
# https://www.youtube.com/watch?v=W7SIRsIAYao

def random_lower_string(length):
        result = ''.join((random.choice(string.ascii_lowercase) for x in range(length)))
        return result
def getNewPath(path):
    filetype = path.split(".")[-1]
    fullname = path.split("/")[-1]
    new_name = random_lower_string(8) + '.mp4'
    new_path = path.replace(fullname, new_name)
    return new_path

class FFMConvertor:

    def convert_vid_mp4_subprocess(self, input_path):
        try:
            output_path = getNewPath(input_path)
            command = 'ffmpeg -i ' + input_path + ' ' + output_path
            subprocess.run(command)
            print('sucess video new path ' + output_path)
        except:
            print('Some Exception')
    
    def convert_vid_mp4_module(self):
        pass


ffm = FFMConvertor()
'''
inpath = r'videos/video4.mp4'
inpath = r'videos/video4.avi'
inpath = r'videos/video4.m4v'
inpath = r'videos/video4.mkv'
inpath = r'videos/video4.mpg'
inpath = r'videos/video4.flv'
inpath = r'videos/video4.mov'
'''
inpath = r'videos/video4.wmv'
ffm.convert_vid_mp4_subprocess(inpath)