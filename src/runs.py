class Runs:
    def __init__(self, df, league: str):
        self.df = df

        if league == 'central':
            self.teams = ['tigers', 'carp', 'dena',
                          'giants', 'swallows', 'dragons']
        elif league == 'pacific':
            self.teams = ['orix', 'lotte', 'hawks',
                          'rakuten', 'lions', 'fighters']

        self.pitcher_stats1 = None
        self.pitcher_stats2 = None
        self.runs_stats = None

    def __repr__(self):
        return f'Runs(league={self.league}, seed={self.seed})'

    def agg_stats(self) -> None:
        dict[str, dict[str, list[int]]]
        """投手の成績を3種類の軸で取得する

        Returns:
            - pitcher_stats1 (dict[str, dict[str, dict[str, list[int]]]]): 対戦チームを考慮した投手の対戦成績
                example:
                    {
                        'lions': {
                            'hawks': {
                                '高橋': [int, int, ...],   # lions高橋の vsソフトバンク失点実績
                                '松本': [int, int, ...],
                            }
                        },
                    }
            - pitcher_stats2 (dict): 対戦チームを考慮しない投手の対戦成績
                example:
                    {
                        'lions': {
                            '高橋': [int, int, ...],   # lions高橋の失点実績
                            '松本': [int, int, ...],
                        },
                    }
            - runs_stats (dict): 対戦投手を考慮しないチームの得点成績
                example:
                    {
                        'lions': [int, int, ...],   # lionsの得点実績
                        'hawks': [int, int, ...],
                    }
        """
        pitcher_stats1 = {}
        pitcher_stats2 = {}
        runs_stats = {}

        for my_team in self.teams:
            # stats1: 対戦チームを考慮した投手の対戦成績
            pitcher_stats1[my_team] = {
                k: {} for k in self.teams if k != my_team}
            team_df = self.df[self.df['my_team'] == my_team]

            # stats2: 対戦チームを考慮しない投手の対戦成績
            pitcher_stats2[my_team] = {}

            # stats3: 対戦投手を考慮しないチームの得点成績
            runs_stats[my_team] = []

            for _, row in team_df.iterrows():
                _player = row['player']
                _op_team = row['opp_team']
                _run = int(row['runs_lost'])

                if _player in pitcher_stats1[my_team][_op_team]:
                    pitcher_stats1[my_team][_op_team][_player].append(_run)
                else:
                    pitcher_stats1[my_team][_op_team][_player] = [_run]

                if _player in pitcher_stats2[my_team]:
                    pitcher_stats2[my_team][_player].append(_run)
                else:
                    pitcher_stats2[my_team][_player] = [_run]

                runs_stats[my_team].append(_run)

        self.pitcher_stats1 = pitcher_stats1
        self.pitcher_stats2 = pitcher_stats2
        self.runs_stats = runs_stats
