from django_slack import slack_message

def push_to_slack(msg):
  slack_message('slacks/report_vector_missing.slack', { 'msg': msg })
