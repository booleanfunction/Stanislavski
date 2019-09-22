import gym
import gym_pow
import numpy as np
import time, pickle, os
import matplotlib.pyplot as plt

env = gym.make('pow-v0')# Change to 40% hashpower

epsilon = 0.5
total_episodes = 50000
lr_rate = 0.4
gamma = 1

Q = np.zeros((100, env.action_space.n))
print(Q)

    
def choose_action(state):
    action=0
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state[1], :])
    return action

def choose_random_action():
    action = env.action_space.sample()
    return action
def choose_honest_action():
    return 0

def learn(state, state2, reward, action):
    predict = Q[state[1], action]
    print("predicted value", predict)
    target = reward + gamma * np.max(Q[state2[1], :])
    Q[state[1], action] = Q[state[1], action] + lr_rate * (target - predict)

# Start
def start(type_of_action):
    average_payouts = []
    t = 0
    for episode in range(total_episodes):
        state = env.reset()
        done = False
        total_payout = 0
        if(t%10==0):
            print("Episode",t)
        max_steps=0
        while done is False:
            #env.render()
            max_steps+=1
            if(type_of_action=="random"):
             
                action = choose_random_action()
            elif(type_of_action=="honest"):
                action = choose_honest_action()
            else:
                action = choose_action(state) 
            print("action: ",action)

            state2, reward, done, info = env.step(action)  
            print("STATE: ",state2)
            print("----INFO---- ",info)
            learn(state, state2, reward, action)
            total_payout+=reward
            state = state2
            if done:
                t+=1
                break
                time.sleep(0.1)
        average_payouts.append(total_payout)

    print(Q)
    plt.plot(average_payouts)                
    plt.xlabel('total_episodes')
    plt.ylabel('ETH payout after 1 hour')
    plt.savefig("Q_learning_GRAPH_%s"%type_of_action)    
    print ("Average payout after {} rounds is {}".format(max_steps, sum(average_payouts)/total_episodes))

    with open("pow_qTable.pkl", 'wb') as f:
        pickle.dump(Q, f)


def main():
    start("random")
    start("honest")
    start("agent")


if __name__ == '__main__':
    main()
