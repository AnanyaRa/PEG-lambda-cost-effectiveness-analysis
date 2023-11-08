import InputData as D
class Node:
    """ base (master) class for nodes """
    def __init__(self, name, cost, health_utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param health_utility: health utility of visiting this node
        """

        self.name = name
        self.cost = cost
        self.healthUtility = health_utility

    def get_expected_cost(self):
        """ abstract method to be overridden in derived classes
        :returns expected cost of this node """

    def get_expected_health_utility(self):
        """ abstract method to be overridden in derived classes
        :returns expected health utility of this node """


class ChanceNode(Node):

    def __init__(self, name, cost, future_nodes, probs, health_utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param future_nodes: (list) future nodes connected to this node
        :param probs: (list) probability of future nodes
        """

        Node.__init__(self, name, cost, health_utility)
        self.futureNodes = future_nodes
        self.probs = probs

    def get_expected_cost(self):
        """
        :return: expected cost of this chance node
        E[cost] = (cost of visiting this node)
                  + sum_{i}(probability of future node i)*(E[cost of future node i])
        """

        # expected cost initialized with the cost of visiting the current node
        exp_cost = self.cost

        # go over all future nodes
        i = 0
        for node in self.futureNodes:
            # increment expected cost by
            # (probability of visiting this future node) * (expected cost of this future node)
            exp_cost += self.probs[i]*node.get_expected_cost()
            i += 1

        return exp_cost

    def get_expected_health_utility(self):
        """
        :return: expected health utility of this chance node
        E[health utility] = (health utility of visiting this node)
                  + sum_{i}(probability of future node i)*(E[health utility of future node i])
        """
        exp_health_utility = self.healthUtility
        i = 0
        for node in self.futureNodes:
            exp_health_utility += self.probs[i]*node.get_expected_health_utility()
            i += 1

        return exp_health_utility


class TerminalNode(Node):

    def __init__(self, name, cost, health_utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        """

        Node.__init__(self, name, cost, health_utility)

    def get_expected_cost(self):
        """
        :return: cost of this visiting this terminal node
        """
        return self.cost

    def get_expected_health_utility(self):
        """
        :return: health utility of visiting this terminal node
        """
        return self.healthUtility


class DecisionNode(Node):

    def __init__(self, name, cost, future_nodes, health_utility):
        """
        :param name: name of this node
        :param cost: cost of visiting this node
        :param future_nodes: (list) future nodes connected to this node
        (assumes that future nodes can only be chance or terminal nodes)
        """

        Node.__init__(self, name, cost, health_utility)
        self.futureNode = future_nodes

    def get_expected_cost(self):
        """ returns the expected costs of future nodes
        :return: a dictionary of expected costs of future nodes with node names as dictionary keys
        """

        # a dictionary to store the expected cost of future nodes
        exp_costs = dict()
        # go over all future nodes
        for node in self.futureNode:
            # add the expected cost of this future node to the dictionary
            exp_costs[node.name] = self.cost + node.get_expected_cost()

        return exp_costs

    def get_expected_health_utility(self):
        """ returns the expected health utility of future nodes
        :return: a dictionary of expected health utility of future nodes with node names as dictionary keys
        """
        # a dictionary to store the expected health utility of future nodes
        exp_health_utilities = dict()
        # go over all future nodes
        for node in self.futureNode:
            # add the expected health utility of this future node to the dictionary
            exp_health_utilities[node.name] = self.healthUtility + node.get_expected_health_utility()

        return exp_health_utilities


def simulate_decision_tree(drug_cost=D.DRUG_COST, hosp_cost=D.HOSP_COST, relative_risk_vax=D.DRUG_RR_VAX_OR_LR,
                           relative_risk_unvax=D.DRUG_RR_UNVAX_HR, rr_pax_vax=D.PAXLOVID_RR_VAX_OR_LR, rr_pax_unvax=D.PAXLOVID_RR_UNVAX_HR):
    T1 = TerminalNode('T1', hosp_cost, 1)
    T2 = TerminalNode('T2', 0, 0)

    VAX_0_0 = ChanceNode(name='VAX_0_0', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_65*D.VAX_HOSP_MULT*rr_pax_vax,
                                                                       1 - (D.HOSP_COMORB_65*D.VAX_HOSP_MULT*rr_pax_vax)], cost=D.PAXLOVID_COST, health_utility=0)
    UNVAX_0_0 = ChanceNode(name='UNVAX_0_0', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_65*rr_pax_unvax,
                                                                           1-(D.HOSP_COMORB_65*rr_pax_unvax)], cost=D.PAXLOVID_COST, health_utility=0)
    VAX_0_1 = ChanceNode(name='VAX_0_1', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_65*D.VAX_HOSP_MULT*rr_pax_vax,
                                                                       1-(D.HOSP_NOCOMORB_65*D.VAX_HOSP_MULT*rr_pax_vax)], cost=D.PAXLOVID_COST, health_utility=0)
    UNVAX_0_1 = ChanceNode(name='UNVAX_0_1', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_65*rr_pax_unvax,
                                                                           1-(D.HOSP_NOCOMORB_65*rr_pax_unvax)], cost=D.PAXLOVID_COST, health_utility=0)
    COMORB_0 = ChanceNode(name='COMORB_0', future_nodes=[VAX_0_0, UNVAX_0_0], probs=[D.VAX_OVER_65, 1-D.VAX_OVER_65], cost=0, health_utility=0)
    NO_COMORB_0 = ChanceNode(name='COMORB_1', future_nodes=[VAX_0_1, UNVAX_0_1], probs=[D.VAX_OVER_65, 1-D.VAX_OVER_65], cost=0, health_utility=0)
    AGE_OVER_0 = ChanceNode(name='OVER_65_0', future_nodes=[COMORB_0, NO_COMORB_0], probs=[D.HR_65_COMORB, 1-D.HR_65_COMORB], cost=0, health_utility=0)

    VAX_0 = ChanceNode(name='VAX_0', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65*D.VAX_HOSP_MULT*rr_pax_vax,
                                                                   1-(D.HOSP_COMORB_UNDER65*D.VAX_HOSP_MULT*rr_pax_vax)], cost=D.PAXLOVID_COST, health_utility=0)
    UNVAX_0 = ChanceNode(name='UNVAX_0', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65*rr_pax_unvax,
                                                                       1-(D.HOSP_COMORB_UNDER65*rr_pax_unvax)], cost=D.PAXLOVID_COST, health_utility=0)
    AGE_UNDER_0 = ChanceNode(name='UNDER_65_0', future_nodes=[VAX_0, UNVAX_0], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)

    HR_0 = ChanceNode(name='HR_0', future_nodes=[AGE_OVER_0, AGE_UNDER_0], probs=[D.HR_65, 1-D.HR_65], cost=0, health_utility=0)

    VAX_LR_0 = ChanceNode(name='VAX_LR_0', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65*D.VAX_HOSP_MULT, 1-(D.HOSP_NOCOMORB_UNDER65*D.VAX_HOSP_MULT)], cost=0, health_utility=0)
    UNVAX_LR_0 = ChanceNode(name='UNVAX_LR_0', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65, 1-D.HOSP_NOCOMORB_UNDER65], cost=0, health_utility=0)
    LR_0 = ChanceNode('LR_0', future_nodes=[VAX_LR_0, UNVAX_LR_0], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    C0 = ChanceNode(name='C0', future_nodes=[HR_0, LR_0], probs=[D.HR, 1-D.HR], cost=0, health_utility=0)
    # ------------------------------------------------#

    VAX_1_0 = ChanceNode(name='VAX_1_0', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_65*D.VAX_HOSP_MULT,
                                                                       1-D.HOSP_COMORB_65*D.VAX_HOSP_MULT], cost=0, health_utility=0)
    UNVAX_1_0 = ChanceNode(name='UNVAX_1_0', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_65*relative_risk_unvax,
                                                                           1-D.HOSP_COMORB_65*relative_risk_unvax], cost=drug_cost, health_utility=0)
    COMORB_1 = ChanceNode(name='COMORB_1', future_nodes=[VAX_1_0, UNVAX_1_0], probs=[D.VAX_OVER_65, 1-D.VAX_OVER_65], cost=0, health_utility=0)

    VAX_1_1 = ChanceNode(name='VAX_1_1', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_65*D.VAX_HOSP_MULT,
                                                                       1-D.HOSP_NOCOMORB_65*D.VAX_HOSP_MULT], cost=0, health_utility=0)
    UNVAX_1_1 = ChanceNode(name='UNVAX_1_1', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_65*relative_risk_unvax,
                                                                           1-D.HOSP_NOCOMORB_65*relative_risk_unvax], cost=drug_cost, health_utility=0)
    NO_COMORB_1 = ChanceNode(name='NO_COMORB_1', future_nodes=[VAX_1_1, UNVAX_1_1], probs=[D.VAX_OVER_65, 1-D.VAX_OVER_65], cost=0, health_utility=0)
    AGE_OVER_1 = ChanceNode(name='OVER_65_1', future_nodes=[COMORB_1, NO_COMORB_1], probs=[D.HR_65_COMORB, 1-D.HR_65_COMORB], cost=0, health_utility=0)

    VAX_1 = ChanceNode(name='VAX_1', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65, 1-D.HOSP_COMORB_UNDER65], cost=0, health_utility=0)
    UNVAX_1 = ChanceNode(name='UNVAX_1', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65*relative_risk_unvax,
                                                                       1-D.HOSP_COMORB_UNDER65*relative_risk_unvax], cost=drug_cost, health_utility=0)
    AGE_UNDER_1 = ChanceNode(name='UNDER_65_1', future_nodes=[VAX_1, UNVAX_1], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    HR_1 = ChanceNode('HR_1', future_nodes=[AGE_OVER_1, AGE_UNDER_1], probs=[D.HR_65, 1-D.HR_65], cost=0, health_utility=0)

    VAX_LR_1 = ChanceNode(name='VAX_LR_1', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65 * D.VAX_HOSP_MULT,
                                                                         1 - (D.HOSP_NOCOMORB_UNDER65 * D.VAX_HOSP_MULT)], cost=0, health_utility=0)
    UNVAX_LR_1 = ChanceNode(name='UNVAX_LR_1', future_nodes=[T1, T2],
                            probs=[D.HOSP_NOCOMORB_UNDER65, 1 - D.HOSP_NOCOMORB_UNDER65], cost=0, health_utility=0)
    LR_1 = ChanceNode('LR_1', future_nodes=[VAX_LR_1, UNVAX_LR_1], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    C1 = ChanceNode('C1', 0, [HR_1, LR_1], [D.HR, 1-D.HR], health_utility=0)  # high risk and un-vaccinated

    # ----------------------------------------------

    VAX_2_0 = ChanceNode('VAX_2_0', drug_cost, [T1, T2], [D.HOSP_COMORB_65*D.VAX_HOSP_MULT*relative_risk_vax,
                                                  1-D.HOSP_COMORB_65*D.VAX_HOSP_MULT*relative_risk_vax], 0)
    UNVAX_2_0 = ChanceNode('UNVAX_2_0', drug_cost, [T1, T2], [D.HOSP_COMORB_65*relative_risk_unvax, 1-D.HOSP_COMORB_65*relative_risk_unvax], 0)
    VAX_2_1 = ChanceNode('VAX_2_1', drug_cost, [T1, T2], [D.HOSP_NOCOMORB_65*D.VAX_HOSP_MULT*relative_risk_vax,
                                                          1-D.HOSP_NOCOMORB_65*D.VAX_HOSP_MULT*relative_risk_vax], 0)
    UNVAX_2_1 = ChanceNode('UNVAX_2_1', drug_cost, [T1, T2], [D.HOSP_NOCOMORB_65*relative_risk_unvax, 1-D.HOSP_NOCOMORB_65*relative_risk_unvax], 0)
    COMORB_2 = ChanceNode(name='COMORB_2', future_nodes=[VAX_2_0, UNVAX_2_0], probs=[D.VAX_OVER_65, 1-D.VAX_OVER_65], cost=0, health_utility=0)
    NO_COMORB_2 = ChanceNode(name='NO_COMORB_2', future_nodes=[VAX_2_1, UNVAX_2_1], probs=[D.VAX_OVER_65, 1-D.VAX_OVER_65], cost=0, health_utility=0)
    AGE_OVER_2 = ChanceNode(name='AGE_OVER_2', future_nodes=[COMORB_2, NO_COMORB_2], probs=[D.HR_65_COMORB, 1-D.HR_65_COMORB], cost=0, health_utility=0)
    VAX_2 = ChanceNode(name='VAX_2', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65*relative_risk_vax*D.VAX_HOSP_MULT,
                                                                   1-D.HOSP_COMORB_UNDER65*relative_risk_vax*D.VAX_HOSP_MULT], cost=drug_cost, health_utility=0)
    UNVAX_2 = ChanceNode(name='UNVAX_2', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65*relative_risk_unvax,
                                                                       1-D.HOSP_COMORB_UNDER65*relative_risk_unvax], cost=drug_cost, health_utility=0)
    AGE_UNDER_2 = ChanceNode(name='AGE_UNDER_2', future_nodes=[VAX_2, UNVAX_2], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    HR_2 = ChanceNode(name='HR_2', future_nodes=[AGE_OVER_2, AGE_UNDER_2], probs=[D.HR_65, 1-D.HR_65], cost=0, health_utility=0)

    VAX_LR_2 = ChanceNode(name='VAX_LR_2', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65 * D.VAX_HOSP_MULT,
                                                                         1 - (D.HOSP_NOCOMORB_UNDER65 * D.VAX_HOSP_MULT)], cost=0, health_utility=0)
    UNVAX_LR_2 = ChanceNode(name='UNVAX_LR_2', future_nodes=[T1, T2],
                            probs=[D.HOSP_NOCOMORB_UNDER65, 1 - D.HOSP_NOCOMORB_UNDER65], cost=0, health_utility=0)
    LR_2 = ChanceNode(name='LR_2', future_nodes=[VAX_LR_2, UNVAX_LR_2], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    C2 = ChanceNode('C2', 0, [HR_2, LR_2], [D.HR, 1-D.HR], 0)  # all high risk

    # ------------------- #

    VAX_3_0 = ChanceNode('VAX_2_0', drug_cost, [T1, T2], [D.HOSP_COMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax,
                                                          1 - D.HOSP_COMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax],
                         0)
    UNVAX_3_0 = ChanceNode('UNVAX_2_0', drug_cost, [T1, T2],
                           [D.HOSP_COMORB_65 * relative_risk_unvax, 1 - D.HOSP_COMORB_65 * relative_risk_unvax], 0)
    VAX_3_1 = ChanceNode('VAX_3_1', drug_cost, [T1, T2], [D.HOSP_NOCOMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax,
                                                          1 - D.HOSP_NOCOMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax],
                         0)
    UNVAX_3_1 = ChanceNode('UNVAX_3_1', drug_cost, [T1, T2],
                           [D.HOSP_NOCOMORB_65 * relative_risk_unvax, 1 - D.HOSP_NOCOMORB_65 * relative_risk_unvax], 0)
    COMORB_3 = ChanceNode(name='COMORB_3', future_nodes=[VAX_3_0, UNVAX_3_0], probs=[D.VAX_OVER_65, 1 - D.VAX_OVER_65],
                          cost=0, health_utility=0)
    NO_COMORB_3 = ChanceNode(name='NO_COMORB_3', future_nodes=[VAX_3_1, UNVAX_3_1],
                             probs=[D.VAX_OVER_65, 1 - D.VAX_OVER_65], cost=0, health_utility=0)
    AGE_OVER_3 = ChanceNode(name='AGE_OVER_3', future_nodes=[COMORB_3, NO_COMORB_3],
                            probs=[D.HR_65_COMORB, 1 - D.HR_65_COMORB], cost=0, health_utility=0)
    VAX_3 = ChanceNode(name='VAX_3', future_nodes=[T1, T2],
                       probs=[D.HOSP_COMORB_UNDER65 * relative_risk_vax * D.VAX_HOSP_MULT,
                              1 - D.HOSP_COMORB_UNDER65 * relative_risk_vax * D.VAX_HOSP_MULT], cost=drug_cost,
                       health_utility=0)
    UNVAX_3 = ChanceNode(name='UNVAX_3', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65 * relative_risk_unvax,
                                                                       1 - D.HOSP_COMORB_UNDER65 * relative_risk_unvax],
                         cost=drug_cost, health_utility=0)
    AGE_UNDER_3 = ChanceNode(name='AGE_UNDER_3', future_nodes=[VAX_3, UNVAX_3],
                             probs=[D.VAX_UNDER_65, 1 - D.VAX_UNDER_65], cost=0, health_utility=0)
    HR_3 = ChanceNode(name='HR_3', future_nodes=[AGE_OVER_3, AGE_UNDER_3], probs=[D.HR_65, 1-D.HR_65], cost=0, health_utility=0)
    VAX_LR_3 = ChanceNode(name='VAX_LR_3', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65 * D.VAX_HOSP_MULT,
                                                                         1 - (D.HOSP_NOCOMORB_UNDER65 * D.VAX_HOSP_MULT)],cost=0, health_utility=0)
    UNVAX_LR_3 = ChanceNode(name='UNVAX_LR_3', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65*relative_risk_unvax,
                                                                             1-D.HOSP_NOCOMORB_UNDER65*relative_risk_unvax], cost=drug_cost, health_utility=0)
    LR_3 = ChanceNode(name='LR_3', future_nodes=[VAX_LR_3, UNVAX_LR_3], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    C3 = ChanceNode('C3', 0, [HR_3, LR_3], [D.HR, 1-D.HR], 0)  # high risk + low risk and un-vaccinated

    # ---------------------------------- #
    VAX_4_0 = ChanceNode('VAX_4_0', drug_cost, [T1, T2], [D.HOSP_COMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax,
                                                          1 - D.HOSP_COMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax],
                         0)
    UNVAX_4_0 = ChanceNode('UNVAX_4_0', drug_cost, [T1, T2],
                           [D.HOSP_COMORB_65 * relative_risk_unvax, 1 - D.HOSP_COMORB_65 * relative_risk_unvax], 0)
    VAX_4_1 = ChanceNode('VAX_4_1', drug_cost, [T1, T2], [D.HOSP_NOCOMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax,
                                                          1 - D.HOSP_NOCOMORB_65 * D.VAX_HOSP_MULT * relative_risk_vax], 0)
    UNVAX_4_1 = ChanceNode('UNVAX_4_1', drug_cost, [T1, T2],
                           [D.HOSP_NOCOMORB_65 * relative_risk_unvax, 1 - D.HOSP_NOCOMORB_65 * relative_risk_unvax], 0)
    COMORB_4 = ChanceNode(name='COMORB_4', future_nodes=[VAX_4_0, UNVAX_4_0], probs=[D.VAX_OVER_65, 1 - D.VAX_OVER_65],
                          cost=0, health_utility=0)
    NO_COMORB_4 = ChanceNode(name='NO_COMORB_4', future_nodes=[VAX_4_1, UNVAX_4_1],
                             probs=[D.VAX_OVER_65, 1 - D.VAX_OVER_65], cost=0, health_utility=0)
    AGE_OVER_4 = ChanceNode(name='AGE_OVER_4', future_nodes=[COMORB_4, NO_COMORB_4],
                            probs=[D.HR_65_COMORB, 1 - D.HR_65_COMORB], cost=0, health_utility=0)
    VAX_4 = ChanceNode(name='VAX_4', future_nodes=[T1, T2],
                       probs=[D.HOSP_COMORB_UNDER65 * relative_risk_vax * D.VAX_HOSP_MULT,
                              1 - D.HOSP_COMORB_UNDER65 * relative_risk_vax * D.VAX_HOSP_MULT], cost=drug_cost,
                       health_utility=0)
    UNVAX_4 = ChanceNode(name='UNVAX_4', future_nodes=[T1, T2], probs=[D.HOSP_COMORB_UNDER65 * relative_risk_unvax,
                                                                       1 - D.HOSP_COMORB_UNDER65 * relative_risk_unvax],
                         cost=drug_cost, health_utility=0)
    AGE_UNDER_4 = ChanceNode(name='AGE_UNDER_4', future_nodes=[VAX_4, UNVAX_4],
                             probs=[D.VAX_UNDER_65, 1 - D.VAX_UNDER_65], cost=0, health_utility=0)
    HR_4 = ChanceNode(name='HR_4', future_nodes=[AGE_OVER_4, AGE_UNDER_4], probs=[D.HR_65, 1 - D.HR_65], cost=0,
                      health_utility=0)
    VAX_LR_4 = ChanceNode(name='VAX_LR_4', future_nodes=[T1, T2], probs=[D.HOSP_NOCOMORB_UNDER65*relative_risk_vax*D.VAX_HOSP_MULT,
                                                                         1-D.HOSP_NOCOMORB_UNDER65*relative_risk_vax*D.VAX_HOSP_MULT], cost=drug_cost, health_utility=0)
    UNVAX_LR_4 = ChanceNode(name='UNVAX_LR_4', future_nodes=[T1, T2],
                            probs=[D.HOSP_NOCOMORB_UNDER65 * relative_risk_unvax,
                                   1 - D.HOSP_NOCOMORB_UNDER65 * relative_risk_unvax], cost=drug_cost, health_utility=0)
    LR_4 = ChanceNode(name='LR_4', future_nodes=[VAX_LR_4, UNVAX_LR_4], probs=[D.VAX_UNDER_65, 1-D.VAX_UNDER_65], cost=0, health_utility=0)
    C4 = ChanceNode(name='C4', cost=0, future_nodes=[HR_4, LR_4], probs=[D.HR, 1-D.HR], health_utility=0)  # all people

    # create Decision Nodes for each allocation strategy
    D0 = DecisionNode('D0', 0, [C0, C1, C2, C3, C4], 0)

    exp_cost = D0.get_expected_cost()
    exp_health_utility = D0.get_expected_health_utility()
    incr_cost_eff_ratio = [exp_cost['C0'], exp_cost['C1'], exp_cost['C2'],
    exp_cost['C3'], exp_cost['C4'], exp_health_utility['C0'], exp_health_utility['C1'],
    exp_health_utility['C2'], exp_health_utility['C3'], exp_health_utility['C4']]

    return incr_cost_eff_ratio

