#!/usr/bin/python
# -*- coding:utf-8 -*-


	
class Vec3(object):
	u"""3次元ベクトル
	"""
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		
	def __add__(self, vec3):
		return Vec3(self.x + vec3.x, self.y + vec3.y, self.z + vec3.z)
		
	def __sub__(self, vec3):
		return Vec3(self.x - vec3.x, self.y - vec3.y, self.z - vec3.z)
	
	def __repr__(self):
		return "(x:%f, y:%f, z:%f)" % (self.x, self.y, self.z)

class Sphere(object):
	u"""球体
	"""
	def __init__(self, pos, radius):
		self.pos = pos
		self.r   = radius
		
	def __repr__(self):
		return "<pos:%s, r:%f>" % (self.pos, self.r)

class OctTree(object):
	u"""八分木を扱う
	登録オブジェクトはSphere前提
	任意のオブジェクトを登録できるようにしたい
	"""
	
	def __init__(self, level, rectBeginXYZ, rectEndXYZ):
		"""コンストラクタ
		@param level        空間を分割する深さ(0=空間数0, 1=空間数9, 2=空間数73 ...)
		@param rectBeginXYZ 空間開始座標
		@param rectEndXYZ   空間終点座標
		"""
		self.__level = level
		self.__begin = rectBeginXYZ
		self.__end   = rectEndXYZ
		assert self.__begin.x < self.__end.x
		assert self.__begin.y < self.__end.y
		assert self.__begin.z < self.__end.z
		self.__size  = Vec3(self.__end - self.__begin)

	def add(self, obj):
		pass
		
	def traverse(self, traverser):
		"""ツリー内を
		"""
		pass
		
	def getIndexOf(self, sphere):
		"""指定オブジェクトが所属する空間インデックスを返す
		"""
		print "sphere", sphere
		sphereMin = Vec3(sphere.pos.x - sphere.r, sphere.pos.y - sphere.r, sphere.pos.z - sphere.r)
		sphereMax = Vec3(sphere.pos.x + sphere.r, sphere.pos.y + sphere.r, sphere.pos.z + sphere.r)
		print "sphereMin", sphereMin
		print "sphereMax", sphereMax
		minIdx = Vec3(
			self.__getAxisIndex(sphereMin.x, self.__begin.x, self.__end.x),
			self.__getAxisIndex(sphereMin.y, self.__begin.y, self.__end.y),
			self.__getAxisIndex(sphereMin.z, self.__begin.z, self.__end.z)
		)
		maxIdx = Vec3(
			self.__getAxisIndex(sphereMax.x, self.__begin.x, self.__end.x),
			self.__getAxisIndex(sphereMax.y, self.__begin.y, self.__end.y),
			self.__getAxisIndex(sphereMax.z, self.__begin.z, self.__end.z)
		)
		if minIdx.x < 0 or minIdx.y < 0 or minIdx.z < 0 or maxIdx.x < 0 or maxIdx.y < 0 or maxIdx.z < 0:
			return -1

		print "minIdx", minIdx
		print "maxIdx", maxIdx
		minMortonIndex    = self.__getMortonIndex(minIdx.x, minIdx.y, minIdx.z)
		maxMortonIndex    = self.__getMortonIndex(maxIdx.x, maxIdx.y, maxIdx.z)
		print "minMortonIndex", minMortonIndex
		print "maxMortonIndex", maxMortonIndex
		commonLevel       = self.__getCommonLevel(minMortonIndex, maxMortonIndex)
		print "commonLevel", commonLevel
		if 0 < commonLevel:
			commonMortonIndex = minMortonIndex >> ((self.__level - commonLevel) * 3)	# minMortonIndexでもmaxMortonIndexでもどっちでもいい
			print "commonMortonIndex", commonMortonIndex
			
			# todo:事前に計算したほうがいい
			offset = (8 ** commonLevel - 1) / 7
			sphereIndex       = offset + commonMortonIndex
			return sphereIndex
		return 0

	def __separateBit3(self, n):
		n = (n | n << 8) & 0x0000f00f
		n = (n | n << 4) & 0x000c30c3
		n = (n | n << 2) & 0x00249249
		return n
		
	def __getMortonIndex(self, idxX, idxY, idxZ):
		return self.__separateBit3(idxX) | self.__separateBit3(idxY) << 1 | self.__separateBit3(idxZ) << 2
		
	def __getCommonLevel(self, idx0, idx1):
		u"""2点の共有空間レベルを取得
		"""
		print "idx0:%d(%s)" % (idx0, bin(idx0))
		print "idx1:%d(%s)" % (idx1, bin(idx1))
		if self.__level == 0:
			return 0
		xor = idx0 ^ idx1
		print "xor", bin(xor)
		level = self.__level
		while 0 < xor:
			xor = xor >> 3
			level -= 1
			print "shift level", level
		return level
		
	def __getAxisIndex(self, pos, begin, end):
		"""軸に対するインデックスを返す
		"""
		# 範囲外はマイナス値を返す
		if pos < begin or end < pos:
			return -1
		width = end - begin
		return int((pos - begin) / (width / (2 ** self.__level)))

	

# test
#sphere1 = Sphere(Vec3(200, 300, 400), 50.0)
#sphere2 = Sphere(Vec3(300, 400, 500), 20.0)
sphere1 = Sphere(Vec3(0, 0, 0), 0.5)
sphere2 = Sphere(Vec3(1, 0, 0), 0.5)
#camera  = Sphere(Vec3(210, 310, 410), 1.0)

octtree = OctTree(2, Vec3(0, 0, 0), Vec3(4, 4, 4))
#octtree.add(sphere1)
#octtree.add(sphere2)
#print octtree.getIndexOf(sphere1)
#print octtree.getIndexOf(sphere2)
#octtree.traverse(camera)

#print octtree._OctTree__getCommonLevel(16, 23)
print octtree.getIndexOf(Sphere(Vec3(1, 1, 1), 0.8))
print octtree.getIndexOf(Sphere(Vec3(2, 2, 2), 0.8))
print octtree.getIndexOf(Sphere(Vec3(3, 3, 3), 0.8))
print octtree.getIndexOf(Sphere(Vec3(0.5, 0.5, 0.5), 0.1))
print octtree.getIndexOf(Sphere(Vec3(3.5, 3.5, 3.5), 0.1))

