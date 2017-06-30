from celery.decorators import task 
from linearQuasiSeq import pipeline
import os


@task(name = "pipeline_driver")
def pipeline_driver(outDir,uploaded_name, referencefilename, ranking_method, startingindex, endingindex, percentagethresh, pvalthresh, read2thresh, snpthresh):
	print("**************Calling Pipeline*************")
	print("************My task id is: "+pipeline_driver.request.id+"***************")
	
	outDir=outDir+pipeline_driver.request.id+"/"
	
	try:
		os.makedirs(outDir)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(outDir):
			pass
		else:
			raise
			
	os.rename("tmp/"+uploaded_name+".fastq", outDir+uploaded_name+".fastq")
	os.rename("tmp/"+referencefilename, outDir+referencefilename)
	
	pipeline(outDir,outDir+uploaded_name+".fastq", outDir+referencefilename, uploaded_name, ranking_method, None)
