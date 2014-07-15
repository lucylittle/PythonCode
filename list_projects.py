# import jira ComponentManager
import com.atlassian.jira.ComponentManager as cm
 
# Create variable for to Project in jira
pm = cm.getInstance().getProjectManager()
 
# foor loor to print list of projects
for p in pm.getProjects() :
    print p
