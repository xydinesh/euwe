USERS = {'max':'user_max',
          'ruby':'admin_ruby'}
GROUPS = {'ruby':['group:admins']}

def group_finder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
