import matplotlib.pyplot as plt


plt.figure(figsize = (6.4, 4.8), dpi = 100)
agent_name = ['random_agent',
              'simple_agent',
              'smart_agent' ,
              'smart_attack_agent',
              'sparse_agent'
             ]

agent_count = len(agent_name)

path = 'C:/Users/Jack/Documents/EMC - Machine Learning/'


# Loop to read the agent data and plot on a figure
for i in range(agent_count):
    file_name = path + agent_name[i] + '_results.txt'
    Value = [0, 0, 0]
    Game_number = []
    Win_percentage = []
    Played = 0
    # Reading the agent data and adjusting the value array dependant on win,
    # draw, or loss
    with open(file_name, 'r') as file:
        for line in file:
            if (line == ''):
                file.close()
            elif (Played < 50):
                if (int(line)) == 1:
                    Value[0] += 1
                elif (int(line)) == 0:
                    Value[1] += 1
                elif (int(line)) == -1:
                    Value[2] += 1
                # Calculating the total games played and the win rate
                Played = Value[0] + Value[1] + Value[2]
                Win_rate = (Value[0] / Played) * 100
                # Appending the x and y values
                Game_number.append(Played)
                Win_percentage.append(Win_rate)
        # Adding the agent data to the figure
        plt.plot(Game_number, Win_percentage, label = agent_name[i])
        # Can calculate the win, draw and loss rate of each agent
        #Win_rate = (Value[0] / Played) * 100
        #Draw_rate = (Value[1] / Played) * 100
        #Loss_rate = (Value[2] / Played) * 100


# Labeling the figure
plt.xlabel('Number of games played')
plt.ylabel('Win percentage')
plt.title('StarCraft II Agent Win Rates')
plt.legend()
plt.show()
plt.figure().savefig('Results_50.jpg')