import pygame
import random
import math
pygame.init()

class DrawInformation:
	#pixel range from 0 to 255 and the three colors we are modifying in each are RGB
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

    #colors of the three greyish bars 
	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 20)
	LARGE_FONT = pygame.font.SysFont('comicsans', 40)

	SIDE_PAD = 100 #padding from the left and right so as to leave that many pixels to keep graph in center,50 on left and right
	TOP_PAD = 150 #this is to accomodate any text on top 

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))  #this is how we define a windown in pygame
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

    #this fn is used to dynamically modify the width and ht of the bars based on the range we have
	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2 #// means integer divide


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR) #we fill the window with the background colour to overwrite any previous drawings and start again

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK) #1 is the anti aliasing to make the lines sharp
	#blit is used to copy a image/text from one surface to another,also we want to center the x cood here therefore we do (window width/2)-(text width by 2) to get in center, for y we just do  45 pixels from the top as random
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 55))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | M - Merge Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 85))

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

    #when we want to clear a rect we dont clear the entire window as the text is static which doesnt change which will not be optimal, therefore we just want to overwrite the rectangle being sorted
	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst): #enumerate will give index as well as value in our list
		x = draw_info.start_x + i * draw_info.block_width
		#the y cood is a bit complicated, see from 28:50
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height)) # the height we can just enter as ht of the screen as we have already determined our starting pt on the top so no matter how far down we go, it will only go as much as our screen and below it won't show so it doesn't matter

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val) 
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True #this is used to pause the execution temporarily, store the state it is at and continue execution after a while,
				#without this we wont be able to press any other buttons while it is executing as the sorting fn has complete control
                #the yield keyword is used in generators,see vid on that

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

def selection_sort(draw_info, ascending=True):
		lst=draw_info.lst

		if ascending:
			for i in range(len(lst)):
				min_idx = i
				for j in range(i+1, len(lst)):
					if lst[min_idx] > lst[j]:
						min_idx = j
				num1=lst[i]
				num2=lst[min_idx]
				lst[i], lst[min_idx] = lst[min_idx], lst[i]
				draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
				yield True
		else:
			for i in range(len(lst)):
				max_idx = i
				for j in range(i+1, len(lst)):
					if lst[max_idx] < lst[j]:
						max_idx = j
				num1=lst[i]
				num2=lst[max_idx]
				lst[i], lst[max_idx] = lst[max_idx], lst[i]
				draw_list(draw_info, {i: draw_info.GREEN, max_idx: draw_info.RED}, True)
				yield True

		return lst

def merge_sort(draw_info, ascending = True):
    lst = draw_info.lst
    width = 1
    n = len(lst)
    while (width < n):
        l=0
        
        while (l < n):
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1) 
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            merge(lst, l, m, r, ascending)
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            draw_list(draw_info, {l : draw_info.RED, r : draw_info.GREEN}, True)
            yield True
            l += width * 2
        width *= 2
        
    return lst

#MERGE Function is also a part of MERGE SORT
def merge(lst, l, m, r, ascending = True):
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    
    for i in range(0, n1):
        L[i] = lst[l + i]
        
    for i in range(0, n2):
        R[i] = lst[m + i + 1]
        
    i, j, k = 0, 0, l
    
    if ascending:
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1
    
        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1
    
        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1
    else:
        while i < n1 and j < n2:
            if L[i] >= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1
    
        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1
    
        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1
	    

def main():
	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(60) #60 is basically fps,how many times the loop can run per second

		if sorting:
			try:
				next(sorting_algorithm_generator) #basically call the next item in the generator till it gets exhausted
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue
            
            #if we press r we want to reset the list
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			#space to start sorting
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting: #a for ascending and d for descending
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm = merge_sort
				sorting_algo_name = "Merge Sort"


	pygame.quit()

# to ensure that we are running this module directly by clicking run 
if __name__ == "__main__":
	main()