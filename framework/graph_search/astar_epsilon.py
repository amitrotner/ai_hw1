from .graph_problem_interface import *
from .astar import AStar
from typing import Optional, Callable
import numpy as np
import math


class AStarEpsilon(AStar):
    """
    This class implements the (weighted) A*Epsilon search algorithm.
    A*Epsilon algorithm basically works like the A* algorithm, but with
    another way to choose the next node to expand from the open queue.
    """

    solver_name = 'A*eps'

    def __init__(self,
                 heuristic_function_type: HeuristicFunctionType,
                 within_focal_priority_function: Callable[[SearchNode, GraphProblem, 'AStarEpsilon'], float],
                 heuristic_weight: float = 0.5,
                 max_nr_states_to_expand: Optional[int] = None,
                 focal_epsilon: float = 0.1,
                 max_focal_size: Optional[int] = None):
        # A* is a graph search algorithm. Hence, we use close set.
        super(AStarEpsilon, self).__init__(heuristic_function_type, heuristic_weight,
                                           max_nr_states_to_expand=max_nr_states_to_expand)
        self.focal_epsilon = focal_epsilon
        if focal_epsilon < 0:
            raise ValueError(f'The argument `focal_epsilon` for A*eps should be >= 0; '
                             f'given focal_epsilon={focal_epsilon}.')
        self.within_focal_priority_function = within_focal_priority_function
        self.max_focal_size = max_focal_size

    def _init_solver(self, problem):
        super(AStarEpsilon, self)._init_solver(problem)

    def _extract_next_search_node_to_expand(self, problem: GraphProblem) -> Optional[SearchNode]:
        """
        Extracts the next node to expand from the open queue,
         by focusing on the current FOCAL and choosing the node
         with the best within_focal_priority from it.
        TODO [Ex.32]: Implement this method!
        Find the minimum expanding-priority value in the `open` queue.
        Calculate the maximum expanding-priority of the FOCAL, which is
         the min expanding-priority in open multiplied by (1 + eps) where
         eps is stored under `self.focal_epsilon`.
        Create the FOCAL by popping items from the `open` queue and inserting
         them into a focal list. Don't forget to satisfy the constraint of
         `self.max_nr_states_to_expand` if it is set (not None).
        Notice: You might want to pop items from the `open` priority queue,
         and then choose an item out of these popped items. Don't forget:
         the other items have to be pushed back into open.
        Inspect the base class `BestFirstSearch` to retrieve the type of
         the field `open`. Then find the definition of this type and find
         the right methods to use (you might want to peek the head node, to
         pop/push nodes and to query whether the queue is empty).
        For each node (candidate) in the created focal, calculate its priority
         by calling the function `self.within_focal_priority_function` on it.
         This function expects to get 3 values: the node, the problem and the
         solver (self). You can create an array of these priority value. Then,
         use `np.argmin()` to find the index of the item (within this array)
         with the minimal value. After having this index you could pop this
         item from the focal (at this index). This is the node that have to
         be eventually returned.
        Don't forget to handle correctly corner-case like when the open queue
         is empty. In this case a value of `None` has to be returned.
        Note: All the nodes that were in the open queue at the beginning of this
         method should be kept in the open queue at the end of this method, except
         for the extracted (and returned) node.
        """

        if self.open.is_empty():
            return None
        min_expanding_priority = self.open.peek_next_node().expanding_priority
        focal = []
        nr_nodes_in_focal = 0
        while self.open.is_empty() is False:
            if self.max_focal_size is not None and nr_nodes_in_focal == self.max_focal_size:
                break
            if self.open.peek_next_node().expanding_priority <= (1 + self.focal_epsilon) * min_expanding_priority:
                focal.append(self.open.pop_next_node())
                nr_nodes_in_focal += 1
            else:
                break
        min_focal_array = []
        for node in focal:
            min_focal_array.append(self.within_focal_priority_function(node, problem, self))
        node_to_return = focal.pop(np.argmin(min_focal_array))
        self.close.add_node(node_to_return)
        while len(focal) > 0:
            self.open.push_node(focal.pop(0))
        return node_to_return
