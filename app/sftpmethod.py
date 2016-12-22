import paramiko
import time


class getversion(object):  
        def ssh_connect(self,_host,_username,_password,_command1,_command2):
            try:
                self._ssh_fd = paramiko.SSHClient()
                self._ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_fd.connect(_host,username=_username,password=_password)
                stdin, stdout, stderr = self._ssh_fd.exec_command(_command1)
                sver = stdout.readlines()
                stdin, stdout, stderr = self._ssh_fd.exec_command(_command2)
                tver = stdout.readlines()
                return sver,tver
            except Exception,e:
                print('ssh %s@%s:%s'%(_username,_host,e))
                exit()
            return self._ssh_fd
        def sftp_open(self,_ssh_fd):
                return self._ssh_fd.open_sftp()
        def ssh_close(self,_ssh_fd):
                self._ssh_fd.close()


class dosendapp(object):  
        def ssh_connect(self,_host,_username,_password):
            try:
                self._ssh_fd = paramiko.SSHClient()
                self._ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_fd.connect(_host,username=_username,password=_password)
                #print stdout.readlines()
            except Exception,e:
                print('ssh %s@%s:%s'%(_username,_host,e))
                exit()
            return self._ssh_fd
        
        def sftp_open(self,_ssh_fd):
                return self._ssh_fd.open_sftp()
        def sftp_up(self,_sftp_fd,_put_from_path,_put_to_path):
                return _sftp_fd.put(_put_from_path,_put_to_path)
        def sftp_down(self,_sftp_fd,_get_from_path,_get_to_path):
                return _sftp_fd.get(_get_from_path,_get_to_path)
        def sftp_close(self,_sftp_fd):
                self._sftp_fd.close()
        def ssh_close(self,_ssh_fd):
                self._ssh_fd.close()

class viapp(object):  
        def ssh_connect(self,_host,_username,_password,_command2):
            try:
                self._ssh_fd = paramiko.SSHClient()
                self._ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_fd.connect(_host,username=_username,password=_password)
                self._ssh_fd.exec_command(_command2)
                #print stdout.readlines()
            except Exception,e:
                print('ssh %s@%s:%s'%(_username,_host,e))
                exit()
            return self._ssh_fd
        
        def sftp_open(self,_ssh_fd):
                return self._ssh_fd.open_sftp()
        def sftp_up(self,_sftp_fd,_put_from_path,_put_to_path):
                return _sftp_fd.put(_put_from_path,_put_to_path)
        def sftp_down(self,_sftp_fd,_get_from_path,_get_to_path):
                return _sftp_fd.get(_get_from_path,_get_to_path)
        def sftp_close(self,_sftp_fd):
                self._sftp_fd.close()
        def ssh_close(self,_ssh_fd):
                self._ssh_fd.close()

class viapp1(object):  
        def ssh_connect(self,_host,_username,_password,_command2,_command3):
            try:
                self._ssh_fd = paramiko.SSHClient()
                self._ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self._ssh_fd.connect(_host,username=_username,password=_password)
                self._ssh_fd.exec_command(_command2)
                self._ssh_fd.exec_command(_command3)
                #print stdout.readlines()
            except Exception,e:
                print('ssh %s@%s:%s'%(_username,_host,e))
                exit()
            return self._ssh_fd
        
        def sftp_open(self,_ssh_fd):
                return self._ssh_fd.open_sftp()
        def sftp_up(self,_sftp_fd,_put_from_path,_put_to_path):
                return _sftp_fd.put(_put_from_path,_put_to_path)
        def sftp_down(self,_sftp_fd,_get_from_path,_get_to_path):
                return _sftp_fd.get(_get_from_path,_get_to_path)
        def sftp_close(self,_sftp_fd):
                self._sftp_fd.close()
        def ssh_close(self,_ssh_fd):
                self._ssh_fd.close()


