
from picamera import PiCamera
from uploader import upload_to_s3
from uploader import retreive_results
import time
import os
import threading
from subprocess import call 


camera = PiCamera()
camera.resolution = (1280,720)
camera.exposure_mode = 'antishake'
camera.contrast = 10

file_path = "/home/pi/Videos/"

def convert_video(filename):
    
    mp4_filename = filename.split('.')[0]+'.mp4'
    command = "MP4Box -add "+file_path+'/'+filename+" "+file_path+'/'+mp4_filename
    call([command], shell=True)
    os.remove(file_path+'/'+filename)
    return mp4_filename

def detect_motion(file_name,h264_path):
    
    start_time = time.time()
    time.sleep(1)
    response = retreive_results(file_name)
    latency = (time.time()-start_time)
    print("Latency: ",latency,file_name)
    for j in range(len(response)):
        print(response[j])
    
            
if __name__=='__main__':
    
    i = 1
    startTime = time.time()
    endTime = startTime+300
    while(time.time()<endTime):
        file_name = "recording_"+str(i)+'.h264'
        path = file_path+file_name
        camera.start_recording(path)
        camera.wait_recording(0.5)
        camera.stop_recording() 
        upload_to_s3(path) 
        mythread = threading.Thread(target=detect_motion,args=(file_name,path,))
        mythread.daemon = True
        mythread.start()
        i = i+1
    
