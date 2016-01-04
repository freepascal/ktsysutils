import os
import threading
import getpass

def javac(sourceDir, classesDir, successCallback = None, errorCallback = None):
	if (not os.path.isdir(sourceDir)) or os.path.isfile(classesDir):
		if hasattr(errorCallback, '__call__'):
			errorCallback()
	javaWilcardDirectories = ''			
	for(dirpath, dirnames, filenames) in os.walk(sourceDir):
		flag_hasJavaFile = False
		for f in filenames:
			if f.endswith('.java'):
				flag_hasJavaFile = True
				break
		if flag_hasJavaFile:
			javaWilcardDirectories += dirpath + '/' + '*.java'
			flag_hasJavaFile = False
			
	#make user has permissions on classesDir	
	if not os.path.isdir(classesDir):
		t_mkdir = threading.Thread(
			target = os.makedirs,
			args = (classesDir,)
		)
		t_mkdir.start()
		t_mkdir.join()	
			
	#javac -d [classesDir] -classpath [classesDir] package1/*.java package2/*.java
	javaccmd = 'sudo javac -d {0} -classpath {1} {2}'.format(
		classesDir,
		classesDir,
		javaWilcardDirectories
	)	
	
	if os.system(javaccmd) == 0:		
		chowncmd = 'sudo chown -R {0}:users {1}'.format(getpass.getuser(), classesDir)	
		t_usertodo = threading.Thread(
			target = os.system,
			args = (chowncmd,)
		)
		t_usertodo.start()
		t_usertodo.join()
		if hasattr(successCallback, '__call__'):
			successCallback()
	else:
		if hasattr(errorCallback, '__call__'):
			errorCallback()	
