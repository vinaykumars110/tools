import sys
import os

def add_to_path():
	cwd = os.getcwd()
	if 'skvinay' in cwd:
		sys.path.insert(0, 'C:/Users/skvinay/PycharmProjects/MyProjects/')
		sys.path.append('C:/Users/skvinay/Appdata/')
	else:
		sys.path.insert(0,os.path.dirname(__file__)+'/../')

def main():
	add_to_path()

if __name__ == "__main__":
	main()
