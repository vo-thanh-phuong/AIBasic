import pygame
from random import randint
import math
from sklearn.cluster import KMeans
import numpy as np  # Import numpy for array checking

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

pygame.init()

screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption("kmeans visualization")

# Set the screen time, as the screen we see on the screen is the blink of many images in the setting time
running = True
clock = pygame.time.Clock()
BACKGROUND = (214,214,214)
BLACK = (0,0,0)
BACKGROUND_PANEL = (249,255,230)
WHITE = (255,255,255)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (147, 153, 35)
PURPLE = (255,0,255)
SKY = (0,255,255)
ORANGE = (255,125,25)
GRAPE = (100,25,125)
GRASS = (55,155,65)

COLORS = [RED,GREEN,BLUE,YELLOW,PURPLE,SKY,ORANGE,GRAPE,GRASS]

# create text render in the orginal way
    # font = pygame.font.SysFont('sans', 40)
    # text_plus = font.render('+', True, WHITE)
# create text render with define function
font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)
def create_text_render(string):
    font = pygame.font.SysFont('sans', 40)
    return font.render(string, True, WHITE)

text_plus = create_text_render("+")
text_minus = create_text_render("-")
text_run = create_text_render("Run")
text_random = create_text_render("Random")
text_algorithm = create_text_render("Algorithm")
text_reset = create_text_render("Reset")

k = 0
error = 0
points = []
clusters = []
labels = np.array([])  # Initialize labels as an empty numpy array

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Draw interface
    # Draw panel
    pygame.draw.rect(screen, BLACK, (50,50,700,500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55,55,690,490))

    # K button +
    pygame.draw.rect(screen, BLACK, (850,50,50,50))
    screen.blit(text_plus, (865,50))
    
    # K button +
    pygame.draw.rect(screen, BLACK, (950,50,50,50))
    screen.blit(text_minus, (970,50))

    # K value
    text_k = font.render("K = "  + str(k), True, BLACK)
    screen.blit(text_k, (1050,50))

    # Run button
    pygame.draw.rect(screen, BLACK, (850,150,150,50))
    screen.blit(text_run, (895,150))

    # Random button
    pygame.draw.rect(screen, BLACK, (850,250,150,50))
    screen.blit(text_random, (865,250))

    # Algorithm
    pygame.draw.rect(screen, BLACK, (850,450,150,50))
    screen.blit(text_algorithm, (855,450))

    # Reset button
    pygame.draw.rect(screen, BLACK, (850,550,150,50))
    screen.blit(text_reset, (880,550))
    
    # Draw mouse position when mouse is in panel
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render("(" + str(mouse_x - 50) + "," + str(mouse_y - 50) + ")", True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))

    # End draw interface

    # Get the coordination of mouse
        
    for event in pygame.event.get(): #event la nhung nut bam, nhu bam chuot, ban phim
        if event.type == pygame.QUIT:
            running = False
        # check when the mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # check the mouse button downs the right place
            # Create point on panel
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = np.array([])  # Clear labels as a numpy array
                point = [mouse_x - 50, mouse_y - 50]
                points.append(point)

            # Change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if k < 8:
                    k += 1
                print("Press K +")
            
            # Change K button -
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if k > 0:
                    k -= 1
                print("Press K -")

            # Run button
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                labels = np.array([])

                if clusters == []:  # if not clusters:
                    continue

                # Assign points to closet clusters
                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        dis = distance(p,c)
                        distances_to_cluster.append(dis)

                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance) # index is use for returning the position of min_distance
                    labels = np.append(labels, label)

                # Update clusters 
                for i in range(k):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1

                    if count != 0:
                        new_cluster_x = sum_x/count
                        new_cluster_y = sum_y/count
                        clusters[i] = [new_cluster_x, new_cluster_y]

                print("run pressed")

            # Random button
            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                labels = np.array([])
                clusters = []
                for i in range(k):
                    random_point = [randint(0,700), randint(0,500)]
                    clusters.append(random_point)
                print("random pressed")

            # Algorithm button
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                try:
                    kmeans = KMeans(n_clusters=k).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                except: 
                    print("error")
                print("algorithm pressed")

            # Reset button
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                k = 0
                error = 0
                points = []
                clusters = []
                labels = np.array([])
                print("reset pressed")

    # Draw point
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0] + 50, points[i][1] + 50), 6)

        if labels.size == 0:
            pygame.draw.circle(screen, WHITE, (points[i][0] + 50, points[i][1] + 50), 5)
        else:
            pygame.draw.circle(screen, COLORS[int(labels[i])], (points[i][0] + 50, points[i][1] + 50), 5)

    # Draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)

    # Calculate and draw error
    error = 0
    if len(clusters) > 0 and labels.size > 0:
        for i in range(len(points)):
            error += distance(points[i], clusters[int(labels[i])])

    text_error = font.render("Error = " + str(int(error)), True, BLACK)
    screen.blit(text_error, (850,350))

    pygame.display.flip() # Due to this code, the codes aboved will be effective

pygame.quit()