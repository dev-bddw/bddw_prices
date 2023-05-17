# QUICK EXPLANATION OF SCRIPTS IN THIS DIR #

build_all.sh > runs the build scripts in all the directories, the build scripts run the vite build for production which
				produces the dist/ assets and then we use replace.py, which just changes the path so that django can serve it
				as a static file (the js, css dependencies)
run_static.sh > runs staticfy.py which converts all the dependenices for the react files to django static url tags
