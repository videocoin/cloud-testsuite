
import subprocess
import random
import string
import json

def rand():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

def pprint(obj):
    print(json.dumps(obj, indent=4))

def ffmpeg_rtmp(source, destination):
    cmd = ['ffmpeg', '-re', '-i', source, '-c', 'copy', '-f', 'flv', destination]
    if source == 'screen':
        cmd = [
            'ffmpeg', '-re', '-f', 'lavfi',
            '-i', 'testsrc=rate=30',
            '-c:v', 'libx264', '-b:v', '1600k', 
            '-preset', 'ultrafast', '-b', '900k',
            '-c:a', 'libfdk_aac', '-b:a', '128k',
            '-s', '640x480', '-x264opts', 'keyint=60', 
            '-g', '30', '-pix_fmt', 'yuv420p',
            '-f', 'flv', destination]
    
    subprocess.check_output(cmd)