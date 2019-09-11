import abc

class SubCmd(abc.ABC):
    @abc.abstractmethod
    def add_parser(self, subparser):
        return NotImplemented

    @abc.abstractmethod
    def execute(self, args):
        return NotImplemented
