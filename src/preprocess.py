from typing import Literal

import pandas as pd


def make_dataset(
        df_runs: pd.DataFrame,
        df_pitcher: pd.DataFrame,
        league: Literal['central', 'pacific']) -> pd.DataFrame:
    """ 使用するデータセットを作成・取得する

    Output:
        df: pd.DataFrame
            使用するデータセット

            (output image)
            | my_team | opp_team | runs_lost | player |
            | ------- | -------- | --------- | ------ |
            |  lions  |  hawks  |    0    |  高橋光成  |
    """

    if league not in {'central', 'pacific'}:
        raise ValueError('引数leagueは"central"か"pacific"を指定してください')

    # 対象行の絞り込み
    df_runs = df_runs.query('gameKind == "リーグ戦"')
    if league == 'central':
        df_runs = df_runs.query(
            'team_en=="tigers" or team_en=="carp" or team_en=="dena" or team_en=="giants" or team_en=="swallows" or team_en=="dragons"')
    elif league == 'pacific':
        df_runs = df_runs.query(
            'team_en=="orix" or team_en=="lotte" or team_en=="rakuten" or team_en=="hawks" or team_en=="fighters" or team_en=="lions"')

    # 対象列の絞り込み
    df_runs = df_runs[['date', 'opp_team_en', 'team_en', 'total']]

    # 元データが得点を表しているので失点に変換
    df_runs = df_runs.rename(columns={
        'opp_team_en': 'my_team',
        'team_en': 'opp_team',
        'total': 'runs_lost'
    })

    # 対象行の絞り込み
    df_pitcher = df_pitcher.query('gameKind == "リーグ戦"')
    if league == 'central':
        df_pitcher = df_pitcher.query(
            'team_en=="tigers" or team_en=="carp" or team_en=="dena" or team_en=="giants" or team_en=="swallows" or team_en=="dragons"')
    elif league == 'pacific':
        df_pitcher = df_pitcher.query(
            'team_en=="orix" or team_en=="lotte" or team_en=="rakuten" or team_en=="hawks" or team_en=="fighters" or team_en=="lions"')

    # 先発投手のみ抽出
    df_pitcher = df_pitcher.groupby(['team_en', 'date']).first()[
        'player'].reset_index()

    df = df_runs.merge(
        df_pitcher,
        left_on=['date', 'my_team'],
        right_on=['date', 'team_en'],
        how='left'
    )
    df = df.drop(columns=['team_en'], axis=1).reset_index(drop=True)

    return df
