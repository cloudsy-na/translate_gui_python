from tkinter import *
import googletrans
import textblob
from tkinter import ttk, messagebox
import csv
import os

root = Tk()
root.title('GAPI Translator')
root.geometry("880x350")
root.config(background="#a3aca9")


def translate_it():
	# Delete Any Previous Translations
	translatedText.delete(1.0, END)

	try:
		# Get Languages From Dictionary Keys
		# Get the From Language Key
		for key, value in languages.items():
			if (value == originalCombo.get().lower()):
				fromLanguageKey = key

		# Get the To Language Key
		for key, value in languages.items():
			if (value == translatedCombo.get().lower()):
				toLanguageKey = key

		# Turn Original Text into a TextBlob
		words = textblob.TextBlob(originalText.get(1.0, END))

		# Translate Text
		words = words.translate(from_lang=fromLanguageKey , to=toLanguageKey)

		# Output translated text to screen
		translatedText.insert(1.0, words)

	except Exception as e:
		messagebox.showerror("Translator", e)


def clear():
	# Clear the text boxes
	originalText.delete(1.0, END)
	translatedText.delete(1.0, END)


def save():
	#get from - to language
	fromLanguage = originalCombo.get()
	toLanguage = translatedCombo.get()

	#get original - translated text
	originalTextList = originalText.get(1.0,END).strip().split("\n")
	translatedTextList = translatedText.get(1.0,END).strip().split("\n")
	
	# Create new file & writing the data into the file
	# modifying from https://www.geeksforgeeks.org/writing-data-from-a-python-list-to-csv-row-wise/
	filename = "output"
	extformat = '.csv'
	file = open(filename + extformat, 'w+', newline ='')
	with file:
		header = [fromLanguage, toLanguage]
		writer = csv.DictWriter(file, fieldnames = header)

		writer.writeheader()
		for i in range(0, len(originalTextList)):
			writer.writerow({fromLanguage : originalTextList[i], toLanguage: translatedTextList[i]})
	
	messagebox.showinfo("Exported", "CSV file exported at {directory}{filename}".format(
		directory = os.getcwd() + "\\", 
		filename = filename + extformat
	))

# Grab Language List From GoogleTrans
languages = googletrans.LANGUAGES

# Convert to list
languageList = list(languages.values())

#Proper case (english -> English, scots gaelic -> Scots Gaelic)
for i in range(0, len(languageList)):
	languageList[i] = languageList[i].title()

# Text Boxes
originalText = Text(root, height=10, width=40)
originalText.grid(row=2, column=0, pady=20, padx=10)

translateButton = Button(root, text="Translate!", font=("Helvetica", 24),
                    activebackground="#51cc0e", command=translate_it)
translateButton.grid(row=2, column=1, padx=10)

translatedText = Text(root, height=10, width=40)
translatedText.grid(row=2, column=2, pady=20, padx=10)

# Combo boxes
originalCombo = ttk.Combobox(root, width=50, value=languageList)
originalCombo.current(21)
originalCombo.grid(row=3, column=0)

translatedCombo = ttk.Combobox(root, width=50, value=languageList)
translatedCombo.current(43)
translatedCombo.grid(row=3, column=2)

# Clear button
clearButton = Button(root, text="Clear", command=clear,activebackground="red",height=2, width=7,font="Normal 10 bold")
clearButton.grid(row=4, column=1)

# export button
exportButton=Button(root, text="Save Result", command=save, activebackground="light green",
                height=2, width=15,font="Normal 10 bold")
exportButton.grid(row=5, column=1,pady=20,padx=10)

root.mainloop()
