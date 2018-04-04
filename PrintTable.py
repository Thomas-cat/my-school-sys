import re
color_dict = {'green':"\033[1;32m",
	      'yellow':"\033[1;33m",
	      'red':"\033[1;31m",
	      'blue':"\033[1;34m",
	      'purple':"\033[1;35m",
	      'green_blue':"\033[1;36m",
	      'no_color':"\033[0m"}
class printtable():
	reg_color = re.compile(r'^{(.*?)}')
	reg_code =re.compile(r'\x1b.*?m')
	def cal_count(self,string):
		lengthA = len(string)
		lengthB = len(string.encode('utf-8'))
		a = re.compile(r'[^\x00-\xff]+')
		remove_string = a.sub('',string)
		remove_count = len(remove_string)
		lengthC = lengthA-remove_count
		if lengthA!=lengthB:
			lengthA = 2*lengthC + remove_count
		return lengthA
	def __init__(self,table_name,padding_width = 1,column_sign = '|',row_sign = '+',color = 'green'):
		self.table_name = table_name	
		self.row_data = []
		if isinstance(table_name,list): 
			for item in table_name:
				if not isinstance(item,str):
					print ('需要str元素\n')
					return None
		else:
			print ('需要list列表')
			return None
		self.get_row_count()
		self.padding_width = padding_width
		self.row_sign = row_sign
		self.column_sign = column_sign
		self.color = color
	def add_row(self,row_list):
		if self.row_count != len(row_list):
			print ('count error')
			return 
		self.row_data.append(row_list)
	def add_column(self,column_list):
		self.column_data.append(column_list)
	def add_color(self,string):
		try:
			color_code = color_dict.get(self.reg_color.findall(string)[0].strip())
			color_end_code = color_dict.get('no_color')
			return self.reg_color.sub(color_code,string)+color_end_code
		except:
			return string
	def cut_color(self,string):
		tmp =  self.reg_code.sub('',self.reg_color.sub('',string))
		return tmp
	def get_maxlength(self):
		maxlengthA = self.cal_count(self.cut_color(sorted(self.table_name,key=lambda x:self.cal_count(self.cut_color(x)),reverse=True)[0]))
		maxlengthB = 0
		for item in self.row_data:
			tmp = self.cal_count(self.cut_color(sorted(item,key=lambda x:self.cal_count(self.cut_color(x)),reverse=True)[0]))
			if maxlengthB < tmp:
				maxlengthB = tmp
		self.maxlength = max(maxlengthA,maxlengthB)
		return self.maxlength

	def get_row_count(self):
		self.row_count = len(self.table_name)
	def deal_string(self,max_count,string):
		string_count = self.cal_count(self.cut_color(string))
		space_count = int((max_count - string_count-1)/2)
		tmp = self.column_sign+' '*space_count+self.add_color(string)
		tmp+=(max_count-self.cal_count(self.cut_color(tmp)))*' '
		return tmp
		
			
	def print_string(self):
		self.get_maxlength()
		row_sign_count =self.maxlength+self.padding_width*2+1
		row_sign_all_count = row_sign_count*self.row_count+1
		start_end_string =self.row_sign*(row_sign_all_count)+'\n'

		tmp_string = ''
		tmp_string+=start_end_string
		tmp_list = []
		tmp_list.append(self.table_name)
		for item in self.row_data:
			tmp_list.append(item)

		for string_list in tmp_list:
			for string in string_list:
				tmp_string+=self.deal_string(row_sign_count,string)
			tmp_string+=self.column_sign+'\n'+start_end_string
		return tmp_string
	def get_string(self):
		tmp = self.print_string()
		return tmp
	def __str__(self):
		tmp = self.print_string()
		return tmp


