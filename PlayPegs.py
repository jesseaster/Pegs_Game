from Tkinter import *
import tkMessageBox
import Tkinter
import math
import peg

def click(event):
	"""
	Get click location. Then determine the closest pin.

	Arguments:
		event: an event is triggered by the user.
	"""
	canvas = event.widget.canvas
	arrow = canvas.data["arrow"]
	global jumper
	x_click = event.x
	y_click = event.y
	jumper = peg_click(canvas, x_click, y_click)

def release(event):
	"""
	Get click release location. Then get the peg number closest
		to the release click. If the clicked peg and released peg
		is a valid move, move the pegs. Then determine if winning
		is still possible.

	Arguments:
		event: an event is triggered by the user.
	"""
	canvas = event.widget.canvas
	peg_node = canvas.data["peg_node"]
	move = canvas.data["move"]
	x_release = event.x
	y_release = event.y
	hole = peg_click(canvas, x_release, y_release)
	if move.check_clicked_move(peg_node, hole, jumper) == True:
		jumpee = move.get_jumpee(peg_node, hole, jumper)
		move_pegs(canvas, hole, jumpee, jumper)
		draw_arrow(canvas, hole, jumper)
		if win_possible(canvas) == True:
			print "you made a wise move"
		else:
			print "you goofed"

def peg_click(canvas, x, y):
	"""
	Determine which peg the user clicked.

	Arguments:
		canvas: object that contains the
	"""
	peg_xy = canvas.data["peg_xy"]
	click_radius = canvas.data["click_radius"]
	found = -1
	for i in range(0,15):
		length = math.sqrt(math.pow(peg_xy[i][0]-x, 2) + math.pow(peg_xy[i][1]-y, 2))
		if length <= click_radius:
			found = i
			break
	return found

def win_possible(canvas):
	"""
	Determine if the game can still be won.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	peg_node = canvas.data["peg_node"]
	return peg_node.is_win_possible()

def draw_arrow(canvas, hole, jumper):
	"""
	Draw an arrow showing which move was made last.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
		hole: location of the hole the jumper will jump to.
		jumper: the peg that will jump the jumpee and end up in the hole.
	"""
	arrow = canvas.data["arrow"]
	peg_xy = canvas.data["peg_xy"]
	if hole != -1 and jumper != -1:
		canvas.delete(arrow)
		arrow = canvas.create_line(peg_xy[hole][0], peg_xy[hole][1], peg_xy[jumper][0], peg_xy[jumper][1], width=3, fill="red", arrow="first")
		canvas.data["arrow"] = arrow

def _create_circle(self, x, y, r, **kwargs):
	"""
	Draw a circle.

	Arguments:
		x: x coordinate.
		y: y coordinate.
		r: radius.
		kwargs:
	"""
	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle

def printInstructions():
	"""
	Print instructions.

	Arguments:
		none.
	"""
	print "Pegs!"
	print "click and drag to move pegs"

def load_peg_locations(canvas):
	"""
	Create locations for pegs.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	triangle_side_length = canvas.data["triangle_side_length"]
	triangle_y_length = canvas.data["triangle_y_length"]
	middle_x = canvas.data["middle_x"]
	padding = canvas.data["padding"]
	peg_xy_generate = []
	peg_xy = []
	for i in [-4,-3,-2,-1,0]:
		for j in range(0, -i+1):
			x = triangle_side_length/12*i + middle_x + triangle_side_length/6*j
			y = (triangle_y_length/6)*(i*-1+4.0/3) + padding
			peg_xy_generate.append([x, y])
	peg_xy.append(peg_xy_generate[14])
	peg_xy.append(peg_xy_generate[12])
	peg_xy.append(peg_xy_generate[13])
	peg_xy.append(peg_xy_generate[9])
	peg_xy.append(peg_xy_generate[10])
	peg_xy.append(peg_xy_generate[11])
	peg_xy.append(peg_xy_generate[5])
	peg_xy.append(peg_xy_generate[6])
	peg_xy.append(peg_xy_generate[7])
	peg_xy.append(peg_xy_generate[8])
	peg_xy.append(peg_xy_generate[0])
	peg_xy.append(peg_xy_generate[1])
	peg_xy.append(peg_xy_generate[2])
	peg_xy.append(peg_xy_generate[3])
	peg_xy.append(peg_xy_generate[4])
	canvas.data["peg_xy"] = peg_xy

def load_starting_peg_pattern(canvas):
	"""
	Create starting peg pattern.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	pegs = []
	pegs.append(False)
	for i in range(0, 14):
		pegs.append(True)
	peg_node = peg.Node(pegs)
	move = peg.move()
	canvas.data["peg_node"] = peg_node
	canvas.data["move"] = move

def load_arrow(canvas):
	"""
	Load the arrow.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	arrow = canvas.create_line(0,0,1,0)
	canvas.data["arrow"] = arrow

