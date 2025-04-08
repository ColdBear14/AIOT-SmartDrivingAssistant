import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()

import cv2
import numpy as np
import helpers.drowsiness_detection as dd
import time
import winsound
import asyncio
from concurrent.futures import ThreadPoolExecutor

class VideoCam:
    def __init__(self):
        self.eye_idxs = {
            'left': [362, 385, 387, 263, 373, 380],
            'right': [33,  160, 158, 133, 153, 144]
        }
        
        self.facemesh = dd.get_media_pipe()
        
        self.ear_txt_pos = (10,30)
        
        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        
        self.state = {
            "start_time": time.perf_counter(),
            'drowsy_time': 0.0,
            'color': self.GREEN,
            'play_alarm': False
        }
        
        self.show_window = True
        self.running = False

        self.executor = ThreadPoolExecutor(max_workers=1)
        
    @staticmethod
    def plot_text(image, text, origin, color, font=cv2.FONT_HERSHEY_SIMPLEX,scale=0.8,thickness=2):
        return cv2.putText(image,
                           text,
                           origin,
                           font,
                           scale,
                           color,
                           thickness)
         
    def ear_detection(self,frame: np.array,thresholds):
        frame = np.ascontiguousarray(frame)
        frame_h,frame_w,_ = frame.shape
        drowsy_text_pos = (10, int(frame_h // 2 * 1.7))
        results = self.facemesh.process(frame) 
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            
            ear, _ = dd.calculate_avg_ear(
                landmarks,
                self.eye_idxs['left'],
                self.eye_idxs['right'],
                frame_w,
                frame_h
            )
            
            if ear < thresholds['ear_threshold']:
                end_time = time.perf_counter()
                
                self.state['drowsy_time'] += end_time - self.state['start_time']
                self.state['start_time'] = end_time
                self.state['color'] = self.RED

                if self.state['drowsy_time'] >= thresholds['wait_time']:
                    ... 
                    #TODO: implement alarm mechanic
                    self.state['play_alarm'] = True
                    winsound.Beep(1000, 500)
                    
                    
            else:
                self.state['start_time'] = time.perf_counter()
                self.state['drowsy_time'] = 0.0
                self.state['color'] = self.GREEN
                
            ear_text = f"EAR: {ear:.2f}"
            drowsy_text = f"Drowsy: {self.state['drowsy_time']:.2f}s"
            
            VideoCam.plot_text(frame,ear_text,self.ear_txt_pos,self.state['color'])
            VideoCam.plot_text(frame,drowsy_text,drowsy_text_pos,self.state['color'])
            
        else: 
            frame = cv2.flip(frame,1)
        
        return frame, self.state['play_alarm']
    
    async def start_webcam(self,thresholds:dict,mirror= False):
        self.running = True
        self.show_window = thresholds.get('show_window', True)
        loop = asyncio.get_event_loop()
        self.future = self.executor.submit(
            self._webcam_loop, thresholds, mirror
        )    
    
        
        
    def _webcam_loop(self,thresholds:dict,mirror= False):
        print("Webcam loop started.")
        cam = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cam.read()
            if not ret:
                break
            if mirror:
                frame = cv2.flip(frame,1)
            
            rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            processed_frame, play_alarm = self.ear_detection(rgb_frame,thresholds)
            
            if self.show_window:
                cv2.imshow('Driver Monitor',processed_frame[:,:,::-1])
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # print("Frame processed.")    
            time.sleep(0.01)
            
        cam.release()
        cv2.destroyAllWindows()
    
    def stop(self):
        self.running = False
        
        if hasattr(self, 'future'):
            self.future.result()
        print("Webcam stopped.")
        
        
    def update_show_window(self,show):
        self.show_window = show
    
    async def main(self):
        print("Main function started.")
        thresholds = {
            'ear_threshold' : 0.25,
            'wait_time': 5.0,
            'show_window': True
        }
        await self.start_webcam(thresholds)
        print("Webcam started.")
        await asyncio.sleep(10)
        self.stop()
        print("Main function finished.")  
            
if __name__ == '__main__':
    
    asyncio.run(VideoCam().main())
    
            
            
                
                
            
            