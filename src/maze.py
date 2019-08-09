# python packages
import random
# internal packages
from block import *

class Maze():
	def __init__(self, length, height):
		self.length = length
		self.height = height
		self.maze = [None] * length * height
		# set up the maze
		self.generate_maze()

	def __repr__(self):
		# the padding helps analyze corners and boundaries.
		padded_length = self.length + 2
		padded_height = self.height + 2
		padded_maze = [None] * padded_length * padded_height

		# graphics are ultimately what we are aiming to find.
		graphic_length = self.length + 1
		graphic_height = self.height + 1
		graphic_maze = [None] * graphic_length * graphic_height
		
		# this thing preps for calculations with graphics.
		for location, reference in enumerate(padded_maze):
			# determine row and column
			row = location // (padded_length)
			column = location % (padded_length)

			# checks if the item is padding for the boundary.
			if (row == 0
			or column == 0
			or row == padded_height - 1
			or column == padded_length - 1):
				pass
			else:
				reference = location - padded_length + 1 - row * 2
				padded_maze[location] = reference

		# this thing calculates the graphics.
		for location, reference in enumerate(graphic_maze):
			# determine row and column
			row = location // (graphic_length)
			column = location % (graphic_length)
			location = location + row

			# determines locations of items in the padded_maze.
			nw_loc = padded_maze[location]
			ne_loc = padded_maze[location + 1]
			sw_loc = padded_maze[location + padded_length]
			se_loc = padded_maze[location + padded_length + 1]

			# initialize hallway passageways.
			# if there is a passway, then its true, else false.
			# none indicates an undeterminate value.
			n_hall = None
			s_hall = None
			e_hall = None
			w_hall = None

			# north boundary
			if (nw_loc is None
			and ne_loc is None):
				n_hall = True
			# south boundary
			if (sw_loc is None
			and se_loc is None):
				s_hall = True
			# east boundary
			if (ne_loc is None
			and se_loc is None):
				e_hall = True
			# west boundary
			if (nw_loc is None
			and sw_loc is None):
				w_hall = True

			if ne_loc and nw_loc and n_hall is None:
				east = self.maze[ne_loc]
				west = self.maze[nw_loc]
				# print(east, east.neighbors['west'])
				# print(west.neighbors['east'], west)
				if (east.neighbors['west'] == west
				and west.neighbors['east'] == east):
					# print("NORTH")
					n_hall = True

			if se_loc and sw_loc and s_hall is None:
				east = self.maze[se_loc]
				west = self.maze[sw_loc]
				print(east, east.neighbors['west'])
				print(west.neighbors['east'], west)
				if (east.neighbors['west'] == west
				and west.neighbors['east'] == east):
					print("SOUTH")
					s_hall = True


			if ne_loc and se_loc and e_hall is None:
				north = self.maze[ne_loc]
				south = self.maze[se_loc]
				if (north.neighbors['south'] == south
				and south.neighbors['north'] == north):
					# print("EAST")
					e_hall = True

			if nw_loc and sw_loc and w_hall is None:
				north = self.maze[nw_loc]
				south = self.maze[sw_loc]
				if (north.neighbors['south'] == south
				and south.neighbors['north'] == north):
					# print("WEST")
					w_hall = True

			# print(
			# 	'---\n'
			# 	f'nw_loc {nw_loc}\n'
			# 	f'ne_loc {ne_loc}\n'
			# 	f'sw_loc {sw_loc}\n'
			# 	f'se_loc {se_loc}\n\n'
			# 	f'n_hall {n_hall}\n'
			# 	f's_hall {s_hall}\n'
			# 	f'e_hall {e_hall}\n'
			# 	f'w_hall {w_hall}\n'
			# )


		return 'WiP'

		'''
			glyph = get_glyph(north, south, east, west)
			if location % string_length == 0:
				amaze += '\n'
			amaze += glyph
			# print(amaze)
		'''



	def get_block(self, row, column):
		'''
		returns the cell located at given coordinates.
		'''
		location = row * self.height + column
		block = self.maze[location]
		return block

	def get_row(self, row):
		'''
		returns the nth full row.
		'''
		east = row * self.height
		west = east + self.length
		row = self.maze[east:west]
		return row

	def get_column(self, column):
		'''
		returns the nth full column.
		'''
		num_columns = self.length
		column = self.maze[column::num_columns]
		return column

	def get_every_row(self):
		'''
		returns an array arrays; a list of every row.
		'''
		every_row = []
		for row in range(0, self.height):
			every_row.append(self.get_row(row))
		return every_row

	def get_every_column(self):
		'''
		returns an array arrays; a list of every column.
		'''
		every_column = []
		for column in range(0, self.length):
			every_column.append(self.get_column(column))
		return every_column

	def generate_maze(self, loc = None):
		'''
		generates a perfect maze.
		its done recursively via a depth-first traversal tree.
		this is a setter function; it does not return anything.
		---
		key = cardinal direction
		rev = reversed cardinal direction
		loc = root location
		nbr = neighbor location
		'''
		if loc is None:
			# start the trees loc at a random point in the maze.
			# this doesnt infer a start/exit in the finished maze.
			# one can always find a path from any point A to B;
			# the program will decide these points later.
			loc = random.randint(0, len(self.maze) - 1)
			# note our visited list exists as the maze property.

		# first, fill the maze spot with an empty block.
		self.maze[loc] = Block()

		# grab the location id from each cardinal direction.
		neighbor_locations = {
			'north': loc - self.length,
			'south': loc + self.length,
			'east': loc - 1,
			'west': loc + 1,
		}

		# this is useful for doubly-linked vertices.
		reverse_compass = {
			'north': 'south',
			'south': 'north',
			'east': 'west',
			'west': 'east',
		}

		# validate will remove indices that are out-of-bounds.
		def validate(location):
			if len(self.maze) > location >= 0:
				return location
			else:
				return None

		# update neighbors with validate.
		for key, nbr in neighbor_locations.items():
			# it is safe to update a key's value in a loop;
			# it isnt safe to update a key in a loop.
			neighbor_locations[key] = validate(nbr)

		for key, nbr in neighbor_locations.items():
			# rev reverses key, a cardinal direction.
			rev = reverse_compass[key]
			# nbr is empty, representing a maze boundary.
			if nbr is None:
				self.maze[loc].neighbors[key] = None
				pass

			# nbr is an int, representing a spot in maze.
			else:
				# this spot is empty! fill it up!
				if self.maze[nbr] is None:
					# generate a new maze block.
					self.generate_maze(nbr)
					# link up the net / graph / tree.
					self.maze[loc].neighbors[key] = self.maze[nbr]
					self.maze[nbr].neighbors[rev] = self.maze[loc]

				# this spot is filled.
				else:
					pass


