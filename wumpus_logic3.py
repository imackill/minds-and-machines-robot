class Node:
    def __init__(self, id: tuple, *parents):

        self.parents: list[Node] = list(parents)
        self.id = id

        self.children = []
        if(self.parents != []):
            for p in self.parents:
                p.children.append(self)

        self.states = set()
        self.safe = None

class WumpusLogic:
    def __init__(self, move_func: function, data_func: function):
        self.move = move_func
        self.data = data_func

        self.nodes = {
            (0,0) : Node((0,0))
        }

        self.pos = self.nodes[(0,0)]

        self.posW = None
        self.posG = None
        self.posP = []

        self.mapped_nodes = set()

    def get_nodes_attr(self, k, v):
        res = []
        for id, node in self.nodes:
            if(node.__getattribute__(k) == v):
                res.append(node)
        return res

    def get_nodes_state(self, v):
        res = []
        for id, node in self.nodes.items():
            if(v in node.states):
                res.append(node)
        return res

    def get_nbr_nodes(self, node):
        # get list of ids for possible neighboring nodes
        ids = [
            (node.id[0]+1, node.id[1]),
            (node.id[0], node.id[1]+1),
            (node.id[0]-1, node.id[1]),
            (node.id[0], node.id[1]-1),
        ]

        # init result
        res = []
        # go through and check valid nodes
        for id in ids:

            # nonexistent add None
            if(id[0] > 3 or id[0] < 0 or id[1] > 3 or id[1] < 0):
                res.append(None)
                continue

            # if necessary, create new node
            if(id not in self.nodes.keys()):
                self.nodes[id] = Node(id, node)

            # add node to parent-child relation
            if(node not in self.nodes[id].parents):
                self.nodes[id].parents.append(node)

            # add node to result
            res.append(self.nodes[id])
        return res

    def _map(self, *args):

        if(self.posG != None):
            self._pathToNode(self.posG)
            return [None, None]

        # get the last visited node
        last_node = args[0]

        # filter out nonexistent nodes
        available_nodes = list(filter(
            lambda node: node != None or node == last_node,
            self.get_nbr_nodes(self.pos)
        ))

        # get data
        data = self.data()

        # data is GOLD, SMELL, BREEZE

        # get states as a set
        state_set = set()
        if(data[0] == 1): state_set.add("g")
        if(data[1] == 1): state_set.add("s")
        if(data[2] == 1): state_set.add("b")

        # add states node
        self.pos.states |= state_set

        # mark ndoes as safe if applicable
        for node in available_nodes:
            if(self.posW != None and len(self.posP) == 2):
                if(node not in self.posP and node != self.posW):
                    node.safe = True
            elif("s" not in state_set and "b" not in state_set or node in self.mapped_nodes):
                node.safe = True

        movable_nodes = list(filter(
            lambda node: node.safe == True and node not in self.mapped_nodes,
            available_nodes
        ))

        if(len(movable_nodes) > 0):
            # if there is a valid SAFE node, move to it
            next_node = movable_nodes[0]

            last_node = self.pos
            self.mapped_nodes.add(last_node)
            # call pathtonode
            self._pathToNode(next_node)
            return [self._map, last_node]
        
        else:
            self.mapped_nodes.add(self.pos)

            # get set of unmapped safe nodes
            node_set = set(filter(
                lambda node: node.safe == True,
                list(self.nodes.values())
            ))-self.mapped_nodes


            if(len(node_set) > 0):
                next_node = list(node_set)[0]
                last_node = self.pos

                self._pathToNode(next_node)

                return [self._map, last_node]
        
        return [self._think, [0, last_node]]# 0 represents this is the first though
            

    def _pathToNode(self, node):

        # get change in row and change in column
        # between current position and desired position

        last_node = self.pos

        # while it isn't at destination
        while self.pos.id != node.id:

            dr = node.id[0]-self.pos.id[0]
            dc = node.id[1]-self.pos.id[1]

            # get available nodes
            available_nodes = self.get_nbr_nodes(self.pos)

            # get nodes based on direction
            node_costs = {
                (-1, 0): available_nodes[0],
                (0, -1): available_nodes[1],
                (1, 0): available_nodes[2],
                (0, 1): available_nodes[3],
            }
            
            # remove nonexistent or bad nodes
            keys_to_del = set()
            for key, val in node_costs.items():
                if(val == None or val.safe != True):
                    keys_to_del.add(key)
        
            if(dr > 0 and (-1, 0) not in keys_to_del):
                next_node = node_costs[(-1, 0)]
                self.move((1, 0))
                self.pos = next_node
            elif(dc > 0 and(0, -1) not in keys_to_del):
                next_node = node_costs[(0, -1)]
                self.move((0, 1))
                self.pos = next_node
            elif(dr < 0 and (1, 0) not in keys_to_del):
                next_node = node_costs[(1, 0)]
                self.move((-1, 0))
                self.pos = next_node
            elif(dc < 0 and (0, 1) not in keys_to_del):
                next_node = node_costs[(0, 1)]
                self.move((0, -1))
                self.pos = next_node
            else:
                node = self.nodes[(0,0)]
                self.mapped_nodes = set()


    def _think(self, args):

        attempt = args[0]# 0 the first time, 1 the second
        last_node = args[1]

        # get nodes adjacent to glitter
        g_nodes = self.get_nodes_state("g")

        # get nodes adjacent to smell
        s_nodes = self.get_nodes_state("s")

        # get nodes adjacent to breeze
        b_nodes = self.get_nodes_state("b")

        # stat vars keep track of whether or not
        # a conclusion is made about the position
        # of any special tiles, if all end false
        # post processing, then the robot cannot
        # solve the puzzle
        g_stat = False
        s_stat = False
        p_stat = False

        if(len(g_nodes) > 0):
            g_stat = self._findGold(g_nodes)

        if(len(s_nodes) > 0):
            s_stat = self._findWumpus(s_nodes)

        if(len(b_nodes) > 0):
            p_stat = self._findPits(b_nodes)

        
        if(self.posG != None):
            self._pathToNode(self.posG)
            return [None, None]
        elif(attempt == 0):
            return [self._think, [1, last_node]]
        elif(attempt == 1):
            # check if dangerous tiles are known
            if(self.posW != None and len(self.posP) == 2):
                for node in self.nodes.values():
                    if(node not in self.posP and node != self.posW):
                        self.nodes[node.id].safe = True
            return [self._map, last_node]

        # puzzle would be impossible
        elif(g_stat == False and s_stat == False and p_stat == False):
            raise Exception("Impossible to Solve")

    # find the gold
    def _findGold(self, nodes):
        # return True if we already know the location of the gold
        if(self.posG != None):
            return True
        
        g_cands = []

        # get possible gold nodes
        for node in nodes:
            nbrs = filter(
                lambda n: n != None and n.safe == True and n not in self.posP + [self.posW],
                self.get_nbr_nodes(node)
            )
            g_cands.append(set(nbrs))

        # get the intersection of all possibilities
        if(len(g_cands) > 1):
            final_set = g_cands[0]
            for cand_set in g_cands[1:]:
                final_set &= cand_set
        else:
            final_set = g_cands[0]


        # if it is possible to find, final_set will have a length of 1
        if(len(final_set) == 1):
            self.posG = list(final_set)[0]
            return True
        elif(len(final_set) > 1):
            invalid_cands = set()
            for node in final_set:
                states = list(e.states for e  in filter(
                    lambda n: n != None,
                    self.get_nbr_nodes(node)
                ))
                for s in states:
                    if(len(s) == 0):
                        invalid_cands.add(node)
            
            self.posG = list(final_set - invalid_cands)[0]
            return True
        else:
            return False

    # essentially the same as the gold function
    def _findWumpus(self, nodes):
        # return True if we already know the location of the wumpus
        if(self.posW != None):
            return True

        w_cands = []
        # get a set of nonsafe adjacent nodes to a smell node
        for node in nodes:
            nbrs = filter(
                lambda n: n != None and n.safe != True and n not in self.posP,
                self.get_nbr_nodes(node)
            )
            w_cands.append(set(nbrs))

        # get the intersection of all smell nodes
        if(len(w_cands) > 1):
            final_set = w_cands[0]
            for cand_set in w_cands[1:]:
                final_set &= cand_set
        else:
            final_set = w_cands[0]

        if(len(final_set) == 1):
            self.posW = list(final_set)[0]
            return True
        else:
            # no conclusion was made
            return False

    # a little different than the other 2
    # have to consider the possibility of
    # overlapping pit adjacent squares
    def _findPits(self, nodes):

        # in case we already know pit locations
        if(len(self.posP) == 2):
            return True

        # get intersection fo neighbors for all possible pairs of nodes
        # so for a set of nodes {a, b, c, d}
        # return [nbrs(a) & nbrs(b), nbrs(b) & nbrs(c), etc...]

        node_nbrs = list(map(
            lambda n: set(
                filter(
                    lambda x: x != None and x.safe != True and x != self.posW and x != self.posG,
                    self.get_nbr_nodes(n)
            )),
            list(nodes)
        ))

        for i in range(len(node_nbrs)):
            j = i+1 if i != len(node_nbrs)-1 else 0
            node_nbrs[i] &= node_nbrs[j]

        # remove any empty intersections
        node_nbrs = list(filter(
            lambda s: len(s) != 0,
            node_nbrs
        ))
        
        pits = list(list(e)[0] for e in node_nbrs)
        pits = list(set(pits))

        if(len(pits) == 1):
            # set part of global pits to be pits
            if(pits[0] not in self.posP):
                self.posP.append(pits[0])
                return True
            for node in self.get_nbr_nodes(pits[0]):
                if(node != None):
                    node.safe = True
            else:
                # no new data gained
                return False
        
        elif(len(pits) == 2):
            # set global pits to be pits
            self.posP = pits
            for node in self.get_nbr_nodes(pits[0])+self.get_nbr_nodes(pits[1]):
                if(node != None):
                    node.safe = True if node.safe != False else False
            return True
        
        elif(len(pits) > 2):
            pit_locations = list(pit.id for pit in pits)
            print(pit_locations)
            # FIXME: remember to add logic for picking between overlap
            return True
        
        # no data gained from this run through
        # len(pits) == 0
        return False



    def loop(self):
        args = self.nodes[0,0]
        phase, args = self._map(args)
        while phase != None:
            phase, args = phase(args)