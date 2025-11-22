import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import requests

pygame.mixer.music.load("song.ogg") #haruta
pygame.mixer.music.play(-1)

level=-2
url = "http://localhost"   
message=""
check=True

directories = [
    "admin",
    "login",
    "uploads",
    "backup",
    "test",
    "images",
    "config",
    "img",
    "downloads",
    "documents",
    "users",
    "members",
    "contact"
]

def draw():
    global level, url
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Website to scan:", center=(400, 130), fontsize=24, color=(25, 200, 255))
        screen.draw.text(url, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        screen.blit("back",(0,0))
        screen.draw.text(message, center=(400, 330), fontsize=24, color=(225, 200, 255))

def scan():
    global message,url
    message+=f"Start Directory-Scan on {url}\n"
    for directory in directories:
        full_url = url + "/"+directory
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                message+=f"[+] Found: {full_url} (Status 200 OK)\n"
            elif response.status_code == 403:
                message+=f"[!] Protected: {full_url} (Status 403 Forbidden)\n"
            else:
                message+=f"[-] Not available: {full_url} (Status {response.status_code})\n"
        except requests.exceptions.RequestException as e:
            message+=f"Error at {full_url}: {e}"

def on_key_down(key, unicode=None):
    global level, url
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        url = ""
    elif key == keys.RETURN and level == 1:
        level = 2
    elif unicode and key != keys.RETURN and level==1:
        url += unicode

def update():
    global level,check
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    if level==2 and check:
        scan()
        check=False
    if level==2 and keyboard.space:
        level=0

pgzrun.go()

