import numpy as np
from GridWorld import GridWorld


class RLAlgorithm:
    def __init__(self, env: GridWorld, gamma=0.9, seed=42):
        self.env = env
        self.gamma = gamma
        self.rng = np.random.RandomState(seed)
        self.reset()

    def reset(self):
        self.values = np.zeros((self.env.n_states))
        # Stochastic policy
        self.policy = np.full((self.env.n_states, len(self.env.actions)), 1.0 / len(self.env.actions))
        self.q_values = np.zeros((self.env.n_states, len(self.env.actions)))

    def set_seed(self, seed):
        """Reset the random number generator with a new seed."""
        self.rng = np.random.RandomState(seed)

    def __str__(self) -> str:
        raise NotImplementedError

    def move_agent(self, action):
        """Move the agent according to the current policy."""
        return self.env.move_agent(action)

    def reset_agent(self):
        """Reset the agent to the initial state."""
        self.env.reset_agent()

    def select_action(self, state):
        raise NotImplementedError

    def select_policy_action(self, state):
        return self.rng.choice(self.env.actions, p=self.policy[state])

    def select_greedy_action(self, state):
        return np.argmax(self.policy[state])


class GeneralizedPolicyIteration(RLAlgorithm):
    def __init__(self, env, gamma=0.9, seed=42):
        super().__init__(env, gamma, seed)
        self.policy_stable = False

    def policy_evaluation_step(self, theta=1e-6):
        """Single step of policy evaluation."""
        raise NotImplementedError

    def policy_improvement_step(self):
        """Single step of policy improvement."""
        raise NotImplementedError

    def greedy_policy_improvement(self):
        is_policy_converged = True
        for s in range(self.env.n_states):
            if s in self.env.terminal_states:
                continue

            old_policy = self.policy[s].copy()

            for a in self.env.actions:
                self.policy[s, a] = 0
            best_action = np.argmax(self.q_values[s])
            self.policy[s, best_action] = 1

            if not np.array_equal(old_policy, self.policy[s]):
                is_policy_converged = False

        return is_policy_converged

    def step(self):
        """Single step of generalized policy iteration."""
        self.policy_evaluation_step()
        self.policy_stable = self.policy_improvement_step()

    def run(self, max_steps=1000):
        """Run generalized policy iteration until convergence or max_steps."""
        for i in range(max_steps):
            self.step()
            if self.policy_stable:
                break


class PolicyIteration(GeneralizedPolicyIteration):
    def policy_evaluation_step(self):
        """Single step of policy evaluation."""

        delta = 0
        old_values = self.values.copy()
        for s in range(self.env.n_states):
            if s in self.env.terminal_states or s in self.env.walls:
                continue

            v = 0
            for a in self.env.actions:
                q = 0
                for s_prime in self.env.get_possible_successors(s, a):
                    q += self.env.transition_probs[s, a, s_prime] * \
                        (self.env.rewards[s_prime] + self.gamma * old_values[s_prime])

                    # Debugging
                    # if s_prime == s:
                    #     print(
                    #         f"State: {self.env.state_to_index(s)}, Action: {a}, Successor: {self.env.state_to_index(s_prime)}, Reward: {self.env.rewards[s_prime]}, Value: {old_values[s_prime]}")

                self.q_values[s, a] = q
                v += self.policy[s, a] * q

            self.values[s] = v
            delta = max(delta, np.abs(old_values[s] - self.values[s]))

        return delta

    def policy_improvement_step(self):
        """Single step of policy improvement."""
        return self.greedy_policy_improvement()

    def __str__(self) -> str:
        return "Policy Iteration"

    def select_action(self, state):
        return self.select_policy_action(state)
