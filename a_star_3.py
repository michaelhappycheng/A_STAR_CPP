import heapq
import numpy as np

expansion_count = [0]
AStar_count = [0]

'''
implementation reference:
https://bradfieldcs.com/algos/trees/priority-queues-with-binary-heaps/
'''
# TODO(Completed): use binary-tree to implement priority queue
# For C++ purpose
# Also, we need to update elements in priority queue

# TODO(completed): implement priority queue with binary heap that 
# 		takes struct node.

# FIX(completed) : binary heap starts from index 0, not index 1

# TODO(implement A*)
class Node():
	def __init__(self, f_value, coordinate):
		self.f_value = f_value
		self.coordinate = coordinate

class BinaryHeap():
	def __init__(self):
		self.items = []

	def __len__(self):
		return len(self.items)

	def insert(self, f_val, coordinate):
		new_node = Node(f_val, coordinate)
		self.items.append(new_node)
		self.percolate_up()

	def percolate_up(self):
		i = len(self.items) - 1
		while i // 2 > 0:
			if self.items[i].f_value < self.items[i // 2].f_value:
				self.items[i // 2], self.items[i] = \
					self.items[i], self.items[i // 2]
			i = i // 2


	def min_child(self, i):
		# i = 0 i*2+1 = 1
		# return smaller child foor root at i
		if i * 2 + 2 >= len(self):
			return i * 2 + 1
		if self.items[i * 2 + 1].f_value < self.items[i * 2 + 2].f_value:
			return i * 2 + 1
		return i * 2 + 2
		

	def percolate_down(self, i):
		while i * 2 + 2 < len(self.items):
			mc = self.min_child(i)
			if self.items[i].f_value > self.items[mc].f_value:
				self.items[i], self.items[mc] = \
					self.items[mc], self.items[i]
			i = mc

	def find_min(self):
		# return the item with the minimum key value
		return self.items[0]

	def del_min(self):
		# return the item with minimum key value, 
		# remove item from heap
		return_value = self.items[0]
		self.items[0] = self.items[len(self.items)-1]
		self.items.pop()
		self.percolate_down(0)
		return return_value
	
	# 		0
	# 	1		2
	# 3	   4  5		6
	def build_heap(self, alist):
		# build a new heapfrom a list of keys
		i = len(alist) // 2
		self.items = alist
		while i >= 0:
			self.percolate_down(i)
			i = i - 1
	
	def same_node(self, node_a, node_b):
		a_f, a_coordinate = node_a.f_value, node_a.coordinate
		b_f, b_coordinate = node_b.f_value, node_b.coordinate
		return a_f == b_f and a_coordinate == b_coordinate

	def remove_node_in_list(self, node, alist):
		for i, elem in enumerate(alist):
			if self.same_node(node, elem):
				del alist[i]
				return
	def update_heap(self, old_node, new_node):
		new_list = self.items[:]	# can't append shit here cause it doesn't return shit
		new_list.append(new_node)
		self.remove_node_in_list(old_node, new_list)
		self.build_heap(new_list)
		# print('itmes after update heap', [(item.f_value, item.coordinate) for item in self.items])

def binary_heap_test():		
	open_set = [Node(3,(0,0)),Node(5,(0,1)),Node(2,(0,2)),Node(4,(0,3)),Node(1,(0,4))]
	BH = BinaryHeap()
	# alist = [4,6,2,7,9,8,1]
	BH.build_heap(open_set)
	print('show all items', [(item.f_value, item.coordinate) for item in BH.items])
	minNode = BH.find_min()
	print('find min', minNode.f_value, minNode.coordinate)
	BH.update_heap(Node(1,(0,4)), Node(-10, (2,2)))
	print('after update 1,(0,4) to -10, (2,2)', [(item.f_value, item.coordinate) for item in BH.items])
	minNode = BH.find_min()
	print('find min', minNode.f_value, minNode.coordinate)
	# print('find min again', BH.find_min())

def process_grid():
	'''
	return a grid class Grid
	'''
	grid = WeightedGrid()
	grid.walls = set()
	grid.start, grid.goal = set(), set()
	grid.rowCount, grid.colCount = 0, 0
	# 14, 16 failed
	with open('inputs/6.txt') as inputfile:
		for i, line in enumerate(inputfile):
			line = line.replace(' ', '')
			if i == 0:
				grid.rowCount = int(line.strip())
				continue
			elif i == 1:
				grid.colCount = int(line.strip())
				continue			
			for j, face in enumerate(line):
				if line[j] == 'x':
					grid.walls.add((i-2, j))
				elif line[j] == 's':
					grid.start = (i-2, j)
				elif line[j] == 'g':
					grid.goal = (i-2, j)
	return grid

class Grid:
	def __init__(self, rowCount = 0, colCount = 0):
		self.rowCount = rowCount
		self.colCount = colCount
		self.walls = set()
		self.start = None
		self.goal = None

	def in_bounds(self, loc):
		(x, y) = loc
		return 0 <= x < self.rowCount and 0 <= y < self.colCount

	def passable(self, loc):
		return loc not in self.walls

	def neighbors(self, loc):
		(x, y) = loc
		results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
		results = list(filter(self.in_bounds, results))
		# results = list(filter(self.passable, results))
		return results

class WeightedGrid(Grid):
	def __init__(self, rowCount=0, colCount=0):
		super().__init__(rowCount, colCount)
		self.weights = {}
	def cost(self, from_node, to_node):
		return self.weights.get(to_node, 1)

def ReconstructPath(came_from, start, goal):
	print(start, goal.coordinate)
	current = goal.coordinate
	path = [current]
	while current != start:
		# print('i am stuck in reconstructpth while loop', current, came_from[current])
		current = came_from[current]
		path.append(current)
	path.reverse()
	return path

def form_grid(grid, path=None):
	colCount = int(grid.colCount)
	rowCount = int(grid.rowCount)
	res = [['_'] * colCount for _ in range(rowCount)]
	for x in range(rowCount):
		for y in range(colCount):
			if (x,y) == grid.start:
				res[x][y] = 'S'
			elif (x,y) == grid.goal:
				res[x][y] = 'G'
			elif (x,y) in grid.walls:
				res[x][y] = 'x'
			elif path and (x,y) in path:
				res[x][y] = '#'
	return res

def form_failed_grid(grid, traversed):
	colCount = int(grid.colCount)
	rowCount = int(grid.rowCount)
	res = [['_'] * colCount for _ in range(rowCount)]
	for x in range(rowCount):
		for y in range(colCount):
			if (x,y) == grid.start:
				res[x][y] = 'S'
			elif (x,y) == grid.goal:
				res[x][y] = 'G'
			elif (x,y) in grid.walls:
				res[x][y] = 'x'
			if (x,y) in traversed:
				res[x][y] = '#'
	return res

def draw_grid(grid):
	for row in grid:
		col_rep = ''
		for c_elem in row:
			col_rep += c_elem
		print(col_rep)
	print('this is end of the graph')

def GetHeuristic(a, b):
	(x1, y1) = a
	(x2, y2) = b
	return abs(x1 - x2) + abs(y1 - y2)

count = [0]

def AStar(grid, start, goal):
	
	open_set = BinaryHeap()

	came_from = {start:None}
	g_score = {start:0}
	f_score = {start:GetHeuristic(start, goal)}
	closed_set = []

	# heapq.heappush(open_set, (f_score[start], start))
	open_set.insert(f_score[start], start)

	while open_set:
		# expand 
		currentNode = open_set.find_min()		
		open_set.del_min()
		expansion_count[0] += 1

		if currentNode.coordinate == goal:
			print('reached goal!!')
			path = ReconstructPath(came_from, start, currentNode)
			# print(np.matrix(draw_grid(grid, path)))
			draw_grid(form_grid(grid, path))
			return
		
		if currentNode.coordinate in grid.walls:
			print('reached wall!!')
			# print('wall path', [i for i in came_from.items()])
			path = ReconstructPath(came_from, start, currentNode)
			# print(np.matrix(draw_grid(grid, path)))
			draw_grid(form_grid(grid, path))
			AStar_count[0] += 1
			continue
		
		# if current not in wall or not goal, generate
		closed_set.append(currentNode)
		
		for nei in grid.neighbors(currentNode.coordinate):
			
			# if nei not in open_set U closed_set
			if(nei not in [item.coordinate for item in open_set.items] and 
				nei not in [i.coordinate for i in closed_set]):
				came_from[nei] = currentNode.coordinate
				g_score[nei] = g_score[currentNode.coordinate] + 1
				f_score[nei] = g_score[nei] + GetHeuristic(nei, goal)
				open_set.insert(f_score[nei], nei)
			elif nei in [item.coordinate for item in open_set.items]:
				tentative_gscore = g_score[currentNode.coordinate] + 1
				if tentative_gscore >= g_score[nei]:
					# this is not a better path
					print('nei is not a better path', nei)
					continue
				# update f and g because this is best path
				came_from[nei] = currentNode.coordinate
				old_node = Node(f_score[nei], nei)
				g_score[nei] = tentative_gscore
				f_score[nei] = g_score[nei] + GetHeuristic(nei, goal)
				new_node = Node(f_score[nei], nei)

				# UpdateOpenSet(open_set, location, f_score)
				open_set.update_heap(old_node, new_node)

	print('closed_set', [i.coordinate for i in closed_set], start, goal)	
	draw_grid(form_failed_grid(grid, [i.coordinate for i in closed_set]))
	print(' no more item in open_set')
open_set = [(3,(0,0)),(5,(0,1)),(2,(0,2)),(4,(0,3)),(1,(0,4))]
#update point(0,1) to have value -1

if __name__ == '__main__':
	# print(SPACE_HOLDER.coordinate)c
	# blocked_count = [0]
	# expanded_count = [0]
	grid = process_grid()
	# print(np.matrix(draw_grid(grid)))
	draw_grid(form_grid(grid))
	AStar(grid, grid.start, grid.goal)
	# print('blocked_count is ', blocked_count[0])
	# print('expanded_count is ', expanded_count[0])
	print('expansion count is ', expansion_count[0])
	print('AStar count is', AStar_count[0])





