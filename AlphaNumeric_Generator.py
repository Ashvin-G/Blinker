import cv2
import numpy as np
import dlib
import matplotlib.pyplot as plt
import math
import time

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

cap = cv2.VideoCapture(0)
morse = cv2.imread('morse.jpg')
morse = cv2.resize(morse, (640, 480))

status_list = []
code = []
string = ""

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}

def decrypt(message):
        message += ' '
        decipher = ''
        citext = ''
        for letter in message:
                try:
                        if(letter != ' '):
                                i=0
                                citext += letter
                        else:
                                i += 1
                                if i == 2:
                                        decipher += ' '
                                else:
                                        decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                                        citext = ''
                except ValueError:
                        decipher = 'Code does not math International Standard of Morse Code'
        return decipher
	

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    morse_frame = np.hstack((morse, frame))
    gray_morse_frame = cv2.cvtColor(morse_frame, cv2.COLOR_BGR2GRAY)

        

    faces = detector(gray_morse_frame)

    for face in faces:
        landmarks = predictor(gray_morse_frame, face)
        
        #Left Eye

        left_eye_landmarks_points = []

        for i in range(36, 42):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            
            left_eye_landmarks_points.append((x, y))
        left_points = np.array(left_eye_landmarks_points, np.int32)
        cv2.polylines(morse_frame, [left_points], True, (0, 255, 0), 1)
        
        x_36 = landmarks.part(36).x
        y_36 = landmarks.part(36).y

        x_39 = landmarks.part(39).x
        y_39 = landmarks.part(39).y

        len_hor_left_eye = math.sqrt((x_39 - x_36)**2 + (y_39 - y_36)**2)
        
        x_37 = landmarks.part(37).x
        y_37 = landmarks.part(37).y

        x_38 = landmarks.part(38).x
        y_38 = landmarks.part(38).y

        mid_x_37_38 = int((x_37 + x_38)/2)
        mid_y_37_38 = int((y_37 + y_38)/2)
        
        x_41 = landmarks.part(41).x
        y_41 = landmarks.part(41).y

        x_40 = landmarks.part(40).x
        y_40 = landmarks.part(40).y

        mid_x_40_41 = int((x_40 + x_41)/2)
        mid_y_40_41 = int((y_40 + y_41)/2)

        len_ver_left_eye = math.sqrt((mid_x_40_41 - mid_x_37_38)**2 + (mid_y_40_41 - mid_y_37_38)**2)
        

        left_eye_ratio = len_hor_left_eye/len_ver_left_eye

        #Right Eye
        right_eye_landmarks_points = []
        for i in range(42, 48):
            x = landmarks.part(i).x
            y = landmarks.part(i).y

            right_eye_landmarks_points.append((x, y))
        right_points = np.array(right_eye_landmarks_points, np.int32)
        cv2.polylines(morse_frame, [right_points], True, (0, 255, 0), 1)
        
        
        x_42 = landmarks.part(42).x
        y_42 = landmarks.part(42).y

        x_45 = landmarks.part(45).x
        y_45 = landmarks.part(45).y

        len_hor_right_eye = math.sqrt((x_42 - x_45)**2 + (y_42 - y_45)**2)
        
        x_43 = landmarks.part(43).x
        y_43 = landmarks.part(43).y

        x_44 = landmarks.part(44).x
        y_44 = landmarks.part(44).y

        mid_x_43_44 = int((x_43 + x_44)/2)
        mid_y_43_44 = int((y_43 + y_44)/2)
        
        x_46 = landmarks.part(46).x
        y_46 = landmarks.part(46).y

        x_47 = landmarks.part(47).x
        y_47 = landmarks.part(47).y

        mid_x_46_47 = int((x_46 + x_47)/2)
        mid_y_46_47 = int((y_46 + y_47)/2)

        len_ver_right_eye = math.sqrt((mid_x_43_44 - mid_x_46_47)**2 + (mid_y_43_44 - mid_y_46_47)**2)
        right_eye_ratio = len_hor_right_eye/len_ver_right_eye
        eye_ratio = (right_eye_ratio + left_eye_ratio)/2

        status = 0
        if eye_ratio >= 4.5:
            status = 1
            cv2.putText(morse_frame, 'Blink', (715, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        status_list.append(status)
        
    
            
    cv2.imshow('Morse', morse_frame)
    #cv2.imshow('Frame', frame)
    if cv2.waitKey(1) == 27:
        break

t=0
sum_1 = 0



while t<len(status_list):
    if status_list[t] == 0:
        t = t+1
        if sum_1 > 15:
            code.append(" -....- ")
            string = string + " -....- "
        elif sum_1 > 5 and sum_1 < 15:
            code.append("-")
            string = string + "-"
        elif sum_1 <=5 and sum_1 >= 1:
            code.append(".")
            string = string + "."
        else:
            pass
        sum_1 = 0

    else:
        while status_list[t] == 1:
            t = t+1;
            sum_1 = sum_1 + 1
            if(t>=len(status_list)):
                if sum_1 > 15:
                    code.append("-....-")
                    string = string + "-....-"
                elif sum_1 > 5 and sum_1 < 15:
                    code.append("-")
                    string = string + "-"
                elif sum_1 <= 5 and sum_1 >= 1:
                    code.append(".")
                    string = string + "."
                else:
                    pass
                break

print(string)
result = decrypt(string) 

text = result

t = []
q = []

string = ''

for p in range(len(text)):
    t.append(text[p])

for q in range(len(t)):
    try:
        if (t[q] == '-' and t[q+1] !='-'):
            t[q] = t[q+1]
            t[q+1] = '_'
            q = q + 1
    except IndexError:
        pass

for r in range(len(t)):
    if t[r] != '_':
        string = string + t[r]
print(string)





cap.release()
cv2.destroyAllWindows()
