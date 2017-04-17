#encoding: u8
import subprocess
from time import (time,sleep)
import tempfile



class BaseCommands(object):

	def __init__(self):
		# self.tmpf = tempfile.NamedTemporaryFile(mode='w+b')
		self.tmpf = tempfile.TemporaryFile()
		self.results = set()
		self.lens = []
		self.bufsize = -1
		self.SleepTime = .1
		self.SEEK = 0
		self.Last = ""
		self.TimeOut = 3600


	def SubCommands(self, command, timeout=None):
		Condition = 1
		if timeout:
			deadline = time() + timeout
		else:
			deadline = time() + self.TimeOut
		process = subprocess.Popen(command, 
					   bufsize=self.bufsize,
					   stdout=self.tmpf, 
					   stderr=subprocess.STDOUT, 
					   close_fds=True,
					   shell=True)
		yield {"logging":"执行子进程PID: {pid}".format(pid=process.pid)}

		while Condition:
			if len(self.lens) > 1000:
				self.results = set()
				self.lens = []
			if time() > deadline:
				process.terminate()
				yield {'Last':self.Last}
				yield {'return':('', 'exec command timeout.', -1)}
				break
			sleep(self.SleepTime)
			ret = process.poll()
			self.tmpf.seek(self.SEEK)
			res = self.tmpf.read()
			
			if res and res not in self.results:
				if not self.results:
					newres = res
					yield {'execoutput':newres}
				elif self.lens and len(res.split("\n")) - self.lens[-1] > 1:
					tlen = len(res.split('\n'))
					llen = self.lens[-1]
					newres = '\n'.join(res.split('\n')[llen-1:tlen])
					yield {'execoutput':newres}
				else:
					newres = res.split("\n")
					if len(newres) == 1:
						newres = newres[-1]
					else:
						if newres[-1]:
							newres = newres[-1]
						else:
							newres = newres[-2]
					yield {'execoutput':newres}
				self.Last = newres
				self.results.add(res)
				self.lens.append(len(res.split("\n")))

			if (ret is not None):
				yield {'Last':self.Last}
				if ret == 0:
					yield {'return':(self.Last, '', 0)}
				else:
					yield {'return':('', self.Last, -1)}
				break


	def command_run(self, command, timeout):
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
	exeobj = BaseCommands()
	exeobj.command_run("echo -e 'aaa\nbbb\n' && for i in {1..10};do echo $i ;done;echo abcd ; echo haha 1 2 3", 15)


if __name__ == '__main__':
	main()

