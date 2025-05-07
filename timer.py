from time import sleep
import re
import playsound
from tkinter import *
from threading import Thread

try:
	def startTimer(query):
		nums = re.findall(r'[0-9]+', query)
		time = 0
		if "minute" in query and "second" in query:
			time = int(nums[0])*60 + int(nums[1])
		elif "minute" in query:
			time = int(nums[0])*60
		elif "second" in query:
			time = int(nums[0])
		else:
			return

		print("Timer Started")
		sleep(time)
		Thread(target=timer).start()


	def timer():
		print("Timer Ended")
		return ()
except Exception as e:
	print("An Error Occured: ", e)

if __name__ == "__main__":
	startTimer("set a timer for 3 seconds")

