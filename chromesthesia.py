import pygame, random

import math
import pyaudio

# class WindowSuperObject(object):
#     pass

# def load_and_initialize_func():
#     """ """
#     chromesthesia = WindowSuperObject()
#     chromesthesia.screen = pygame.display.set_mode((800,600))
#     chromesthesia.quit_icon = pygame.image.load('art_assets/png_output/quit_icon.png')

#     chromesthesia.draw_on = False
#     chromesthesia.last_pos = (0, 0)
#     chromesthesia.color = (255, 128, 0)
#     chromesthesia.radius = 10


#     return chromesthesia

    


def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.display.update(pygame.draw.circle(srf, color, (x, y), radius))

def mouse_button_down_func():
    """ """
    pass

def find_piano_key_freq_given_pixel_position(y_pos):
    """ """
    #easier than math
    # root_twelve_of_two = 1.0594630943592952645618252949463417007792043174941856  
    inverse_pos = math.fabs(y_pos*1.0 - 600.0)   
    piano_key = inverse_pos / 6.8
    n_exponent = (piano_key - 49.0) / 12.0



    freq = math.pow(2,n_exponent) * 440.0

    return freq

def make_the_music(p,freq=261.63):
    """ """


    #sudo apt-get install python-pyaudio
    

    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 44000 #number of frames per second/frameset.      

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    # FREQUENCY = 261.63 #Hz, waves per second, 261.63=C4-note.
    # LENGTH = 1.2232 #seconds to play sound
    LENGTH = 1.0 / 10.0
    # print freq
    FREQUENCY = freq

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''    

    for x in xrange(NUMBEROFFRAMES):
        WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    

    #fill remainder of frameset with silence
    for x in xrange(RESTFRAMES): 
        WAVEDATA = WAVEDATA+chr(128)

    
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)
    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()

def play_freq_list(p,play_list):
    """ """
    BITRATE = 16000 #number of frames per second/frameset.      

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    # FREQUENCY = 261.63 #Hz, waves per second, 261.63=C4-note.
    # LENGTH = 1.2232 #seconds to play sound
    LENGTH = 2.0 / 600.0
    # print freq


    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)

    big_wave_data = ""
    for freq in play_list:
        FREQUENCY = freq

        NUMBEROFFRAMES = int(BITRATE * LENGTH)
        RESTFRAMES = NUMBEROFFRAMES % BITRATE
        WAVEDATA = ''    

        for x in xrange(NUMBEROFFRAMES):
            WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    

        #fill remainder of frameset with silence
        # for x in xrange(RESTFRAMES): 
        #     WAVEDATA = WAVEDATA+chr(128)

        big_wave_data += WAVEDATA


    stream.write(big_wave_data)


    stream.stop_stream()
    stream.close()


def loop_and_update_forever():
    """ """
    screen = pygame.display.set_mode((800,600))
    quit_icon = pygame.image.load('art_assets/png_output/quit_icon.png')

    draw_on = False
    last_pos = (0, 0)
    color = (255, 128, 0)
    radius = 1

    do_once = True
    # temp_array = []

    PyAudio = pyaudio.PyAudio
    p = PyAudio()

    # roundline(screen, (1,1,1), (1,1), (799,1),  radius)

    try:
        while True:
            e = pygame.event.wait()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    raise StopIteration
                if e.key == pygame.K_c:
                    screen.fill( (0,0,0) )
                    pygame.display.flip()

                if e.key == pygame.K_m:
                    if the_first_click:
                        # x,y = the_first_click
                        the_whole_list = []
                        last_list = []
                        another_big_list = []
                        for x_pos in xrange(1,800,5):
                            y_list = []
                            play_list = []
                            last = None
                            freq = last_freq = None
                            for y_pos in xrange(1,600):

                                pixel = screen.get_at((x_pos, y_pos))
                                if pixel[0] > 0:
                                    # y_list.append(y_pos)
                                    if not last:
                                        freq = find_piano_key_freq_given_pixel_position(y_pos) 
                                    elif (last == y_pos):
                                        pass # y_list.remove(last)
                                    else:
                                        freq = find_piano_key_freq_given_pixel_position(last) 
                                        # print freq  
                                        # make_the_music(p,freq)

                                    if (last_freq and last_freq != freq):
                                        play_list.append(freq)  
                                        another_big_list.append(freq)   

                                    last_freq = freq
                                    last = y_pos

                            if play_list != []:
                                print play_list 
                                last_list = play_list 
                            else:
                                for freq in last_list:
                                    another_big_list.append(freq)          
                                # play_freq_list(p,play_list)

                            # the_whole_list.append((x_pos,play_list))

                        # play_the_whole_damn_list(p, the_whole_list)
                        play_freq_list(p,another_big_list)


                                # make_the_music(p,play_list[0])

                            # last = None
                            # for y_pos in y_list:
                            #     if not last:
                            #         last = y_pos
                            #     elif (last < y_pos+2 and last > y_pos-2):
                            #         y_list.remove(last)
                            #         last = y_pos
                            #     else:
                            #         freq = find_piano_key_freq_given_pixel_position(last)   
                            #         make_the_music(p,freq)



                        # print y_list

                        # freq = find_piano_key_freq_given_pixel_position(y)
                        # make_the_music(p,freq)
                # if event.key == pygame.K_Q:
                #     location += 1

            if e.type == pygame.QUIT:
                raise StopIteration
            if e.type == pygame.MOUSEBUTTONDOWN:
                if do_once:
                    do_once=False
                    the_first_click = e.pos
                    print e.pos

                color = (random.randrange(256), random.randrange(256), random.randrange(256))
                # color = (155,99,12) #organge lol
                pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                draw_on = False
            if e.type == pygame.MOUSEMOTION:
                if draw_on:
                    pygame.display.update(pygame.draw.circle(screen, color, e.pos, radius))
                    roundline(screen, color, e.pos, last_pos,  radius)
                last_pos = e.pos
            #pygame.display.flip()

    except StopIteration:
        pass

    p.terminate()



def main():
    """ business logic for when running this module as the primary one!"""
    
    # load_and_initialize_func()

    loop_and_update_forever()

    pygame.quit()





# Here's our payoff idiom!
if __name__ == '__main__':
    main()
