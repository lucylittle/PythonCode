from jira.client import JIRA

options = {

'server': 'our_server'

}

jira = JIRA(options=options,basic_auth=('u_name', 'pswrd'))

issue = jira.issue('issue_id')

file=open('/Desktop/test.xlsx','rb')

attachement_object=jira.add_attachment(issue,file)

file.close() 
