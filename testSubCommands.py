#encoding: u8
from subcommands import *


class ExecCommands(BaseCommands):

	def command_run(self, command, timeout=None):
		result = self.SubCommands(command, timeout)
		for rs in result:
			key = rs.keys()[0]
			value = rs[key]
			if key == 'logging':
				print "logging: ", value
			elif key == 'execoutput':
				print "execoutput: ", value
			elif key == 'Last':
				print "Last: ", value
			elif key == 'return':
				print "return: ", value
			




def main():
	exeobj = ExecCommands()
	exeobj.command_run("echo -e 'aaa\nbbb\n' && for i in {1..10};do echo $i ;done;echo abcd ; echo haha 1 2 3", 15)


if __name__ == '__main__':
	main()
