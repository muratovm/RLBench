import random


# maximum steps in the pattern
steps_max = 6
# minimum steps in the pattern
steps_min = 3
# maximum amount of steps until reassessment of effectiveness of current memory patterns
max_steps_until_memory_reassessment = random.randint(80, 120)


# current memory of the agent
current_memory = []
# list of 1, 0 and -1 representing win, tie and lost results of the game respectively
# length is max_steps_until_memory_r_t
results = []
# current best sum of results
best_sum_of_results = 0
# memory length of patterns in first group
# steps_max is multiplied by 2 to consider both my_agent's and opponent's actions
group_memory_length = steps_max * 2
# list of groups of memory patterns
groups_of_memory_patterns = []
for i in range(steps_max, steps_min - 1, -1):
    groups_of_memory_patterns.append({
        # how many steps in a row are in the pattern
        "memory_length": group_memory_length,
        # list of memory patterns
        "memory_patterns": []
    })
    group_memory_length -= 2

    
def find_pattern(memory_patterns, memory, memory_length):
    """ find appropriate pattern in memory """
    for pattern in memory_patterns:
        actions_matched = 0
        for i in range(memory_length):
            if pattern["actions"][i] == memory[i]:
                actions_matched += 1
            else:
                break
        # if memory fits this pattern
        if actions_matched == memory_length:
            return pattern
    # appropriate pattern not found
    return None

def get_step_result_for_my_agent(my_agent_action, opp_action):
    """ 
        get result of the step for my_agent
        1, 0 and -1 representing win, tie and lost results of the game respectively
    """
    if my_agent_action == opp_action:
        return 0
    elif (my_agent_action == (opp_action + 1)) or (my_agent_action == 0 and opp_action == 2):
        return 1
    else:
        return -1


def my_agent(obs, conf):
    """ your ad here """
    global results
    global best_sum_of_results
    # action of my_agent
    my_action = None
    # if it's not first step, add opponent's last action to agent's current memory
    # and reassess effectiveness of current memory patterns
    if obs["step"] > 0:
        current_memory.append(obs["lastOpponentAction"])
        # previous step won or lost
        results.append(get_step_result_for_my_agent(current_memory[-2], current_memory[-1]))
        # if there is enough steps added to results for memery reassessment
        if len(results) == max_steps_until_memory_reassessment:
            results_sum = sum(results)
            # if effectiveness of current memory patterns has decreased significantly
            if results_sum < (best_sum_of_results * 0.5):
                # flush all current memory patterns
                best_sum_of_results = 0
                results = []
                for group in groups_of_memory_patterns:
                    group["memory_patterns"] = []
            else:
                # if effectiveness of current memory patterns has increased
                if results_sum > best_sum_of_results:
                    best_sum_of_results = results_sum
                del results[:1]
    for group in groups_of_memory_patterns:
        # if length of current memory is bigger than necessary for a new memory pattern
        if len(current_memory) > group["memory_length"]:
            # get momory of the previous step
            previous_step_memory = current_memory[:group["memory_length"]]
            previous_pattern = find_pattern(group["memory_patterns"], previous_step_memory, group["memory_length"])
            if previous_pattern == None:
                previous_pattern = {
                    "actions": previous_step_memory.copy(),
                    "opp_next_actions": [
                        {"action": 0, "amount": 0, "response": 1},
                        {"action": 1, "amount": 0, "response": 2},
                        {"action": 2, "amount": 0, "response": 0}
                    ]
                }
                group["memory_patterns"].append(previous_pattern)
            # if such pattern already exists
            for action in previous_pattern["opp_next_actions"]:
                if action["action"] == obs["lastOpponentAction"]:
                    action["amount"] += 1
            # delete first two elements in current memory (actions of the oldest step in current memory)
            del current_memory[:2]
            # if action was not yet found
            if my_action == None:
                pattern = find_pattern(group["memory_patterns"], current_memory, group["memory_length"])
                # if appropriate pattern is found
                if pattern != None:
                    my_action_amount = 0
                    for action in pattern["opp_next_actions"]:
                        # if this opponent's action occurred more times than currently chosen action
                        # or, if it occured the same amount of times and this one is choosen randomly among them
                        if (action["amount"] > my_action_amount or
                                (action["amount"] == my_action_amount and random.random() > 0.5)):
                            my_action_amount = action["amount"]
                            my_action = action["response"]
    # if no action was found
    if my_action == None:
        my_action = random.randint(0, 2)
    current_memory.append(my_action)
    return my_action
%%writefile black_belt/iocane_powder.py

import random


def recall(age, hist):
    """Looking at the last 'age' points in 'hist', finds the
    last point with the longest similarity to the current point,
    returning 0 if none found."""
    end, length = 0, 0
    for past in range(1, min(age + 1, len(hist) - 1)):
        if length >= len(hist) - past: break
        for i in range(-1 - length, 0):
            if hist[i - past] != hist[i]: break
        else:
            for length in range(length + 1, len(hist) - past):
                if hist[-past - length - 1] != hist[-length - 1]: break
            else: length += 1
            end = len(hist) - past
    return end

def beat(i):
    return (i + 1) % 3
def loseto(i):
    return (i - 1) % 3

