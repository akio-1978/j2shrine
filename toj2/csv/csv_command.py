import argparse
import toj2
from ..command import Command
from .csv_loader import CsvLoader


class CsvCommand(Command):

    def __init__(self):
        self.parser = argparse.ArgumentParser(exit_on_error=False, prog=f'{toj2.PROG_NAME} csv mode',
                                              usage=toj2.SEE_HELP
                                              )
        super().__init__()

    def get_loader(self, context):
        """Commandが使うRenderのクラスを返す"""
        return CsvLoader(context=context, processor=self.get_processor(context=context))

    def add_optional_arguments(self):
        """csv固有のオプション引数を定義する
        """
        # flag first line is header
        self.parser.add_argument('-H', '--header', help='先頭行をヘッダとして解釈するか？ヘッダは各カラムの名前として使用可能.',
                            dest='read_header', action='store_true')
        # flag tab separate values
        self.parser.add_argument('-d', '--delimiter', dest='delimiter', metavar='',
                            help="カラムの区切り文字 defaultは ',' .", default=',')
        # skip head lines
        self.parser.add_argument('-s', '--skip-lines', metavar='',
                            type=int, help='指定した数値分だけ先頭から行を読み飛ばす.', default=0)
        self.parser.add_argument('--col-prefix', default='col_')
