from map import Map

def main(resolution = (1440, 810)):
    nx = 32
    ny = 18
    w = resolution[0]
    h = resolution[1]
    d = min(w//nx, h//ny)
    map = Map(w, h, d, d)
    map.main_menu()

if __name__ == '__main__':
    main( (1280, 720) )