class Stats:
    """Maintains three running counts and returns the highest count based
         on any given time horizon and threshold."""
    def __init__(self):
        self.sum = [[0, 0, 0]]
    def add(self, move, score):
        self.sum[-1][move] += score
    def advance(self):
        self.sum.append(self.sum[-1])
    def max(self, age, default, score):
        if age >= len(self.sum): diff = self.sum[-1]
        else: diff = [self.sum[-1][i] - self.sum[-1 - age][i] for i in range(3)]
        m = max(diff)
        if m > score: return diff.index(m), m
        return default, score

class Predictor:
    """The basic iocaine second- and triple-guesser.    Maintains stats on the
         past benefits of trusting or second- or triple-guessing a given strategy,
         and returns the prediction of that strategy (or the second- or triple-
         guess) if past stats are deviating from zero farther than the supplied
         "best" guess so far."""
    def __init__(self):
        self.stats = Stats()
        self.lastguess = -1
    def addguess(self, lastmove, guess):
        if lastmove != -1:
            diff = (lastmove - self.prediction) % 3
            self.stats.add(beat(diff), 1)
            self.stats.add(loseto(diff), -1)
            self.stats.advance()
        self.prediction = guess
    def bestguess(self, age, best):
        bestdiff = self.stats.max(age, (best[0] - self.prediction) % 3, best[1])
        return (bestdiff[0] + self.prediction) % 3, bestdiff[1]

ages = [1000, 100, 10, 5, 2, 1]

class Iocaine:

    def __init__(self):
        """Build second-guessers for 50 strategies: 36 history-based strategies,
             12 simple frequency-based strategies, the constant-move strategy, and
             the basic random-number-generator strategy.    Also build 6 meta second
             guessers to evaluate 6 different time horizons on which to score
             the 50 strategies' second-guesses."""
        self.predictors = []
        self.predict_history = self.predictor((len(ages), 2, 3))
        self.predict_frequency = self.predictor((len(ages), 2))
        self.predict_fixed = self.predictor()
        self.predict_random = self.predictor()
        self.predict_meta = [Predictor() for a in range(len(ages))]
        self.stats = [Stats() for i in range(2)]
        self.histories = [[], [], []]

    def predictor(self, dims=None):
        """Returns a nested array of predictor objects, of the given dimensions."""
        if dims: return [self.predictor(dims[1:]) for i in range(dims[0])]
        self.predictors.append(Predictor())
        return self.predictors[-1]

    def move(self, them):
        """The main iocaine "move" function."""

        # histories[0] stores our moves (last one already previously decided);
        # histories[1] stores their moves (last one just now being supplied to us);
        # histories[2] stores pairs of our and their last moves.
        # stats[0] and stats[1] are running counters our recent moves and theirs.
        if them != -1:
            self.histories[1].append(them)
            self.histories[2].append((self.histories[0][-1], them))
            for watch in range(2):
                self.stats[watch].add(self.histories[watch][-1], 1)

        # Execute the basic RNG strategy and the fixed-move strategy.
        rand = random.randrange(3)
        self.predict_random.addguess(them, rand)
        self.predict_fixed.addguess(them, 0)

        # Execute the history and frequency stratgies.
        for a, age in enumerate(ages):
            # For each time window, there are three ways to recall a similar time:
            # (0) by history of my moves; (1) their moves; or (2) pairs of moves.
            # Set "best" to these three timeframes (zero if no matching time).
            best = [recall(age, hist) for hist in self.histories]
            for mimic in range(2):
                # For each similar historical moment, there are two ways to anticipate
                # the future: by mimicing what their move was; or mimicing what my
                # move was.    If there were no similar moments, just move randomly.
                for watch, when in enumerate(best):
                    if not when: move = rand
                    else: move = self.histories[mimic][when]
                    self.predict_history[a][mimic][watch].addguess(them, move)
                # Also we can anticipate the future by expecting it to be the same
                # as the most frequent past (either counting their moves or my moves).
                mostfreq, score = self.stats[mimic].max(age, rand, -1)
                self.predict_frequency[a][mimic].addguess(them, mostfreq)

        # All the predictors have been updated, but we have not yet scored them
        # and chosen a winner for this round.    There are several timeframes
        # on which we can score second-guessing, and we don't know timeframe will
        # do best.    So score all 50 predictors on all 6 timeframes, and record
        # the best 6 predictions in meta predictors, one for each timeframe.
        for meta, age in enumerate(ages):
            best = (-1, -1)
            for predictor in self.predictors:
                best = predictor.bestguess(age, best)
            self.predict_meta[meta].addguess(them, best[0])

        # Finally choose the best meta prediction from the final six, scoring
        # these against each other on the whole-game timeframe. 
        best = (-1, -1)
        for meta in range(len(ages)):
            best = self.predict_meta[meta].bestguess(len(self.histories[0]) , best) 

        # We've picked a next move.    Record our move in histories[0] for next time.
        self.histories[0].append(best[0])

        # And return it.
        return best[0]

iocaine = None

def iocaine_agent(observation, configuration):
    global iocaine
    if observation.step == 0:
        iocaine = Iocaine()
        act = iocaine.move(-1)
    else:
        act = iocaine.move(observation.lastOpponentAction)
        
    return act
