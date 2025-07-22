def run_simulation(game_class, players_class, n_games: int):
    results = []
    for _ in range(n_games):
        game = game_class()
        players = players_class()
        while not game.is_game_over():
            for i in range(game.num_players):
                obs = game.get_observation(i)
                action = players.choose_action(obs)
                game.apply_action(i, action)
        results.append(game.get_score())
    return results
