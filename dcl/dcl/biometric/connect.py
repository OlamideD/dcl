from zk import ZK, const

#dcl.dcl.biometric.connect.connect
def connect():
    conn = None
    # create ZK instance
    ip = "154.120.64.42"
    zk = ZK(ip, port=4370, timeout=10)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        # conn.disable_device()
        # # another commands will be here!
        # # Example: Get All Users
        # users = conn.get_users()
        # for user in users:
        #     privilege = 'User'
        #     if user.privilege == const.USER_ADMIN:
        #         privilege = 'Admin'
        #     print ('+ UID #{}'.format(user.uid))
        #     print ('  Name       : {}'.format(user.name))
        #     print ('  Privilege  : {}'.format(privilege))
        #     print ('  Password   : {}'.format(user.password))
        #     print ('  Group ID   : {}'.format(user.group_id))
        #     print ('  User  ID   : {}'.format(user.user_id))
        #
        # # Test Voice: Say Thank You
        # conn.test_voice()
        # # re-enable device after all commands already executed
        # conn.enable_device()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()