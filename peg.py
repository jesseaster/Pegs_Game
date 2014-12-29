class Node(object):
	"""
	Consists of functionality to find all possible ways for the pegs game to end.

	Arguments:
		data: object that contains the list of where the pegs are on the board.
	"""
	def __init__(self, data):
		self.data = data
		self.children = []

	def add_child(self, data):
		"""
		Add child to the Node

		Arguments:
			data: object that contains the list of where the pegs are on the board.
		"""
		self.children.append(data)

	def print_tree(self, level=1):
		"""
		Print the list of peg locations for each node in the tree.

		Arguments:
			level: if no level given, then level is 1, else level is what is recieved.
				Used for spacing to visualize how deep into the tree the node is.
		"""
		if level == 1:
			print self.data
		if self.children == None:
			print '  ' * level + str(self.data) + ' ' + str(level)
			return
		for c in self.children:
			print '  ' * level +str(c.data) + ' ' + str(level)
			c.print_tree(level + 1)

	def print_winners(self, level=1):
		"""
		Print only nodes that are 14 levels deep. Only one peg is left.

		Arguments:
			level: if no level given, then level is 1, else level is what is recieved.
				Used to keep track how deep into the the the node is.
		"""
		if level == 14:
			print str(self.data) + ' ' + str(level)
			return
		for c in self.children:
			c.print_winners(level + 1)

	def print_leaves(self, level=1):
		"""
		Print all nodes that contain no children.

		Arguments:
			level: if no level given, then level is 1, else level is what is recieved.
				Used to keep track how deep into the the the node is.
		"""
		if len(self.children) == 0:
			print str(self.data) + ' ' + str(level)
			return
		for c in self.children:
			c.print_leaves(level + 1)

	def move_peg(self, hole, jumpee, jumper):
		"""
		Complete a turn by moving the jumper to the hole and removing the jumpee.

		Returns:
			Returns when completed.

		Arguments:
			hole (integer): location of hole with no peg.
			jumpee (integer): location of peg to be jumped.
			jumper (integer): location of peg that jumps the jumpee.
		"""
		self.data[hole] = True
		self.data[jumpee] = False
		self.data[jumper] = False
		return

	def check_valid_move(self, hole, jumpee, jumper):
		"""
		Check that the hole is empty and the jumpee and jumper have pegs.

		Arguments:
			hole (integer): location of hole.
			jumpee (integer): location of peg to be jumped.
			jumper (integer): location of peg that jumps the jumpee.

		Returns:
			Returns True if hole is False and jumpee and jumper are True.
		"""
		if self.data[hole]== False and self.data[jumpee] == True and self.data[jumper] == True:
			return True
		else:
			return False

	def create_child_copy(self):
		"""
		Create a new child node with the same peg locations as the parent.

		Arguments:
			self (Node)
		"""
		p= list(self.data)
		self.add_child(Node(p))

	def attempt_move(self, hole, jumpee, jumper):
		"""
		Attempt to move recieved pegs. If pegs can be moved, create a child
			copy and move the pegs for the child.

		Arguments:
			hole (integer): location of hole.
			jumpee (integer): location of peg to be jumped.
			jumper (integer): location of peg that jumps the jumpee.

		Returns:
			Returns True if the move was made, False if the move could not be made
		"""
		if self.check_valid_move(hole, jumpee, jumper) == True:
			self.create_child_copy()
			self.children[len(self.children)-1].move_peg(hole, jumpee, jumper)
			return True
		else:
			return False

	def attempt_moves(self, hole):
		"""
		Attempt all possible moves that can be made for the recieved hole.

		If a move is made, a child is created representing that move. If multiple
			moves can be made, multiple children are created representing the multiple
			possibilities.

		Arguments:
			hole (integer): location of hole.

		Returns:
			Returns True if one or more moves are made, else returns False.
		"""
		moves_made = False
		for move_num in range(0, len(moves[hole])):
			if self.attempt_move(hole, moves[hole][move_num][0], moves[hole][move_num][1]) == True:
				moves_made = True
		return moves_made

	def attempt_all_moves(self):
		"""
		Attempt all moves for the game.

		Go through each hole on the board and attempt to move all combinations of possible moves.
			If a move is made, a child is created. Make a recursive call. This will run until all
			possible ways for the game to end have been run.

		Returns:
			Returns True if moves are made, else returns False.
		"""
		moves_made = False
		for hole in range(0, len(self.data)):
			if self.attempt_moves(hole) == True:
				moves_made = True
		if moves_made == True:
			for i in self.children:
				i.attempt_all_moves()
		return moves_made

##############################
#
#     Peg hole labels
#           / \
#          / 0 \
#        / 1   2 \
#      / 3   4   5 \
#    / 6   7   8   9 \
#  / 10 11  12  13  14 \
# -----------------------
#
###############################

############# Define valid moves ######################
moves = []
moves.append([[ 1, 3],[ 2, 5]])					#peg 0
moves.append([[ 3, 6],[ 4, 8]])					#peg 1
moves.append([[ 4, 7],[ 5, 9]])					#peg 2
moves.append([[ 1, 0],[ 4, 5],[ 6,10],[ 7,12]])	#peg 3
moves.append([[ 7,11],[ 8,13]])					#peg 4
moves.append([[ 2, 0],[ 4, 3],[ 8,12],[ 9,14]])	#peg 5
moves.append([[ 3, 1],[ 7, 8]])					#peg 6
moves.append([[ 4, 2],[ 8, 9]])					#peg 7
moves.append([[ 4, 1],[ 7, 6]])					#peg 8
moves.append([[ 5, 2],[ 8, 7]])					#peg 9
moves.append([[ 6, 3],[11,12]])					#peg 10
moves.append([[ 7, 4],[12,13]])					#peg 11
moves.append([[ 7, 3],[ 8, 5],[11, 5],[13,14]])	#peg 12
moves.append([[12,11],[ 8, 4]])					#peg 13
moves.append([[ 9, 5],[13,12]])					#peg 14


### create starting peg pattern ###
pegs = []
pegs.append(False)

for i in range(0, 14):
	pegs.append(True)

a = Node(pegs)

# Build the tree diagram
a.attempt_all_moves()

# Print all leaves that end in a win
a.print_winners()
