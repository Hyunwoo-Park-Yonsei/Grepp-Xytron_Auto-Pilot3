#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################################
# 프로그램명 : hough_drive.py
# 작 성 자 : 자이트론
# 생 성 일 : 2020년 08월 12일
# 수 정 일 : 2021년 03월 16일
# 검 수 인 : 조 이현
# 본 프로그램은 상업 라이센스에 의해 제공되므로 무단 배포 및 상업적 이용을 금합니다.
####################################################################



def u_turn(sensor):
    print("U Turn")
    speed, angle = 0, 10
    current_state = "go"
    if current_state == "go" and sensor[2] < 40:
        current_state = "back"
    elif current_state == "back" and 200 > sensor[2] > 100:
        current_state = "go"
    elif current_state == "go" or current_state == "back" and sensor[2] >= 200:
        current_state = "stop"
    
    
    if current_state == "go":
        speed = 20
        angle = -50
    elif current_state == "back":
        speed = -20
        angle = 50
    else:
        speed = 0
        angle = 0
    return speed, angle
    