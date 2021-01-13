#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import io
from logging import getLogger, StreamHandler, DEBUG
import re
import os

ENCODE_IN  = 'utf_8'
ENCODE_OUT = 'utf_8_sig'

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel (DEBUG)
logger.addHandler(handler)
logger.propagate = False


def change_encode(input_dir, pattern, output_dir, is_recursive = True, is_overwrite = True):
    """ 指定されたディレクトリ内にあるファイルを走査し、
    パターンに合致するファイルのみエンコード形式を変更し、
    指定されたディレクトリに出力する。

    Parameters
    ----------
    input_dir : str
        エンコードするファイルが格納されているディレクトリ
    pattern : str
        検索するファイル名のパターン（正規表現）
    output_dir : str
        エンコード変更後のファイルを出力するディレクトリ
    is_recursive : bool
        再帰的に走査するか
    is_overwrite : bool
        出力するファイルが既に存在する場合上書きするか
    """
    logger.debug(f"start input_dir:[{input_dir}], pattern:[{pattern}],output_dir:[{output_dir}], is_recursive:[{is_recursive}], is_overwrite:[{is_overwrite}]")
 
    if is_recursive:
        target_path = os.path.join(input_dir, "**", pattern)
    else:
        target_path = os.path.join(input_dir, pattern)
    logger.debug(f"target_path:[{target_path}]")
 
    files = glob.glob(target_path, recursive=is_recursive)
    logger.debug(f"files counts:[{len(files)}]")
    for f_in in files:
        logger.debug(f"file path:[{f_in}]")

        # 本スクリプトのエンコードは変更しない
        if f_in == __file__:
            continue
        # 出力先フォルダ作成
        f_out = f_in.replace(input_dir, output_dir)
        d_out = os.path.dirname(f_out)
        logger.debug(f"f_out:{f_out}, d_out:{d_out}")
        if not os.path.exists(d_out):
            logger.debug(f"make directory {d_out}")
            os.makedirs(d_out, exist_ok=True)
        # エンコードの変換
        with io.open(f_in, "rt", encoding=ENCODE_IN) as fs_in, io.open(f_out, "w", encoding=ENCODE_OUT) as fs_out:
            i = 0
            for line in fs_in:
                fs_out.write(line)
                i += 1
            logger.debug(f"{f_in}, line count:{i}")

current_path = os.path.dirname(__file__)
output_path_template = os.path.join(current_path, "encoded")
output_path = output_path_template

# 出力先フォルダ作成
i = 0
# 既にフォルダがあれば別名フォルダを作成
while os.path.exists(output_path):
    i += 1
    if i == 0:
        output_path = output_path_template
    else:
        output_path = output_path_template + f" ({i})"
# エンコード実行
change_encode(current_path, "*.csv", output_path)