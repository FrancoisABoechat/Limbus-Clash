import math
import itertools

class ClashOld:
    def __init__(self, cl1, cl2):
        self.cl1_bp = cl1[0]
        self.cl1_cp = cl1[1]
        self.cl1_ca = cl1[2]
        self.cl1_sa = cl1[3]
        self.cl1_lv = cl1[4]
        self.cl2_bp = cl2[0]
        self.cl2_cp = cl2[1]
        self.cl2_ca = cl2[2]
        self.cl2_sa = cl2[3]
        self.cl2_lv = cl2[4]

    def Clash_old(self):
        """
        cl1, cl2 (list): contains values in the following order - base power, coin power, number of coins, sanity and level.
        calculates the odds for clasher 1 to win the clash in one round of clash, following iterations notwithstanding.
        """
        winrate = 0
        winrate_tie = 0
        power_diff = int((self.cl1_lv - self.cl2_lv)/3)
        modifier_cl1 = ((50+self.cl1_sa)/100)
        modifier_cl2 = ((50+self.cl2_sa)/100)
        for coin1 in range(0,self.cl1_ca+1):
            for coin2 in range(0,self.cl2_ca+1):
                odds_cl1 = ((modifier_cl1**(coin1)) * (1-modifier_cl1)**(self.cl1_ca-coin1)) * math.comb(self.cl1_ca,coin1)
                odds_cl2 = ((modifier_cl2**(coin2)) * (1-modifier_cl2)**(self.cl2_ca-coin2)) * math.comb(self.cl2_ca,coin2)
                total_chance = odds_cl1 * odds_cl2
                value_cl1 = self.cl1_bp + self.cl1_cp*coin1 + power_diff
                value_cl2 = self.cl2_bp + self.cl2_cp*coin2
                if value_cl1 > value_cl2:
                    winrate += total_chance
                elif value_cl1 == value_cl2:
                    winrate_tie += total_chance
        winrate = winrate/(1-winrate_tie)
        return round(winrate,2)

    @staticmethod
    def _winrate_text(winrate):
        """
        Winrate text is defined as folow:
            0-10 hopeless
            10-40 strugling
            40-60 neutral
            60-90 favored
            90-100 dominating
        """
        if winrate < 0.1:
            text = "Hopeless"
        elif winrate >= 0.1 and winrate < 0.4:
            text = "Strugling"
        elif winrate >= 0.4 and winrate < 0.6:
            text = "Neutral"
        elif winrate >= 0.6 and winrate < 0.9:
            text = "Favored"
        else:
            text = "Dominating"
        return text

