def numIslands(grid):
    """Take in a grid of 1s (land) and 0s (water) and return the number of islands."""
    islands = []
    land = set()
    queue = []
    for col in range(len(grid)):
        for row in range(len(grid[col])):
            cell = grid[col][row]
            if cell == 1:
                land.add((col, row))

    while land:
        queue.append(list(land).pop())
        islands.append(set())
        while len(queue) > 0:
            current_land = queue.pop()
            if(current_land in land):
                land.remove(current_land)
                islands[-1].add(current_land)
                col, row = current_land

                if col != 0 and grid[col - 1][row] == 1:
                    queue.append((col - 1, row))
                if col < len(grid) - 1 and grid[col + 1][row] == 1:
                    queue.append((col + 1, row))
                if row != 0 and grid[col][row - 1] == 1:
                    queue.append((col, row - 1))
                if row < len(grid[col]) - 1 and grid[col][row + 1] == 1:
                    queue.append((col, row + 1))
    return len(islands)

def timeToRot(grid):
    """
    Take in a grid of numbers, where 0 is an empty space, 1 is a fresh orange, and 2 is a rotten
    orange. Each minute, a rotten orange contaminates its 4-directional neighbors. Return the number
    of minutes until all oranges rot.
    """

    orange_queue = []
    for col in range(len(grid)):
        for row in range(len(grid[col])):
            if grid[col][row] == 2:
                orange_queue.insert(0, (col, row))
    
    distance_dict = {}
    for orange in orange_queue:
        distance_dict[orange] = 0
    largest_dist = 0
    while len(orange_queue) > 0:
        current_orange = orange_queue.pop()
        current_distance = distance_dict[current_orange]
        if current_distance > largest_dist:
            largest_dist = current_distance
        current_col, current_row = current_orange
        grid[current_col][current_row] = 2

        edge_check = [0, -1, 0, 1]
        for i in range(len(edge_check)):
            row = current_row + edge_check[i]
            col = current_col + edge_check[(i + 1) % 4]
            if col > 0 and col < len(grid) and row >=0 and row < len(grid[col]) and grid[col][row] == 1 :
                cell = (col, row)
                if cell in distance_dict:
                    if distance_dict[cell] < current_distance + 1:
                        distance_dict[cell] = current_distance + 1
                else:
                    distance_dict[cell] = current_distance + 1
                    orange_queue.insert(0, cell)
    for col in range(len(grid)):
        for row in range(len(grid[col])):
            if grid[col][row] == 1:
                return -1
    return largest_dist

def courseOrder(numCourses, prerequisites):
    """Return a course schedule according to the prerequisites provided."""
     adj_list = defaultdict(list)
        indegree = {}
        for dest, src in prerequisites:
            adj_list[src].append(dest)

            indegree[dest] = indegree.get(dest, 0) + 1

        zero_indegree_queue = deque([k for k in range(numCourses) if k not in indegree])

        topological_sorted_order = []

        while zero_indegree_queue:

            vertex = zero_indegree_queue.popleft()
            topological_sorted_order.append(vertex)

            if vertex in adj_list:
                for neighbor in adj_list[vertex]:
                    indegree[neighbor] -= 1

                    if indegree[neighbor] == 0:
                        zero_indegree_queue.append(neighbor)

        return topological_sorted_order if len(topological_sorted_order) == numCourses else []

def wordLadderLength(beginWord, endWord, wordList):
    """Return the length of the shortest word chain from beginWord to endWord, using words from wordList."""

    def compareWords(firstWord, secondWord):
        difference = 0
        for i in range(len(firstWord)):
            if firstWord[i] != secondWord[i]:
                difference += 1
        return difference == 1

    def findClosest(word):
        close = []
        for i in wordList:
            if compareWords(word, i):
                close.append(i)
        return close

    def recursive(currentWord, targetWord, path=[], seen=set()):
        seen.add(currentWord)
        path.append(currentWord)
        neighbors = findClosest(currentWord)
        for neighbor in neighbors:
            if neighbor == targetWord:
                return path
            fullPath = None
            if neighbor not in seen:
                fullPath = recursive(neighbor, targetWord, path, seen)
            if fullPath is not None:
                return fullPath
        path.pop()
        return None
    
    return len(recursive(beginWord, endWord))