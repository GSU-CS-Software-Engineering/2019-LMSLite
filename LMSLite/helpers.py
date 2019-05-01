import csv

from django.core.files.storage import default_storage
import smtplib


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
	with default_storage.open(output, "wt") as fout:
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
		return fout


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
				if 'Correct' in qtype[i]:

					questions.append(
						Question(
								pType=1,
								pLabel=qtype[i][1],
								pAnswers=qtype[i][::2],
								cAns=qtype[i][qtype[i].index("Correct") - 1]))
					questions[i].answers = 	questions[i].answers[1:]
				else:
					questions.append(
						Question(
							pType=1,
							pLabel=qtype[i][1],
							pAnswers=qtype[i][::2],
							cAns=[]))
					questions[i].answers = questions[i].answers[1:]

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
	gradeable=0
	while i < len(first):
		if first[i][0] == "MC":
			gradeable += 1
			if first[i] == second[i]:
				correct += 1

		if first[i][0] == "TF":
			gradeable += 1
			if first[i] == second[i]:
				correct += 1

		if first[i][0] == "MA":
			j = 3
			gradeable += 1
			correctCounter = 0
			incorrectCounter = 0
			studentCorrectCounter = 0
			while j < len(first[i]):
				if first[i][j] == "Correct":
					correctCounter += 1
				if first[i][j] == second[i][j] and first[i][j] == "Correct":
					studentCorrectCounter += 1 # (1 / ((len(first[i][2:]) / 2)))
				elif first[i][j] == "Incorrect" and second[i][j] == "Correct":
					incorrectCounter += 1
				elif second[i][j] == "Incorrect" and first[i][j] == "Correct":
					incorrectCounter += 0
				j += 2
			if ((1/correctCounter*studentCorrectCounter)-(1/correctCounter*incorrectCounter)) >= 0:
				correct += (1/correctCounter*studentCorrectCounter)-(1/correctCounter*incorrectCounter)
			else:
				correct += 0
		i += 1
	return round(100 *(correct/gradeable),2)

def send_email(students, assignment):

	emails = []

	for student in students:
		emails.append(student.email)


	for i in range(len(emails)):

		if assignment.type == 0:
			s = smtplib.SMTP('smtp.zoho.com', 587)
			s.starttls()
			s.login("lmslite.no-reply@gsulms.com", "openLMS2019*")
			message = "Subject:{subj}\n\n" \
					  "{prof} has posted a new {type}.\n" \
					  "Course: {course}\n" \
					  "Assignment: {name}\n" \
					  "Due Date: {date}".format(
				subj=assignment.course_id.course_name,
				prof=assignment.prof.first_name +" "+ assignment.prof.last_name,
				type="Survey",
				course=assignment.course_id.course_name,
				name=assignment.assignment_name,
				date=assignment.due_date)

		elif assignment.type == 1:
			s = smtplib.SMTP('smtp.zoho.com', 587)
			s.starttls()
			s.login("lmslite.no-reply@gsulms.com", "openLMS2019*")
			message = "Subject:{subj}\n\n" \
					  "{prof} has posted a new {type}.\n" \
					  "Course: {course}\n" \
					  "Assignment: {name}\n" \
					  "Due Date: {date}".format(
				subj=assignment.course_id.course_name,
				prof=assignment.prof.first_name +" "+ assignment.prof.last_name,
				type="Survey",
				course=assignment.course_id.course_name,
				name=assignment.assignment_name,
				date=assignment.due_date)

		elif assignment.type == 2:
			s = smtplib.SMTP('smtp.zoho.com', 587)
			s.starttls()
			s.login("lmslite.no-reply@gsulms.com", "openLMS2019*")
			message = "Subject:{subj}\n\n" \
					  "{prof} has posted a new {type}.\n" \
					  "Course: {course}\n" \
					  "Assignment: {name}\n" \
					  "Due Date: {date}".format(
				subj=assignment.course_id.course_name,
				prof=assignment.prof.first_name +" "+ assignment.prof.last_name,
				type="Survey",
				course=assignment.course_id.course_name,
				name=assignment.assignment_name,
				date=assignment.due_date)

		s.sendmail("lmslite.no-reply@gsulms.com", emails[i], message)
		s.quit()


def update_quiz(input, post):
	n = 1
	for key, value in post.items():
		if key.startswith("Question "):
			n = n + 1

	# prints out each question with answers
	with default_storage.open(input, 'w+b') as file:
		for i in range(1, n):
			for key, value in post.items():
				if ('Question%stype' % i) in post:
					if post['Question%stype' % i] == '1':
						post['Question%stype' % i] = 'MC'
						file.write("%s\t%s\t" % (post['Question%stype' % i], post['Question %s' % i]))
						bool = False
						for key, value in post.items():
							if key == ('Question%sRadioGrp' % i):
								bool = True

							if key.startswith("Question%sAnswer" % i):
								if bool:
									file.write("{value}\t{val}\t".format(value=value, val='Correct'))
									bool = False

								else:
									file.write("{value}\t{val}\t".format(value=value, val='Incorrect'))
						file.write("\n")

					if post['Question%stype' % i] == '2':
						post['Question%stype' % i] = 'SR'
						file.write("%s\t%s\t%s\n" % (
						post['Question%stype' % i], post['Question %s' % i], post['Question%sAnswer1' % i]))

					if post['Question%stype' % i] == '3':
						post['Question%stype' % i] = 'MA'
						file.write("%s\t%s\t" % (post['Question%stype' % i], post['Question %s' % i]))
						for key, value in post.items():
							if key.startswith("Question%sAnswer" % i):
								if value[0] in post['Question%sCheckboxGrp' % i]:
									file.write("{value}\t{bool}\t".format(value=(value), bool='Correct'))
								else:
									file.write("{value}\t{bool}\t".format(value=(value), bool='Incorrect'))
						file.write("\n")

					if post['Question%stype' % i] == '4':
						post['Question%stype' % i] = 'FIB'
						file.write("%s\t%s\t%s\n" % (
						post['Question%stype' % i], post['Question %s' % i], post['Question%sAnswer1' % i]))

					if post['Question%stype' % i] == '5':
						post['Question%stype' % i] = 'TF'
						file.write("%s\t%s\t%s\n" % (
						post['Question%stype' % i], post['Question %s' % i], post['Question%sAnswer1' % i]))

					if post['Question%stype' % i] == '6':
						post['Question%stype' % i] = 'ESS'
						file.write("%s\t%s\t%s\n" % (
						post['Question%stype' % i], post['Question %s' % i], post['Question%sAnswer1' % i]))
		file.close()
