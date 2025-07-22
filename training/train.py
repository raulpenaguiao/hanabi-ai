def train_agents():
    for epoch in range(NUM_EPOCHS):
        rewards = run_simulation(...)
        loss = -reward.mean()  # use REINFORCE or PPO loss
        loss.backward()
        optimizer.step()
