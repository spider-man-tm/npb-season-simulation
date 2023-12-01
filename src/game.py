import random

import pandas as pd
import numpy as np


class Game():
    def __init__(self, df_base: pd.DataFrame, league: str, seed: int = 0):
        self.df_base = df_base
        self.seed = seed

        if league == 'central':
            self.teams = ['tigers', 'carp', 'dena',
                          'giants', 'swallows', 'dragons']
        elif league == 'pacific':
            self.teams = ['orix', 'lotte', 'hawks',
                          'rakuten', 'lions', 'fighters']

        self.schedule = None

    def __repr__(self):
        return f'Game(league={self.league}, seed={self.seed})'

    def set_schedule(self) -> None:
        """実際の試合日程に対して、対戦先発投手をセットしていく"""
        starting_pithers = self.get_staring_pithcers()
        opp_pithers = self.set_opp_pither(starting_pithers)

        df_schedule = self.df_base.iloc[1::2][['date', 'my_team', 'opp_team']]
        df_schedule = df_schedule.rename(
            columns={'my_team': 'home_team', 'opp_team': 'away_team'})
        home_pithers, away_pitchers = [], []

        for _, row in df_schedule.iterrows():
            home_team, away_team = row['home_team'], row['away_team']
            home_pithers.append(opp_pithers[home_team][away_team].pop(0))
            away_pitchers.append(opp_pithers[away_team][home_team].pop(0))

        df_schedule['home_pitcher'] = home_pithers
        df_schedule['away_pitcher'] = away_pitchers

        self.schedule = df_schedule

    def get_staring_pithcers(self) -> dict[str, np.ndarray]:
        """先発投手を取得する

        Returns:
            dict[str, np.ndarray]: 125試合分の先発投手

            example:
                {
                    lions: np.array(['高橋', '高橋', '高橋', ...]),   # 125試合分
                    fighters: ...
                }
        """
        starting_pithers = {}
        for team in self.teams:
            _df = self.df_base[self.df_base['my_team'] == team]
            starting_pithers[team] = np.array(sorted(_df['player']))

        return starting_pithers

    def set_opp_pither(self, starting_pithers: dict[str, np.ndarray]):
        """対戦相手の先発投手をセットする

        Args:
            starting_pithers (dict[str, list]): 125試合の先発投手リスト

        Returns:
            dict[str, dict[str, list]]: 対戦チームとの試合に投げる先発投手リスト

            example:
                {
                    lions: {
                        hawks: ['高橋', '今井', '松本', ...],   # vs Hawks 25試合分
                        rakuten: ...
                    },
                    carp: ...
                }
        """
        opp_pithers = {}
        for i, my_team in enumerate(self.teams):
            opp_pithers[my_team] = {}

            # ランダムに並べ替える
            random.seed(self.seed + i)
            opp_teams = [opp for opp in self.teams if opp != my_team]
            opp_teams = random.sample(opp_teams, len(opp_teams))

            for j, opp_team in enumerate(opp_teams):
                # ランダムに並べ替える
                random.seed(self.seed + i + j)
                _pitchers = list(starting_pithers[my_team][j::5])
                _pitchers = random.sample(_pitchers, len(_pitchers))
                opp_pithers[my_team][opp_team] = _pitchers

        return opp_pithers
