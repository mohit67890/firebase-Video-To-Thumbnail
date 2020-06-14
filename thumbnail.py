import os
from google.cloud import storage
from subprocess import check_output
from videoprops import get_video_properties

client = storage.Client()

# STARTfunction on videdo uploaded to cloud storage
def convert_video_thumbnail(data, context):
  
  print(data)

  if data['contentType'].startswith('video/'):

     bucket = client.get_bucket(data['bucket'])
     name = data['name']

     file_name = '/tmp/' + name
     print(file_name)

     thumbnail_file_name = '/tmp/' + name.split('.')[0] + '.png'
     print(thumbnail_file_name)

     try:
          os.remove(file_name)
     except OSError:
          pass

     try:
          os.remove(thumbnail_file_name)
     except OSError:
          pass

     print("File has been removed")

     # Downloading the video to the cloud functions
     blob = bucket.get_blob(name)
     blob.download_to_filename(file_name)

     print("Video Downloaded")

     props = get_video_properties(file_name)

     

     if os.path.exists(file_name):
          print("NEW MP4 EXISTS")            
          check_output('ffmpeg  -itsoffset -4  -i '+file_name+' -vcodec mjpeg -vframes 1 -an -f rawvideo -s '+str(props['width'])+'x'+str(props['height'])+' '+thumbnail_file_name, shell=True)
          thumbnail_blob = bucket.blob(name.split('.')[0] + '.png')
          thumbnail_blob.upload_from_filename(thumbnail_file_name)
     else:
          print("MP4 not created")

     
     print("uploaded")

  else :
     print("Not a Video")
