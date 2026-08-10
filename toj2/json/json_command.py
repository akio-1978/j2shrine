import argparse
from ..command import Command
from .json_loader import JsonLoader
import toj2

# CommandRunnerのデフォルト実装


class JsonCommand(Command):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{toj2.PROG_NAME} json mode',
                                              usage=toj2.SEE_HELP)
        super().__init__()

    def get_loader(self, context):
        """Commandが使うRenderのクラスを返す"""
        return JsonLoader(context=context, processor=self.get_processor(context=context))
