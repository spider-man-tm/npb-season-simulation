import os
import logging
from typing import Literal

import pandas as pd

from src.preprocess import make_dataset
from src.game import Game
from src.runs import Runs
from src.simulation import simulation, agg_ranking
from src.plot import plot_ranking
from src.utils import make_logger


def main(
    league: Literal['central', 'pacific'], year: int, n_simulation: int = 10000, logger=logging.Logger
) -> None:
    df_runs = pd.read_csv(f'data/df_runs_{year}.csv')
    df_pitcher = pd.read_csv(f'data/df_pitcher_{year}.csv')

    df = make_dataset(df_runs, df_pitcher, league=league)

    # 交流戦成績は今回のシミュレーションでは考慮せず、そのまま使用する
    if year == 2021:
        inter_games = {
            'tigers': [11, 7, 0],    # win、loss、draw
            'carp': [3, 12, 3],      # win、loss、draw
            'dena': [9, 6, 3],       # win、loss、draw
            'giants': [7, 8, 3],     # win、loss、draw
            'swallows': [10, 8, 0],  # win、loss、draw
            'dragons': [9, 7, 2],    # win、loss、draw
            'orix': [12, 5, 0],      # win、loss、draw
            'lotte': [8, 9, 1],      # win、loss、draw
            'hawks': [5, 9, 4],      # win、loss、draw
            'rakuten': [9, 8, 1],    # win、loss、draw
            'lions': [7, 7, 4],      # win、loss、draw
            'fighters': [7, 11, 0],  # win、loss、draw
        }
    elif year == 2023:
        inter_games = {
            'tigers': [7, 10, 1],    # win、loss、draw
            'carp': [9, 9, 0],       # win、loss、draw
            'dena': [11, 7, 0],      # win、loss、draw
            'giants': [11, 7, 0],    # win、loss、draw
            'swallows': [7, 11, 0],  # win、loss、draw
            'dragons': [7, 10, 1],   # win、loss、draw
            'orix': [11, 7, 0],      # win、loss、draw
            'lotte': [7, 9, 2],      # win、loss、draw
            'hawks': [11, 7, 0],     # win、loss、draw
            'rakuten': [9, 9, 0],    # win、loss、draw
            'lions': [6, 12, 0],     # win、loss、draw
            'fighters': [10, 8, 0],  # win、loss、draw
        }

    # 対戦成績の実績集計
    runs = Runs(df, league=league)
    runs.agg_stats()

    # シミュレーション開始
    rankings = []
    for seed in range(n_simulation):

        if seed % 1000 == 0:
            logger.debug(f'simulation: {seed} / {n_simulation} start...')

        # スケジュールの作成
        game = Game(df, league=league, seed=seed)
        game.set_schedule()

        # シミュレーション
        home_team_runs, away_team_runs = simulation(game, runs, seed)

        df_result = game.schedule.copy()
        df_result['home_team_runs'] = home_team_runs
        df_result['away_team_runs'] = away_team_runs

        # シミュレーション結果からランキングを算出
        ranking = agg_ranking(df_result, inter_games)
        rankings.append(ranking)

    # 結果をプロット
    plot_ranking(rankings, league=league,
                 img_path=f'./output/{league}_{year}.png', n_simulation=n_simulation)


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    logger = make_logger(path='logs/main.log')
    main(league='pacific', year=2021, n_simulation=10000, logger=logger)
    main(league='central', year=2021, n_simulation=10000, logger=logger)
    main(league='pacific', year=2023, n_simulation=10000, logger=logger)
    main(league='central', year=2023, n_simulation=10000, logger=logger)