def load_triangle(canvas):
	"""
	Load the triangle.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	box = canvas.data["box"]
	padding = canvas.data["padding"]
	triangle_bottom_y_coord = canvas.data["triangle_bottom_y_coord"]
	tri_coord0 = box/2, padding
	tri_coord1 = padding, triangle_bottom_y_coord
	tri_coord2 = box-padding, triangle_bottom_y_coord
	tri_coords = tri_coord0, tri_coord1, tri_coord2
	triangle = canvas.create_polygon(tri_coords, fill="yellow")

def move_pegs(canvas, hole, jumpee, jumper):
	"""
	Move the pegs.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
		hole: location of the hole the jumper will jump to.
		jumpee: the peg that gets jumped and removed.
		jumper: the peg that will jump the jumpee and end up in the hole.
	"""
	old_peg_node = canvas.data["peg_node"]
	old_peg_node.create_child_copy()
	peg_node = old_peg_node.children[-1]
	peg_node.move_peg(hole, jumpee, jumper)
	canvas.data["peg_node"] = peg_node
	canvas.data["old_peg_node"] = old_peg_node
	redraw_pegs(canvas)

def redraw_pegs(canvas):
	"""
	Redraw the pegs.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	peg_node = canvas.data["peg_node"]
	peg_xy = canvas.data["peg_xy"]
	peg_radius = canvas.data["peg_radius"]
	peg_gui = canvas.data["peg_gui"]
	hole_radius = canvas.data["hole_radius"]
	for i in range(0,15):
		canvas.delete(peg_gui[i])
	peg_gui = []
	for i in range(0,15):
		if peg_node.data[i] == True:
			peg_gui.append(canvas.create_circle(peg_xy[i][0],peg_xy[i][1], peg_radius, fill="orange"))
		else:
			peg_gui.append(canvas.create_circle(peg_xy[i][0],peg_xy[i][1], hole_radius, fill="black"))
	canvas.data["peg_gui"] = peg_gui

def load_pegs(canvas):
	"""
	Load the pegs.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	peg_node = canvas.data["peg_node"]
	peg_xy = canvas.data["peg_xy"]
	peg_radius = canvas.data["peg_radius"]
	hole_radius = canvas.data["hole_radius"]
	peg_gui = []
	for i in range(0,15):
		if peg_node.data[i] == True:
			peg_gui.append(canvas.create_circle(peg_xy[i][0],peg_xy[i][1], peg_radius, fill="orange"))
		else:
			peg_gui.append(canvas.create_circle(peg_xy[i][0],peg_xy[i][1], hole_radius, fill="black"))
	canvas.data["peg_gui"] = peg_gui

def load_peg_board(canvas):
	"""
	Load the peg board.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	load_peg_locations(canvas)
	load_starting_peg_pattern(canvas)
	load_arrow(canvas)
	load_triangle(canvas)
	load_pegs(canvas)

def init(canvas):
	"""
	Initialize the canvas.

	Arguments:
		canvas: widget that draws the canvas and used to store data.
	"""
	printInstructions()
	load_peg_board(canvas)
	canvas.data["isGameOver"] = False

def run():
	"""
	Run the program.

	Arguments:
		none.
	"""
	root = Tk()
	box = 800
	padding = 10
	triangle_side_length = box-padding*2
	hole_radius = triangle_side_length/80
	click_radius = triangle_side_length/13
	peg_radius = triangle_side_length*3/80
	triangle_y_length = math.sin(math.pi/3) * triangle_side_length
	triangle_bottom_y_coord = triangle_y_length + padding
	middle_x = box/2
	canvas = Canvas(root, bg="white", height=box, width=box)
	canvas.pack()
	root.resizable(width=0, height=0)
	# Store canvas in root and in canvas itself for callbacks
	root.canvas = canvas.canvas = canvas
	# Set up canvas data and call init
	canvas.data = { }
	canvas.data["box"] = box
	canvas.data["padding"] = padding
	canvas.data["triangle_side_length"] = triangle_side_length
	canvas.data["hole_radius"] = hole_radius
	canvas.data["click_radius"] = click_radius
	canvas.data["peg_radius"] = peg_radius
	canvas.data["triangle_y_length"] = triangle_y_length
	canvas.data["triangle_bottom_y_coord"] = triangle_bottom_y_coord
	canvas.data["middle_x"] = middle_x
	init(canvas)
	# set up events
	canvas.bind("<ButtonPress-1>", click)
	canvas.bind("<ButtonRelease-1>", release)
	root.mainloop()

run()