class ClashNew:
    def __init__(self, cl1, cl2):
        print(cl1)
        print(cl2)
        self.cl1_bp = cl1[0]
        self.cl1_cp = cl1[1]
        self.cl1_ca = cl1[2]
        self.cl1_sa = cl1[3]
        self.cl1_lv = cl1[4]
        self.cl2_bp = cl2[0]
        self.cl2_cp = cl2[1]
        self.cl2_ca = cl2[2]
        self.cl2_sa = cl2[3]
        self.cl2_lv = cl2[4]

    def Clash_old(self):
        """
        cl1, cl2 (list): contains values in the following order - base power, coin power, number of coins, sanity and level.
        calculates the odds for clasher 1 to win the clash in one round of clash, following iterations notwithstanding.
        """
        winrate = 0
        winrate_tie = 0
        power_diff = int((self.cl1_lv - self.cl2_lv)/3)
        modifier_cl1 = ((50+self.cl1_sa)/100)
        modifier_cl2 = ((50+self.cl2_sa)/100)
        for coin1 in range(0,self.cl1_ca+1):
            for coin2 in range(0,self.cl2_ca+1):
                odds_cl1 = ((modifier_cl1**(coin1)) * (1-modifier_cl1)**(self.cl1_ca-coin1)) * math.comb(self.cl1_ca,coin1)
                odds_cl2 = ((modifier_cl2**(coin2)) * (1-modifier_cl2)**(self.cl2_ca-coin2)) * math.comb(self.cl2_ca,coin2)
                total_chance = odds_cl1 * odds_cl2
                value_cl1 = self.cl1_bp + self.cl1_cp*coin1 + power_diff
                value_cl2 = self.cl2_bp + self.cl2_cp*coin2
                if value_cl1 > value_cl2:
                    winrate += total_chance
                elif value_cl1 == value_cl2:
                    winrate_tie += total_chance
        winrate = winrate/(1-winrate_tie)
        return round(winrate,2)

    def Clash_new(self):
        """
        cl1, cl2 (list): contains values in the following order - base power, coin power, number of coins, sanity and level.
        Using the old clash system to calculate the probabilities with each permutation of coins between clashers, creates a
        binary tree containing each clash children and odds for transitioning to left child, clasher 1 wins
        """
        winrate = 0
        permutations = list(itertools.product(list(reversed(range(1,self.cl1_ca+1))),list(reversed(range(1,self.cl2_ca+1)))))
        original_coins_cl1 = self.cl1_ca
        original_coins_cl2 = self.cl2_ca
        winrates = {}
        for permutation in permutations:
            self.cl1_ca = permutation[0]
            self.cl2_ca = permutation[1]
            temp_winrate = self.Clash_old()
            if permutation[0]-1 and permutation[1]-1:
                winrates.update({permutation: [temp_winrate, [(permutation[0],permutation[1]-1), (permutation[0]-1,permutation[1])]]})
            elif permutation[0]-1:
                winrates.update({permutation: [temp_winrate, [(permutation[0],permutation[1]-1), (permutation[0]-1,permutation[1])]]})
            elif permutation[1]-1:
                winrates.update({permutation: [temp_winrate, [(permutation[0],permutation[1]-1), (permutation[0]-1,permutation[1])]]})
            else:
                winrates.update({permutation: [temp_winrate, [(0,0)]]})
        winrate = self.recursive_tree(winrates, winrate, original_coins_cl1, original_coins_cl2)
        return round(winrate,2)

    def recursive_tree(self, tree, total, c1, c2):
        """
        Construct the recursive probabilities formula in a recursive manner using a binary tree.
        As an example, starting from the first node, we have winrate = W1 * L + W2 * R, where L and R are the
        winning and losing tree child tree respectively.
        if c2 is 0, which means clasher 2 has run out of coins, then we multiply the curent path by 1.
        if c1 has only one coin left, we only add one child as winrate = W1 * L, as we do not concern
        ourselves with calculating losing probabilities.
        Ex: Consider a clash between two skills with 2 coins each, the equation would develop as follow:
            winrate = W1 * L + W2 * R
            winrate = W1 * (W3 * L + W4 * R) + W2 * R
            winrate = W1 * (W3 * 1 + W4 * W6) + W2 * R
            winrate = W1 * (W3 + W4 * W6 * L) + W2 * R
            winrate = W1 * (W3 + W4 * W6) + W2 * R
            winrate = W1 * (W3 + W4 * W6) + W2 * (W5 * L)
            winrate = W1 * (W3 + W4 * W6) + W2 * W5 * (W7 * L)
            winrate = W1 * (W3 + W4 * W6) + W2 * W5 * W7
        """
        if c2 == 0:
            winrate = 1
        elif c1 == 1:
            winrate = tree.get((c1,c2))[0] * self.recursive_tree(tree, total, c1, c2-1)
        else:
            winrate = (
            tree.get((c1,c2))[0] * self.recursive_tree(tree, total, c1, c2-1)
            + (1-tree.get((c1,c2))[0]) * self.recursive_tree(tree, total, c1-1, c2)
            )
        return winrate

    @staticmethod
    def _winrate_text(winrate):
        """
        Winrate text is defined as folow:
            0-10 hopeless
            10-40 strugling
            40-60 neutral
            60-90 favored
            90-100 dominating
        """
        if winrate < 0.1:
            text = "Hopeless"
        elif winrate >= 0.1 and winrate < 0.4:
            text = "Strugling"
        elif winrate >= 0.4 and winrate < 0.6:
            text = "Neutral"
        elif winrate >= 0.6 and winrate < 0.9:
            text = "Favored"
        else:
            text = "Dominating"
        return text