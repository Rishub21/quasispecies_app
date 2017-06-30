from __future__ import division
#import gevent.monkey
#gevent.monkey.patch_all()
#import gevent
#import gevent.pool

#from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
#from sparc import pipeline
import argparse
from multiprocessing import Pool, freeze_support, Manager
import subprocess
import os
import time
from collections import defaultdict
from pipeline import pipeline

#import multiprocessing.pool

numtime = 1
starttime = time.time()
sampleQueue = defaultdict(str)
#pool = Pool()

#current_directory = os.getcwd()



def mediary(tuple):
	print "mediary started"

	new_Input = tuple[0]
	reference = tuple[1]
	#pool = pool
	print "This is new_Input" + new_Input
	print "This is reference" + reference
	print "calling this mediary function "


	return



def fullrecursionpipeline(*args):

     global starttime
     global numtime
     filename = args[0]
     reference = args[1]
     ranking = args[2]
     startingindex = args[3]
     endingindex = args[4]
     percentagethresh = args[5]
     pvalthresh = args[6]
     read2thresh = args[7]
     snpthresh = args[8]
     passed_dictionary = args[9]
     conbul = args[10]
     consensus_output = args[11]
     consensus_string = args[12]
     headings_string = args[13]
     finalheadings_string = args[14]
     finalconsensus_string  = args[15]
     consensus_dict = args[16]
     headings_output = args[17]

     conbul = args[9]

     global sampleQueue

     cluster_parameters = pipeline(filename, reference, ranking,conbul, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh)  #the initial run will have False for the consenus_bul because we are using the original

     conbul = True
     print "THIS IS FILE NAME" + str(filename)

     rankedfile = str(cluster_parameters[4].strip())


     with open(rankedfile  ,"r") as ranked:
	for line in ranked:
		ranked_amount = int(line.split(None, 1)[0])
		print "THIS IS NUMBER OF RANKED " + str(ranked_amount)
  		break

	print "THIS IS SNP THRESH" + str(snpthresh)
	if ranked_amount  >= snpthresh:
		adjustedQueue = dict(sampleQueue)
	 	for key in adjustedQueue:
	 		if key == str(filename):
	 			del sampleQueue[filename]

		#command = "java -classpath .:/usr/local/MATLAB/MATLAB_Runtime/v91/toolbox/javabuilder/jar/javabuilder.jar:/mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/scripts/SigClust/for_testing/SigClust.jar getClust /mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/rishub_backup/testing_brad/djangoProject\ copy/cluster_interface/" + cluster_parameters[3] + " /mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/rishub_backup/testing_brad/djangoProject\ copy/cluster_interface/" + cluster_parameters[4] + " " + cluster_parameters[6]
		command = "java -classpath .:/usr/local/MATLAB/MATLAB_Runtime/v91/toolbox/javabuilder/jar/javabuilder.jar:/mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/scripts/selfTuned_sigClust/for_testing/SigClust.jar getClust /mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/rishub_backup/rerun/" + cluster_parameters[3] + " /mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/rishub_backup/rerun/" + cluster_parameters[4] + " " + cluster_parameters[6]

		#command = "java -classpath .:/usr/local/MATLAB/MATLAB_Runtime/v91/toolbox/javabuilder/jar/javabuilder.jar:/mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/scripts/SigClust/for_testing/SigClust.jar getClust /mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/rishub_backup/xiaoli_bwa/" + cluster_parameters[3] + " /mnt/LHRI/Bioinformatics/Projects/Quasispecies/manuscript/rishub_backup/xiaoli_bwa/" + cluster_parameters[4] + " " + cluster_parameters[6]



		print command
		subprocess.call(command, shell =True)
		cluster_directory = str(cluster_parameters[6]) + "_clusters"
		print ("THIS IS CLUSTER DIRECTORY: " + cluster_directory)


	 	with open(cluster_directory,"r") as clusteroutput:

			for line in clusteroutput:
				clusterheading = line.strip()
				sampleQueue[clusterheading] = False
		with open(cluster_directory, "r") as clusteroutput:
			for line in clusteroutput:
				clusterlist = []
                                clusterheading = line.strip()
                                command = "java -cp ../script/ Fastq_filter_by_readID " + filename+ ".fastq " + clusterheading # the cluster program will create clusterheading files in the output folder so thats what you are using here. Output/clusterheading is the actual file that is located in the output folder. remember the clusterheading b$
                                print command
                                print "analyzing the " + str(numtime) + "SUBCLUSTERs"
                                subprocess.call(command, shell = True)
                                newInput =   clusterheading
                                print "THIS IS THE NEXT INPUT" + newInput
                                newReference = cluster_parameters[2] # the consensus file of the previous cluster
                                numtime +=1
                                newTuple = (newInput, newReference )
                                clusterlist.append(newTuple)
                                print "************************Recursive Call*************************"
				fullrecursionpipeline(newInput, newReference, ranking, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh, passed_dictionary, True, consensus_output,consensus_string, headings_string, finalheadings_string, finalconsensus_string, consensus_dict,
                                headings_output)

		print str(time.time()-starttime)

	else:
		sampleQueue[cluster_parameters[6]] = True # the initial sample is done, has no more subclusters in it
		print "THIS IS SAMPLE QUEUE"
		print cluster_parameters[6]
		print sampleQueue

		command = "cat " + str(cluster_parameters[2]) + " >> " + str(consensus_string)
		subprocess.call(command, shell = True)

		command = "echo " + str(cluster_parameters[6]) + " >> " + str(headings_string)

		consensus_dict[cluster_parameters[6]]  =cluster_parameters[2]


		subprocess.call(command, shell = True)




		bul_counter = 0
		for value in sampleQueue.values() :
			print "checking"
			if value == True:
				bul_counter+=1
				print "BUL COUNT"
				print bul_counter
				print len(sampleQueue)
				if bul_counter ==  len(sampleQueue):
					print "END OF PIPELINE " + finalconsensus_string + " " + finalheadings_string
					print "Pipeline took this much time : " + str(time.time()-starttime)
					total_lines = 0
					for key in sampleQueue:
						var = str(key) + ".fastq"
						total_lines += sum(1 for line in open(str(var)))


					for key in sampleQueue:
						print key
						headings_output.write(str(key))
						headings_output.write("\n")

						num_lines = sum(1 for line in open(var))

						for element in consensus_dict :
							if key == element:
								#consensus_output.write(str(element) + "\n")
								with open(str(consensus_dict[element]), "r") as consensus:
									#next(consensus)
									for line in consensus:
										for c in line:
											if c is ">":
												perc_int = (num_lines/total_lines) * 100
												perc_int = round(perc_int, 2)
												print "this is num_lines " + str(num_lines)
												print "this is total lines " + str(total_lines)
												num_string = " Freq: " + str(perc_int) + "% "
												print "this is nums_string" + num_string
												line = line.replace(".consensus", num_string)
												#line += str(num_lines)
												#lines = line.strip("\n")
										consensus_output.write(line)




					print sampleQueue
					command = "rm " + finalheadings_string + " " + finalconsensus_string
                                        subprocess.call(command, shell = True)
                                        command = "python matcher.py " + headings_string + " " + consensus_string
                                        subprocess.call(command, shell = True)

if __name__ == "__main__":


	var = subprocess.Popen("nproc", stdout = subprocess.PIPE)
	nproc = var.stdout.read() # number of cores on machine

        print "THIS IS MAIN FUNCTION"
        consensus_string = filename + "_Quasi_strains.fasta"
        finalconsensus_string = filename + "_final" + "_Quasi_strains.fasta"

        clearing_string = open((filename + "_Quasi_strains.fasta"), "w")
        clearing_string.close()

	clearing_consensusstring = open(finalconsensus_string, "w")
	clearing_consensusstring.close()

        headings_string = filename + "_leaves"
        finalheadings_string = filename + "_final" + "_leaves"

	clearing_headingsstring = open(headings_string, "w")
	clearing_headingsstring.close()

        consensus_output = open(finalconsensus_string, "a+")
	headings_output = open(finalheadings_string, "w+")

	consensus_dict = defaultdict(str)

  	#pool = gevent.pool.Pool(int(nproc))
	#pool.join()
