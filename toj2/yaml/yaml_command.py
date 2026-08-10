import argparse
from ..command import Command
from .yaml_loader import YamlLoader
import toj2

# CommandRunnerのデフォルト実装


class YamlCommand(Command):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog=f'{toj2.PROG_NAME} yaml mode',
                                              usage=toj2.SEE_HELP)
        super().__init__()

    def get_loader(self, context):
        """Commandが使うLoaderのクラスを返す"""
        return YamlLoader(context=context, processor=self.get_processor(context=context))
