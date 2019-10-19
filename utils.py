
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
            'ffmpeg',
            '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
            '-f', 'avfoundation', '-pix_fmt', 'uyvy422', '-i', 'Capture screen 0',
            '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', 
            '-preset', 'medium', '-r', '30', '-g', '30', '-b:v', '2500k',
            '-acodec', 'libmp3lame', '-ar', '44100', '-threads', '6', '-b:a', '712000', '-bufsize', '512k',
            '-f', 'flv', destination]
    
    subprocess.check_output(cmd)