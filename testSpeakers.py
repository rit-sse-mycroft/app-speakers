import pygame

pygame.mixer.init()

chan = pygame.mixer.music
chan.load("./test.wav")
chan.play()
input("Enter for next song...")
chan.load("./../test.wav")
chan.play()
input("Enter to quit...")
