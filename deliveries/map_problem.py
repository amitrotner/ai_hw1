from framework import *

from typing import Iterator, Optional, Callable
from dataclasses import dataclass

__all__ = ['MapState', 'MapProblem']


@dataclass(frozen=True)
class MapState(GraphProblemState):
    """
    StreetsMap state is represents the current geographic location on the map.
    This location is defined by the junction index.
    """
    junction_id: int

    def __eq__(self, other):
        assert isinstance(other, MapState)
        return other.junction_id == self.junction_id

    def __hash__(self):
        return hash(self.junction_id)

    def __str__(self):
        return str(self.junction_id).rjust(5, ' ')


class MapProblem(GraphProblem):
    """
    Represents a problem on the streets map.
    The problem is defined by a source location on the map and a destination.
    """

    name = 'StreetsMap'

    def __init__(self, streets_map: StreetsMap, source_junction_id: int, target_junction_id: int,
                 road_cost_fn: Optional[Callable[[Link], Cost]] = None,
                 zero_road_cost: Optional[Cost] = None):
        initial_state = MapState(source_junction_id)
        super(MapProblem, self).__init__(initial_state)
        self.streets_map = streets_map
        self.target_junction_id = target_junction_id
        self.road_cost_fn = road_cost_fn
        self.zero_road_cost = zero_road_cost
        self.name += f'(src: {source_junction_id} dst: {target_junction_id})'

    def expand_state_with_costs(self, state_to_expand: GraphProblemState) -> Iterator[OperatorResult]:
        """
        For a given state, iterates over its successor states.
        The successor states represents the junctions to which there
         exists a road originates from the given state.
        """

        # All of the states in this problem are instances of the class `MapState`.
        assert isinstance(state_to_expand, MapState)

        # Get the junction (in the map) that is represented by the state to expand.
        junction = self.streets_map[state_to_expand.junction_id]

        for link in junction.outgoing_links:
            yield OperatorResult(successor_state=MapState(link.target),
                                 operator_cost=link.distance if self.road_cost_fn is None else self.road_cost_fn(link))

        # TODO [Ex.10]: (Done)
        #  Read the documentation of this method in the base class `GraphProblem.expand_state_with_costs()`.
        #  Finish the implementation of this method.
        #  Iterate over the outgoing links of the current junction (find the implementation of `Junction`
        #  type to see the exact field name to access the outgoing links). For each link:
        #    (1) Create the successor state (it should be an instance of class `MapState`). This state represents the
        #        target junction of the current link;
        #    (2) Calculate the operator cost: if `self.road_cost_fn` is None the operator cost should be
        #        `link.distance`, otherwise call the function `self.road_cost_fn` with the link as an argument
        #        and set the operator cost to be the returned value of this call;
        #    (3) Yield an object of type `OperatorResult` with the successor state and the operator cost (you don't
        #        have to specify the operator name here).
        #  Note: Generally, in order to check whether a variable is set to None you should use the expression:
        #        `my_variable_to_check is None`, and particularly do NOT use comparison (==).

    def is_goal(self, state: GraphProblemState) -> bool:
        """
        :return: Whether a given map state represents the destination.
        """
        assert (isinstance(state, MapState))

        # TODO [Ex.10]: modify the returned value to indicate whether `state` is a final state.
        # You may use the problem's input parameters (stored as fields of this object by the constructor).
        return state.junction_id == self.target_junction_id  # TODO: modify this! (Done)

    def get_zero_cost(self) -> Cost:
        if self.zero_road_cost is not None:
            return self.zero_road_cost
        return 0.0
