import random
import warnings
from typing import Literal

import numpy as np
import numba

from src.game import Game
from src.runs import Runs


# 特定の警告を無視する
warnings.filterwarnings('ignore', category=numba.NumbaDeprecationWarning)
warnings.filterwarnings('ignore', category=numba.NumbaWarning)


@numba.jit
def simulation(game: Game, runs: Runs, seed: int):
    pitcher_stats1 = runs.pitcher_stats1
    pitcher_stats2 = runs.pitcher_stats2
    runs_stats = runs.runs_stats
    home_teams = game.schedule['home_team'].values
    away_teams = game.schedule['away_team'].values
    home_pitchers = game.schedule['home_pitcher'].values
    away_pitchers = game.schedule['away_pitcher'].values

    home_team_runs = np.zeros(len(home_teams))
    away_team_runs = np.zeros(len(away_teams))

    for i, (home_team, away_team, home_pitcher, away_pitcher) in enumerate(zip(
        home_teams, away_teams, home_pitchers, away_pitchers
    )):
        random.seed(seed + i)
        random_number = random.random()

        if random_number < 0.6:
            # 方法1: 自チームの先発投手 vs 対戦チームの過去失点からランダムに選択(ただし対戦実績がなければ、他の方法を選択)
            away_team_run = select_run(
                random_number, pitcher_stats1, pitcher_stats2, runs_stats,
                my_team=home_team, op_team=away_team, pitcher=home_pitcher)
            # 方法1: 対戦チームの先発投手 vs 自チームの過去失点からランダムに選択(ただし対戦実績がなければ、他の方法を選択)
            home_team_run = select_run(
                random_number, pitcher_stats1, pitcher_stats2, runs_stats,
                my_team=away_team, op_team=home_team, pitcher=away_pitcher)
        elif random_number < 0.9:
            # 方法2: 対戦チームの先発投手 vs 全チームの過去失点からランダムに選択
            home_team_run = _random_select_run_from_s2(
                pitcher_stats2, away_team, away_pitcher)
            # 方法3: 自チームの先発投手 vs 全チームの過去失点からランダムに選択
            away_team_run = _random_select_run_from_s2(
                pitcher_stats2, home_team, home_pitcher)
        else:
            # 方法3: 自チームの全得点実績からランダムに選択
            home_team_run = _random_select_run_from_rs(runs_stats, home_team)
            # 方法3: 対戦チームの全得点実績からランダムに選択
            away_team_run = _random_select_run_from_rs(runs_stats, away_team)

        home_team_runs[i] = home_team_run
        away_team_runs[i] = away_team_run

    return home_team_runs, away_team_runs


@numba.jit
def select_run(
    random_number: float,
    pitcher_stats1: dict,
    pitcher_stats2: dict,
    runs_stats: dict,
    my_team: str,
    op_team: str,
    pitcher: str):
    # 方法1
    if pitcher in pitcher_stats1[my_team][op_team]:
        return _random_select_run_from_s1(pitcher_stats1, my_team, op_team, pitcher)
    # 対戦実績がなければ、他の方法を選択
    if random_number < 0.5:
        # 方法2
        return _random_select_run_from_s2(pitcher_stats2, my_team, pitcher)
    # 方法3
    return _random_select_run_from_rs(runs_stats, op_team)


def _random_select_run_from_s1(
    stats: dict,
    my_team: str,
    op_team: str,
    my_pitcher: str
):
    return random.choice(stats[my_team][op_team][my_pitcher])


def _random_select_run_from_s2(
    stats: dict,
    my_team: str,
    my_pitcher: str
):
    return random.choice(stats[my_team][my_pitcher])


def _random_select_run_from_rs(
    stats: dict,
    my_team: str
):
    return random.choice(stats[my_team])


def agg_ranking(df, inter_games: dict) -> list[str]:
    """シミュレーション結果から勝率を計算し、ランキングを返す"""

    def _get_win_team(row):
        if row['home_team_runs'] > row['away_team_runs']:
            return row['home_team']
        elif row['home_team_runs'] < row['away_team_runs']:
            return row['away_team']
        else:
            return None

    def _get_lose_team(row):
        if row['home_team_runs'] < row['away_team_runs']:
            return row['home_team']
        elif row['home_team_runs'] > row['away_team_runs']:
            return row['away_team']
        else:
            return None

    df['win_team'] = df.apply(_get_win_team, axis=1)
    df['lose_team'] = df.apply(_get_lose_team, axis=1)

    win_cnt = dict(df['win_team'].value_counts())
    loss_cnt = dict(df['lose_team'].value_counts())

    win_cnt = {_team: win_cnt[_team] + inter_games[_team][0]
               for _team in win_cnt.keys()}
    loss_cnt = {_team: loss_cnt[_team] + inter_games[_team][1]
                for _team in loss_cnt.keys()}
    win_rate = {_team: win_cnt[_team] / (win_cnt[_team] + loss_cnt[_team])
                for _team in win_cnt.keys()}
    ranking = sorted(win_rate, key=win_rate.get, reverse=True)

    return ranking
