import argparse
from pathlib import Path
import toj2
from ..command import Command, KeyValuesParseAction
from .excel_loader import ExcelLoader
from .excel_processor import ExcelProsessor
from ..utils import get_stream
from .excelutils import parse_read_range, parse_sheet_args

class ExcelCommand(Command):

    HELP_SHEETS = """読込対象シート ('1' シート1のみ. '1:4' シート1からシート4まで. '1:' シート1からすべてのシート)"""
    HELP_READ_RANGE = """読込セル範囲 ('A1:D4' A1:D4の16セル 'A1:D' A1を起点として、AからDまでの全ての行.)"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{toj2.PROG_NAME} excel mode', 
                                              formatter_class=argparse.RawTextHelpFormatter,
                                              usage=toj2.SEE_HELP)
        super().__init__()

    def get_loader(self, context):
        """Commandが使うRenderのクラスを返す"""
        return ExcelLoader(context=context, processor=self.get_processor(context=context))

    def get_processor(self, context):
        return ExcelProsessor(context=context)

    def add_positional_arguments(self):
        """excel固有の必須引数があるので、位置引数を定義しなおす
            * excelブックをstdinから受け取れないため、ファイル名は必須
            * 読み取り対象シートの指定は必須
            * 読み取りセル範囲の指定は必須
        """
        super().add_positional_arguments()
        self.parser.add_argument('sheets', help=ExcelCommand.HELP_SHEETS, action=SheetRangeAction)
        self.parser.add_argument('read_range', help=ExcelCommand.HELP_READ_RANGE, action=CellRangeAction)

    def add_optional_arguments(self):
        """excel固有のオプションを追加する"""
        # 基本的なオプションは引き継ぐ
        super().add_optional_arguments()
        # 絶対位置指定セルを追加する
        self.parser.add_argument(
            '-a', '--absolute', help='絶対位置指定でセル値を固定で取得する [セル位置=名前]の形式で列挙する. ex: A1=NAME1 A2=NAME2...', dest='absolute', nargs='*', default={}, action=KeyValuesParseAction)
        self.parser.add_argument('--col-prefix', default='col_')
        self.parser.add_argument('--split', help='ソートの1枚ごとに1ファイルを生成します.このモードを指定するためには出力先をディレクトリに指定する必要があります。', nargs=1, dest='split')

    def call_render(self, *, render, source, out):
        """
        in側はopenpyxlにファイル名を直接渡す必要があるため、call_renderをoverrideする
        """
        with get_stream(source=out, 
                           encoding=render.context.output_encoding, 
                           mode='w' ) as dest:
            render.render(source=source, output=dest)

    def validate(self, context):
        """parse_argsでは検出できないエラーの捕捉"""
        path = Path(context.out)
        if context.split and not path.is_dir():
            raise ValueError('--split指定時は出力先はディレクトリを指定してください')
        
        if context.source == '-':
            raise ValueError('Excelブックは標準出力から読み込めません')

class CellRangeAction(argparse.Action):
    """ 読み取るセル範囲を表す座標情報をセットする
        ex. 指定値毎の動作
        A2:C4 => 3row * 3column = 9 cells
        A2:C  => 3row * all_rows = 3(all_rows) cells
        setattrされる値は2つのCellPositionのタプル（起点、終点）
    """
    
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, parse_read_range(range_str=values))
        
class SheetRangeAction(argparse.Action):
    """処理対象シートを決定するアクション
        ex. 指定値毎の動作
        1    => 1枚目のシートを処理対象とする
        1:4  => 1-4枚目のシートを処理対象とする
        1:   => 1枚目以降全てのシートを処理対象とする
        setattrされる値は起点、終点のtuple(int)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, parse_sheet_args(sheets_range_str=values))

