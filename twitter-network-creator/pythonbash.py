import subprocess
print "start"
res = subprocess.check_output(["bash", "unzipper"])
print res
print "end"