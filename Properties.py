# reads properties.conf file and produce a corresponding object


class Properties :


	# default fileName is properties.conf
	def __init__(self, fileName="properties.conf") :
	
		self.username = ""
		self.password = ""
		self.summon = []
		self.disabled = []
		self.helpmsg = "There is no help message in your config file. Probably an error !"
	
		try :
			fileStream = open(fileName)
		except OSError as readError :
			#TODO improve on error reporting
			return(False)
			
		while True :
			workingLine = fileStream.readline()
			if not workingLine :
				break
			else:
				workingLine = workingLine.strip()
				words = workingLine.split(" ")
			
			if workingLine == "" :
				pass
			elif workingLine[0] == "#" :
				pass
			
			elif words[0] == "username" :
				self.username = words[1]
			
			elif words[0] == "password" :
				self.password = workingLine[9:len(workingLine)]
			
			elif words[0] == "summon" :
				self.summon.append(workingLine[7:len(workingLine)])
				#print(summon)

			elif words[0] == "disabled" :
				self.disabled.append(workingLine[9:len(workingLine)])
				#print(disabled)
				
			# now this is a bit more complicated..
			elif words[0] == "helpmsg" :
				self.helpmsg = ""
				workingLine = fileStream.readline()
				while workingLine.strip() != "helpmsgend" :
					# I guess in theory the terminator wouldn't be needed if helpmsg was at the end of the file
					if not workingLine :
						break
					
					# escaping double quotes
					# not sure this is actually needed
					# after trying, seems to work fine without
					#workingLine = workingLine.replace("\"", "\\\"")
					
					self.helpmsg+=workingLine
					workingLine = fileStream.readline()
				#print(helpmsg)
					
			
#test = Properties()
