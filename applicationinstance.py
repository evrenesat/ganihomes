import os
import os.path
import time
from sys import exit
 
#class used to handle one application instance mechanism
class ApplicationInstance:
 
    #specify the file used to save the application instance pid
    def __init__( self, pid_file ):
        self.pid_file = pid_file
        self.check()
        self.startApplication()
 
    #check if the current application is already running
    def check( self ):
        #check if the pidfile exists
        if not os.path.isfile( self.pid_file ):
            return
 
        #read the pid from the file
        pid = 0
        try:
            file = open( self.pid_file, 'rt' )
            data = file.read()
            file.close()
            pid = int( data )
        except:
            pass
 
        #check if the process with specified by pid exists
        if 0 == pid:
            return
 
        #exit the application
        print "The application is already running !"
        exit(0) #exit raise an exception so don't put it in a try/except block
 
    #called when the single instance starts to save it's pid
    def startApplication( self ):
        file = open( self.pid_file, 'wt' )
        file.write( str( os.getpid() ) )
        file.close()
 
    #called when the single instance exit ( remove pid file )
    def exitApplication( self ):
        try:
            os.remove( self.pid_file )
        except:
            pass
 
 
if __name__ == '__main__':
    #create application instance
    appInstance = ApplicationInstance( 'myapp.pid' )
 
    #do something here
    print "Start MyApp"
    time.sleep(5)    #sleep 5 seconds
    print "End MyApp"
 
    #remove pid file
    appInstance.exitApplication()
