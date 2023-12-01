from typing import Literal

import matplotlib.pyplot as plt


def plot_ranking(
    rankings: list[list[str]],
    league: Literal['central', 'pacific'],
    img_path: str,
    n_simulation: int,
):
    if league not in {'central', 'pacific'}:
        raise ValueError('league must be central or pacific')

    if league == 'central':
        teams = ['tigers', 'carp', 'dena', 'giants', 'swallows', 'dragons']
        colors = ['#ffe201', '#ff0000', '#094a8c',
                  '#f97709', '#98c145', '#002569']
    else:
        teams = ['orix', 'lotte', 'hawks', 'rakuten', 'lions', 'fighters']
        colors = ['#b08f32', '#221815', '#f9ca00',
                  '#85010f', '#102961', '#02518c']

    # 順位の出現回数を集計
    result = {team: [0, 0, 0, 0, 0, 0] for team in teams}
    for ranking in rankings:
        for i, team in enumerate(ranking):
            result[team][i] += 1

    fig, axes = plt.subplots(3, 2, figsize=(8, 9))
    bin_edges = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]  # ビンのエッジを手動で設定

    for i, (_team, _list) in enumerate(result.items()):
        _place = []
        for j in range(6):
            _place.extend([j + 1] * _list[j])
        axes[i//2][i % 2].hist(_place, bins=bin_edges, color=colors[i])
        axes[i//2][i % 2].set_ylim([0, int(n_simulation * 0.7)])
        axes[i//2][i % 2].set_xlim([0.5, 6.5])
        axes[i//2][i % 2].set_xticks(range(1, 7))
        axes[i//2][i % 2].set_title(f'{_team}')

    fig.tight_layout()
    plt.savefig(img_path)
