from map import Map

def main(resolution):
    nx = 21
    ny = 12
    w = resolution[0]
    h = resolution[1]
    d = min(w//nx, h//ny)
    map = Map(w, h, d, d)
    map.main_menu()

if __name__ == '__main__':
    #resolution = (1280, 720)
    resolution = (800, 450)
    main( resolution )