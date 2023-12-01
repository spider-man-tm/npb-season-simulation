import logging


def make_logger(path: str) -> logging.Logger:
    logger = logging.getLogger(__name__)       # ロガーを取得
    logger.setLevel(logging.DEBUG)             # 出力レベルを設定

    # 呼び出し元が異なる際に起こるloggerの重複を防ぐ
    if not logger.hasHandlers():
        fmt = logging.Formatter(
            '[%(levelname)s] - %(asctime)s - %(message)s'
        )                                      # フォーマッターを設定
        handler_s = logging.StreamHandler()    # ストリームハンドラーを生成（標準出力）
        handler_f = logging.FileHandler(path)  # ファイルハンドラーを生成（ログファイル出力）
        handler_s.setLevel(logging.DEBUG)      # 出力レベルを設定
        handler_f.setLevel(logging.INFO)       # 出力レベルを設定
        handler_s.setFormatter(fmt)            # ハンドラーにフォーマッターを設定
        handler_f.setFormatter(fmt)            # ハンドラーにフォーマッターを設定
        logger.addHandler(handler_s)           # ロガーにハンドラーを設定
        logger.addHandler(handler_f)           # ロガーにハンドラーを設定
        logger.propagate = False
    return logger
