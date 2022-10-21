# Autor: Vlasov Fedor
# Created: 18.09.2022
# Black Mirror lib for AI

def cs(s: str) -> str:
	s = s.lower()
	r = ''
	for i in range(len(s)):
		if s[i].isalpha() or s[i] == ' ':
			r += s[i]
		else:
			r += ' '
	return r.strip()


def dk(a: str, b: str) -> float:
	l = len(a) + len(b)
	c = l - len(set(a) - set(b))
	if not c:
		return 999.999
	return (l - c) / c


def gl(fn: str) -> list:
	r = []
	with open(fn, 'r') as f:
		r = f.read().split('\n')
	return r


def md(lt: list, m: str, cj: float) -> (int, float):
	if not lt:
		return (-1, 999.999)
	ds = [abs(dk(m, l) - cj) for l in lt]
	ds = [(i, ds[i]) for i in range(len(ds))]
	md = min(ds, key = lambda t: t[1])
	return md


class ChineseRoom:

	def __init__(self, fn: str):
		self.mem = gl(fn)

	def query(self, m: str) -> str:
		mc = 0
		r = ''
		iw = set(cs(m).split(' '))
		for l in self.mem:
			lw = cs(l.split('<&>')[0])
			lw = set(lw.split(' '))
			c = len(iw & lw)
			if c > mc:
				mc = c
				r = l.split('<&>')[-1].strip()
		return r


class Mirror:
	cj = 0
	mj = 0.666
	se = 1
	st = 0.13
	lm = ''
	mem = []
	fue = []

	def __init__(self, fn: str, ar: ChineseRoom):
		ls = gl(fn)
		for i in range(len(ls)):
			res = ar.query(ls[i])
			if res:
				ls[i] += res
		self.mem = ls

	def next(self, m: str, aj: bool = False) -> str:
		ls = list(set(self.mem) - set(self.fue))
		i, d = md(ls, m, self.cj)
		if self.cj > self.mj:
			self.se = -1
		elif self.cj < 0.0:
			self.se = 1
		if aj:
			self.cj += self.se * self.st
		return ls[i] if i >= 0 else ''

	def query(self, m: str, st: str) -> str:
		self.fue = []
		self.lm = cs(m)
		while not st in self.lm:
			pv = self.lm
			self.lm = self.next(self.lm, True)
			self.fue.append(self.lm)
			if not self.lm:
				break
		return self.lm.split(st)[0]

	def requirement(self, m: str = '') -> str:
		return self.query(m, '<?>')

	def conclusion(self, m: str = '') -> str:
		return self.query(m, '<!>')


class BlackMirror:

	def __init__(self, cr: ChineseRoom, mr: Mirror):
		self.cr = cr
		self.mr = mr

	def requirement(self, m: str) -> str:
		req = self.mr.requirement(m)
		return self.cr.query(m)

	def conclusion(self, m: str) -> str:
		return self.mr.conclusion(m)


class Daemon:
	bms = []

	def __init__(self, mr: Mirror):
		self.mr = mr

	def add(self, bm: BlackMirror):
		self.bms.append(bm)

	def query(self, m: str) -> str:
		con = self.mr.conclusion(m)
		cs = [bm.conclusion(con) for bm in self.bms]
		i, d = md(cs, m, 1)
		return self.bms[i].requirement(m) if i >= 0 else ''

