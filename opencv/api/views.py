import cv2
import numpy as np
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Imgcaptured
from .serializer import ImgcapturedModelSerializer
from ..utils import get_info
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import subprocess
from django.core.files.uploadedfile import InMemoryUploadedFile
import json
from io import BytesIO
import PIL.Image
import uuid





class VideoCapture:
    def __del__(self):
        self.video.release()

    def get_frame(self):
        self.video = cv2.VideoCapture(0)
        _, frame = self.video.read()
        processed_image = get_info(frame)
        _, jpeg = cv2.imencode('.jpg', processed_image)
        return base64.b64encode(jpeg).decode('utf-8')


video_capture = VideoCapture()

@csrf_exempt
def video_feed1(request):
    return render(request,'index.html')

def run_subprocess1(request):
    try:
        
        result=subprocess.run(['python', 'subprocess/aruco_model.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output_json = result.stdout.strip()
        output_dict = json.loads(output_json)

        #getting the data from json
        result_list = output_dict.get('result_list', [])  
        result_img1=output_dict.get('result_img')
    
        bin_img = base64.b64decode(result_img1)
        image_file = InMemoryUploadedFile(
            file=BytesIO(bin_img),
            field_name='image',  
            name=f"captured_image{uuid.uuid4()}.jpg",  
            content_type='image/jpeg',
            size=len(bin_img),
            charset=None
        )
        

        #saving it in the django db
        my_model = Imgcaptured(image=image_file, height=result_list[0], width=result_list[1], canopy=result_list[2])
        my_model.save()
        
        
        return JsonResponse({'status': 'success', 
                             'message': 'External program executed successfully',
                              'output': result_list
                             }, status=status.HTTP_201_CREATED)
    
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 
                             'message': f'Error: {e}',
                            'output': e.stderr
                            })
        
        
def run_subprocess2(request):
    try:
        
        result=subprocess.run(['python', 'subprocess/refrence_model.py'],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output_json = result.stdout.strip()
        output_dict = json.loads(output_json)

        #getting the data from json
        result_list = output_dict.get('result_list', [])  
        result_img1=output_dict.get('result_img')
    
        bin_img = base64.b64decode(result_img1)
        image_file = InMemoryUploadedFile(
            file=BytesIO(bin_img),
            field_name='image',  
            name=f"captured_image{uuid.uuid4()}.jpg",  
            content_type='image/jpeg',
            size=len(bin_img),
            charset=None
        )
        

        #saving it in the django db
        my_model = Imgcaptured(image=image_file, height=result_list[0], width=result_list[1], canopy=result_list[2])
        my_model.save()
        
        
        return JsonResponse({'status': 'success', 
                             'message': 'External program executed successfully',
                              'output': result_list
                             }, status=status.HTTP_201_CREATED)
    
    except subprocess.CalledProcessError as e:
        return JsonResponse({'status': 'error', 
                             'message': f'Error: {e}',
                            'output': e.stderr
                            })
        
@api_view(['POST'])
def video_feed(request):
    return JsonResponse({'image': video_capture.get_frame()}, status=status.HTTP_201_CREATED)