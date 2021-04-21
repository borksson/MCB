import shutil
import zlib
import codecs
cTypes = ['GZip','Zlib']

worldName = "TestZone"

regionFileName = "r.0.-1.mca"

shutil.copy2("C:\\Users\\craz0\\Desktop\\Programing\\Geany\\MCB\\regionBase.txt", "C:\\Users\\craz0\\AppData\\Roaming\\.minecraft\\saves\\"+worldName+"\\region\\"+regionFileName)

#prep region file copy

regionFilePath = "C:\\Users\\craz0\\AppData\\Roaming\\.minecraft\\saves\\"+worldName+"\\region\\"+regionFileName

def ChunkBuilder(chunkx,chunkz):
	chunk = [chunkx,chunkz]
	
	offset = 4 * ((chunk[0] % 32) + (chunk[1] % 32) * 32)
	with open("C:\\Users\\craz0\\Desktop\\Programing\\Geany\\MCB\\chunkBase.txt","rb") as file:
		chunkBase = file.read().hex()

	print("Chunkbase opened")
	# In[88]:


	sectionTag = "09000853656374696f6e730a00000010"
	frontAdd = chunkBase.index(sectionTag)
	chunkBase[frontAdd+len(sectionTag)+36:frontAdd+len(sectionTag)+36+4096]


	# In[89]:


	frontsAdd = frontAdd+len(sectionTag)+36
	endAdd = frontAdd+len(sectionTag)+36+4096
	blockStates = "0"*4096
	for i in range(16):
		if i==0:
			chunkBase = chunkBase[:frontsAdd]+blockStates+chunkBase[endAdd:]
		else:
			chunkBase = chunkBase[:frontsAdd+(12530*i)]+blockStates+chunkBase[endAdd+(12530*i):]

	print("Block states edited")
	# In[90]:


	#compress
	chunkField = ""
	BOchunkData = bytearray.fromhex(chunkBase)
	cChunkData = zlib.compress(BOchunkData)

	chunkLength = hex(int(len(cChunkData.hex())/2))
	if len(chunkLength)%2==0:
		chunkLength = "0"*(8-len(chunkLength[2:]))
	else:
		chunkLength = "0"+str(chunkLength[2:])
		chunkLength = "0"*(8-len(chunkLength))+chunkLength
	chunkLength = bytes.fromhex(chunkLength)

	print("Data compressed")
	# In[91]:


	#overwrite chunk data [0,0]
	with open(regionFilePath,"r+b") as file:
		file.seek(offset,0)
		chunkOffset = 4096*int(file.read(3).hex(),16)
		chunkSize = 4096*int(file.read(1).hex(),16)
		file.seek(chunkOffset,0)
		file.write(chunkLength)
		file.seek(1,1)
		file.write(cChunkData)
		file.seek(chunkOffset,0)
		
	print("Completed:"+str(chunk))

for l in range(32):
	for i in range(32):
		ChunkBuilder(l,i)
