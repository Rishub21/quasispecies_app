# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from random import randint
import subprocess
from collections import defaultdict
#import gevent.monkey
#gevent.monkey.patch_all()
#import gevent
from multiprocessing import Pool
import multiprocessing.pool
import errno
from celery.result import AsyncResult

import calendar
import time
import os

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
#from driver import fullrecursionpipeline
#from sparc import pipeline
#from linearQuasiSeq import pipeline
from tasks import pipeline_driver
#from driver import mediary

#from linear_sparc import fullrecursionpipeline, mediary
from multiprocessing import Pool, freeze_support, Manager

# Create your views here.

def index(request):
	#return render(request, "cluster_app/chart.html")
	response = render(request, "cluster_app/intro_form.html")

	var = subprocess.Popen("nproc", stdout = subprocess.PIPE)
	nproc = var.stdout.read() # number of cores on machine
#	pool = gevent.pool.Pool(int(nproc))

	#test(session_id)

	#currentTask=None
	if(request.method == "POST"):

		if(request.POST.get("flu_submit")):
			return redirect("fluData")

		if(request.POST.get("hiv19_submit")):
			return redirect("hivData")

		if(request.POST.get("Pro4mix")):
			return redirect("Pro4mix")



		session_id="quasiSeq_"+str(int(calendar.timegm(time.gmtime())))
		outDir="/data/quasiSeqOut/" #+session_id+"/"
		tmpDir="tmp/"
		try:
			os.makedirs(outDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(outDir):
				pass
			else:
				raise
		try:
			os.makedirs(tmpDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(tmpDir):
				pass
			else:
				raise

		print ("Session key:"+session_id)
		#num = randint(100000,999999)
		num = 99999
		#sess = request.session.session_key
		#request.session["ID"] = num
		uploaded_file = request.FILES['my_file']
		uploaded_name = request.FILES["my_file"].name
		uploaded_name = uploaded_name.strip(".fastq")
		samplefilename = uploaded_name + ".fastq"

		with open(tmpDir+samplefilename , "wb+") as samplefile: # add the plus so that it will create the file if it does not exist
			# get the session ID and append that to sampleID.txt file name so that it is a different file for every user and the same file does not get overwritten
			for chunk in uploaded_file.chunks():
				samplefile.write(chunk)

		reference_file = request.FILES["reference_file"]
		uploaded_reference = request.FILES["reference_file"].name
		#uploaded_reference = uploaded_reference.strip("fasta")
		referencefilename= uploaded_reference

		with open(tmpDir+referencefilename, "wb+") as  referencefile :
			for chunk in reference_file.chunks():
				referencefile.write(chunk)

		ranking_method = request.POST["rank"]
		print ranking_method


		#fullrecursionpipeline(filename, reference, ranking, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh, False, pool)
		startingindex = request.POST["start"]
		endingindex = request.POST["end"]

		if startingindex == None:
			startingindex = 0

		percentagethresh = request.POST["perc"]
		pvalthresh = request.POST["pval"]
		read2thresh = request.POST["read2"]
		snpthresh = request.POST.get("snp")

		print "THIS IS THE FIRST VALUE OF SNPTHRESH" + str(snpthresh)

		if percentagethresh == None:
			percentagethresh = 1.0
		if pvalthresh == None:
			pvalthresh = .001
		if read2thresh == None:
			read2thresh = 10
		if snpthresh == None:
			snpthresh = 10
		snpthresh = 10
		print "I AM SETTING SNP THRESH TO " + str(snpthresh)


		print "THIS IS MAIN FUNCTION"


		print "THESE ARE INPUTS" + str(uploaded_name) + str(referencefile)

		currentTask=pipeline_driver.delay(outDir,uploaded_name, referencefilename, ranking_method, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh)

		return redirect("result", currentTask.task_id, uploaded_name)
	else:
		return response


def fluData(request):
	response = render(request, "cluster_app/intro_form_flu.html")
	session_id="quasiSeq_"+str(int(calendar.timegm(time.gmtime())))
	outDir="/data/quasiSeqOut/" #+session_id+"/"
	tmpDir="tmp/"

	if (request.method == "POST"):

		if(request.POST.get("flu_submit")):
			return redirect("fluData")

		if(request.POST.get("hiv19_submit")):
			return redirect("hivData")

		if(request.POST.get("Pro4mix")):
			return redirect("Pro4mix")

		if (request.POST.get("home")):
			return redirect("index")
		try:
			os.makedirs(outDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(outDir):
				pass
			else:
				raise
		try:
			os.makedirs(tmpDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(tmpDir):
				pass
			else:
				raise

		print ("Session key:"+session_id)
		uploaded_file = "/data/examples/flu10mix_FL_ccs.fastq"
		uploaded_name = "flu10mix_FL_ccs.fastq"
		uploaded_name = uploaded_name.strip(".fastq")
		samplefilename = uploaded_name + ".fastq"
		opened_file = open(uploaded_file, "r")
		with open(tmpDir+samplefilename , "wb+") as samplefile: # add the plus so that it will create the file if it does not exist
			# get the session ID and append that to sampleID.txt file name so that it is a different file for every user and the same file does not get overwritten
			for line in opened_file:
				samplefile.write(line)

		reference_file = "/data/examples/flu1PB.fa"
		uploaded_reference = "flu1PB.fa"
		#uploaded_reference = uploaded_reference.strip("fasta")
		referencefilename= uploaded_reference
		opened_ref_file = open(reference_file, "r")

		with open(tmpDir+referencefilename, "wb+") as  referencefile :
			for line in opened_ref_file:
				referencefile.write(line)

		ranking_method = request.POST.get("rank")
		print ranking_method


		#fullrecursionpipeline(filename, reference, ranking, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh, False, pool)
		startingindex = request.POST.get("start")
		endingindex = request.POST.get("end")

		if startingindex == None:
			startingindex = 0

		percentagethresh = request.POST.get("perc")
		pvalthresh = request.POST.get("pval")
		read2thresh = request.POST.get("read2")
		snpthresh = request.POST.get("snp")

		print "THIS IS THE FIRST VALUE OF SNPTHRESH" + str(snpthresh)

		if ranking_method == None:
			ranking_method  = "percentage"
		if percentagethresh == None:
			percentagethresh = 1.0
		if pvalthresh == None:
			pvalthresh = .001
		if read2thresh == None:
			read2thresh = 10
		if snpthresh == None:
			snpthresh = 10
		snpthresh = 10
		print "I AM SETTING SNP THRESH TO " + str(snpthresh)


		print "THIS IS MAIN FUNCTION"


		print "THESE ARE INPUTS" + str(uploaded_name) + str(referencefile)

		currentTask=pipeline_driver.delay(outDir,uploaded_name, referencefilename, ranking_method, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh)

		return redirect("result", currentTask.task_id, uploaded_name)
	else:
		return response


def hivData(request):
	response = render(request, "cluster_app/intro_form_HIV.html")
	session_id="quasiSeq_"+str(int(calendar.timegm(time.gmtime())))
	outDir="/data/quasiSeqOut/" #+session_id+"/"
	tmpDir="tmp/"

	if (request.method == "POST"):

		if(request.POST.get("flu_submit")):
			return redirect("fluData")

		if(request.POST.get("hiv19_submit")):
			return redirect("hivData")

		if(request.POST.get("Pro4mix")):
			return redirect("Pro4mix")

		if (request.POST.get("home")):
			return redirect("index")
		try:
			os.makedirs(outDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(outDir):
				pass
			else:
				raise
		try:
			os.makedirs(tmpDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(tmpDir):
				pass
			else:
				raise



		print ("Session key:"+session_id)
		uploaded_file = "/data/examples/hiv19_FL_subreads.fastq"
		uploaded_name = "hiv19_FL_subreads.fastq"
		uploaded_name = uploaded_name.strip(".fastq")
		samplefilename = uploaded_name + ".fastq"
		opened_file = open(uploaded_file, "r")
		with open(tmpDir+samplefilename , "wb+") as samplefile: # add the plus so that it will create the file if it does not exist
			# get the session ID and append that to sampleID.txt file name so that it is a different file for every user and the same file does not get overwritten
			for line in opened_file:
				samplefile.write(line)

		reference_file = "/data/examples/HxB2_700.fasta"
		uploaded_reference = "HxB2_700.fasta"
		#uploaded_reference = uploaded_reference.strip("fasta")
		referencefilename= uploaded_reference
		opened_ref_file = open(reference_file, "r")

		with open(tmpDir+referencefilename, "wb+") as  referencefile :
			for line in opened_ref_file:
				referencefile.write(line)

		ranking_method = request.POST.get("rank")
		print ranking_method


		#fullrecursionpipeline(filename, reference, ranking, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh, False, pool)
		startingindex = request.POST.get("start")
		endingindex = request.POST.get("end")

		if startingindex == None:
			startingindex = 0

		percentagethresh = request.POST.get("perc")
		pvalthresh = request.POST.get("pval")
		read2thresh = request.POST.get("read2")
		snpthresh = request.POST.get("snp")

		print "THIS IS THE FIRST VALUE OF SNPTHRESH" + str(snpthresh)

		if ranking_method == None:
			ranking_method  = "percentage"
		if percentagethresh == None:
			percentagethresh = 1.0
		if pvalthresh == None:
			pvalthresh = .001
		if read2thresh == None:
			read2thresh = 10
		if snpthresh == None:
			snpthresh = 10
		snpthresh = 10
		print "I AM SETTING SNP THRESH TO " + str(snpthresh)


		print "THIS IS MAIN FUNCTION"


		print "THESE ARE INPUTS" + str(uploaded_name) + str(referencefile)

		currentTask=pipeline_driver.delay(outDir,uploaded_name, referencefilename, ranking_method, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh)

		return redirect("result", currentTask.task_id, uploaded_name)
	else:
		return response


def Pro4mix(request):
	response = render(request, "cluster_app/intro_form_promix.html")
	session_id="quasiSeq_"+str(int(calendar.timegm(time.gmtime())))
	outDir="/data/quasiSeqOut/" #+session_id+"/"
	tmpDir="tmp/"

	if (request.method == "POST"):

		if(request.POST.get("flu_submit")):
			return redirect("fluData")

		if(request.POST.get("hiv19_submit")):
			return redirect("hivData")

		if(request.POST.get("Pro4mix")):
			return redirect("Pro4mix")

		if (request.POST.get("home")):
			return redirect("index")
		try:
			os.makedirs(outDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(outDir):
				pass
			else:
				raise
		try:
			os.makedirs(tmpDir)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(tmpDir):
				pass
			else:
				raise


		print ("Session key:"+session_id)
		uploaded_file = "/data/examples/pro4mix_FL_ccs.fastq"
		uploaded_name = "pro4mix_FL_ccs.fastq"
		uploaded_name = uploaded_name.strip(".fastq")
		samplefilename = uploaded_name + ".fastq"
		opened_file = open(uploaded_file, "r")
		with open(tmpDir+samplefilename , "wb+") as samplefile: # add the plus so that it will create the file if it does not exist
			# get the session ID and append that to sampleID.txt file name so that it is a different file for every user and the same file does not get overwritten
			for line in opened_file:
				samplefile.write(line)

		reference_file = "/data/examples/HxB2_700.fasta"
		uploaded_reference = "HxB2_700.fasta"
		#uploaded_reference = uploaded_reference.strip("fasta")
		referencefilename= uploaded_reference
		opened_ref_file = open(reference_file, "r")

		with open(tmpDir+referencefilename, "wb+") as  referencefile :
			for line in opened_ref_file:
				referencefile.write(line)

		ranking_method = request.POST.get("rank")
		print ranking_method


		#fullrecursionpipeline(filename, reference, ranking, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh, False, pool)
		startingindex = request.POST.get("start")
		endingindex = request.POST.get("end")

		if startingindex == None:
			startingindex = 0

		percentagethresh = request.POST.get("perc")
		pvalthresh = request.POST.get("pval")
		read2thresh = request.POST.get("read2")
		snpthresh = request.POST.get("snp")

		print "THIS IS THE FIRST VALUE OF SNPTHRESH" + str(snpthresh)

		if ranking_method == None:
			ranking_method  = "percentage"
		if percentagethresh == None:
			percentagethresh = 1.0
		if pvalthresh == None:
			pvalthresh = .001
		if read2thresh == None:
			read2thresh = 10
		if snpthresh == None:
			snpthresh = 10
		snpthresh = 10
		print "I AM SETTING SNP THRESH TO " + str(snpthresh)


		print "THIS IS MAIN FUNCTION"


		print "THESE ARE INPUTS" + str(uploaded_name) + str(referencefile)

		currentTask=pipeline_driver.delay(outDir,uploaded_name, referencefilename, ranking_method, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh)

		return redirect("result", currentTask.task_id, uploaded_name)
	else:
		return response



def result(request,taskId, uploaded_name):

	taskResult=AsyncResult(taskId)
	taskState=taskResult.state
	statusbul = False
	specieslist = []
	if (taskState == "SUCCESS") :
		statusbul = True
		"""
		path =  "/data/quasiSeqOut/" + str(taskId) + "/" + uploaded_name + ".consensus.fasta"

		filename = open(path, "r")
		response = HttpResponse(filename, content_type = "text/csv")
		response["Content-Disposition"] = "attachment; filename = consensus.fasta"

		return response
		"""
		specieslist = []
		labellist = []
		valuelist = []
		counter = 0
		with open("/data/examples/final_10clones_FL_redirected_3_1_1_1_leaves", "r") as readfile :
			for line in readfile:
				linelist = line.split(",")
				specieslist.append(linelist)
				counter +=1

		for lister in specieslist:
				labellist.append(str(str((lister[1]).strip("\n")).strip("'")))
				valuelist.append(int(lister[0]))
		labellist = labellist[:-1] # here we are removing the last element that is just the total
 		valuelist = valuelist[:-1]

		#labellist = ["10clones1", "10clones2", "10clones3"]


		if(request.method == "POST"):
			return redirect("downloadFile", taskId, uploaded_name)

		response = render(request, "cluster_app/results.html", {"taskState" : taskState, "taskId" : taskId, "statusbul" : statusbul, "uploaded_name" : uploaded_name, "specieslist": specieslist, "labellist" : labellist,  "valuelist" : valuelist })
		return response

	url = request.get_full_path()
	return HttpResponse("Task status is: "+taskState+" Copy and paste this url " + str("http://128.231.20.59:8000") + url + "\n" " to check for results" )


def downloadFile(request, taskId, uploaded_name):
		path =  "/data/quasiSeqOut/" + str(taskId) + "/" + uploaded_name + ".consensus.fasta"

		filename = open(path, "r")
		response = HttpResponse(filename, content_type = "text/csv")
		response["Content-Disposition"] = "attachment; filename = consensus.fasta"

		return response



	#	ref_file = request.FILES['reference_file']
