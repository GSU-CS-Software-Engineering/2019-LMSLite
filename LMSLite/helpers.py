import csv


class Question:
	type = 0
	label = ''
	answers = []
	cAnswers = []

	def __init__(self, pType, pLabel, pAnswers, cAns):
		self.label = pLabel
		self.answers = pAnswers
		self.cAnswers = cAns
		self.type = pType


def reset_quiz(input, output, post):
	qtype = []

	with open(input, "rt") as fin:
		reader = csv.reader(fin, delimiter='\t')  # parse by tab
		reader = (line for line in reader if line)  # ignore blank lines
		for questy in reader:
			qtype.append(questy)

		fin.close()

	i = 0
	j = 0
	string = 'Question '
	with open(output, "wt") as fout:
		for line in qtype:
			for ans in qtype[i]:
				string += str(i+1)
				if j % 2 != 0 and qtype[i][j] == 'Correct':
					qtype[i][j] = 'Incorrect'

				if qtype[i][0] == 'TF':

					if qtype[i][2] == 'True':
						qtype[i][2] = 'False'
					else:
						qtype[i][2] = 'True'

				if string in post:
					if qtype[i][0] == 'MC':
						qtype[i][qtype[i].index(post[string])+1] = 'Correct'

					elif qtype[i][0] == 'SR' or qtype[i][0] == 'TF' or qtype[i][0] == 'ESS':
						qtype[i][2] = post[string]

					elif qtype[i][0] == 'MA':
						for answer in qtype[i][2:]:
							if answer in post.getlist(string):
								qtype[i][qtype[i].index(answer)+1] = 'Correct'

					elif qtype[i][0] == 'FIB':
						for answer in qtype[i][2:]:
							qtype[i][2] = post[string]


				string = 'Question '
				j += 1
			j = 0
			fout.write('\t'.join(qtype[i]))
			fout.write('\n')
			i += 1
		fout.close()


def create_quiz(input):

	qtype = []
	questions = []

	with open(input, "r") as file:
		reader = csv.reader(file, delimiter='\t')  # parse by tab
		reader = (line for line in reader if line)  # ignore blank lines
		for questy in reader:
			qtype.append(questy)

		i = 0  # initialize index
		while i < len(qtype):

			if qtype[i][0] == "MC":
				questions.append(
					Question(
							pType=1,
							pLabel=qtype[i][1],
							pAnswers=qtype[i][::2],
							cAns=qtype[i][qtype[i].index("Correct") - 1]))
				questions[i].answers = 	questions[i].answers[1:]

			if qtype[i][0] == "SR":  # Short Answer
				questions.append(Question(pType=2, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=qtype[i][2]))

			if qtype[i][0] == "MA":  # Multiple Select
				cAns = []
				for k in range(len(qtype[i])):
					if qtype[i][k] == "Correct":
						cAns.append(qtype[i][k - 1])
				questions.append(Question(pType=3, pLabel=qtype[i][1], pAnswers=qtype[i][2::2], cAns=cAns))

			if qtype[i][0] == "FIB":

				cAns = []
				j = 2
				while j < len(qtype[i]):
					cAns.append((qtype[i][j]))
					j += 1
				questions.append(Question(pType=4, pLabel=qtype[i][1], pAnswers=cAns[0:1], cAns=cAns))

			if qtype[i][0] == "TF":  # True or False
				questions.append(Question(pType=5, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=qtype[i][2]))
			if qtype[i][0] == "ESS":  # Esaay Question
				questions.append(Question(pType=6, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=qtype[i][2]))
			i += 1

	return questions


def grade_quiz(input, key):
	first = []
	second = []

	with open(key, "r") as f1:
		read1 = csv.reader(f1, delimiter='\t')  # parse by tab
		read1 = (line for line in read1 if line)  # ignore blank lines
		for ques in read1:
			first.append(ques)
	with open(input, "r") as f2:
		read2 = csv.reader(f2, delimiter='\t')  # parse by tab
		read2 = (line for line in read2 if line)  # ignore blank lines
		for questy in read2:
			second.append(questy)
	i = 0
	correct = 0
	while i < len(first):
		if first[i][0] == "MC":
			if first[i] == second[i]:
				correct += 1

		if first[i][0] == "TF":
			if first[i] == second[i]:
				correct += 1

		if first[i][0] == "MA":
			j = 3
			while j < len(first[i]):
				if first[i][j] == second[i][j]:
					correct += (1 / ((len(first[i][2:]) / 2)))
				j += 2
		i += 1
	return round(100 *(correct/len(first)),2)