def get_glyph(north, south, east, west):
	'''
	this function returns a maze drawing character.
	'''
	# == FIXME ==
	# this function is awkwardly large.
	# not sure where to put it semantically.
	# == TODO ==
	# these unicode characters must be converted!
	# like emojis, its a code smell to have them.

	# four passages
	if north and south and east and west:
		glyph = ' '
	# three passages
	elif south and east and west and not (north):
		glyph = '╵'
	elif north and east and west and not (south):
		glyph = '╷'
	elif north and south and west and not (east):
		glyph = '╶'
	elif north and south and east and not (west):
		glyph = '╴'
	# two passages
	elif north and south and not (east or west):
		glyph = '─'
	elif north and east and not (south or west):
		glyph = '┐'
	elif north and west and not (south or east):
		glyph = '┌'
	elif south and east and not (north or west):
		glyph = '┘'
	elif south and west and not (north or east):
		glyph = '└'
	elif east and west and not (north or south):
		glyph = '│'
	# one passage
	elif north and not (south or east or west):
		glyph = '┬'
	elif south and not (north or east or west):
		glyph = '┴'
	elif east and not (north or south or west):
		glyph = '┤'
	elif west and not (north or south or east):
		glyph = '├'
	# zero passages
	elif not (north or south or east or west):
		glyph = '┼'

	return glyph