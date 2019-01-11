from django.core.files.storage import Storage

# 변경 후
# return posixpath.join(dirname, self.get_valid_name(filename))

# 변경 전
# return os.path.normpath(os.path.join(dirname, self.get_valid_name(filename)))


    # def _mkremdirs(self, path):
    #     pwd = self._connection.pwd()
    #     path_splitted = path.split('/')
    #     # edit for media root mkdir
    #     ######################
    #     try:
    #         self._connection.mkd(settings.MEDIA_ROOT)
    #         self._connection.cwd(settings.MEDIA_ROOT)
    #     except:
    #         pass
    #     ########################
    #     for path_part in path_splitted:
    #         try:
    #             self._connection.cwd(path_part)
    #         except ftplib.all_errors:
    #             try:
    #                 self._connection.mkd(path_part)
    #                 self._connection.cwd(path_part)
    #             except ftplib.all_errors:
    #                 raise FTPStorageException(
    #                     'Cannot create directory chain %s' % path
    #                 )
    #     self._connection.cwd(pwd)
    #     return
    #
    # def _put_file(self, name, content):
    #     # Connection must be open!
    #     try:
    #         self._mkremdirs(os.path.dirname(name))
    #         ##############################
    #         self._connection.cwd(settings.MEDIA_ROOT)
    #         ##############################
    #         pwd = self._connection.pwd()
    #         self._connection.cwd(os.path.dirname(name))
    #         self._connection.storbinary('STOR ' + os.path.basename(name),
    #                                     content.file,
    #                                     content.DEFAULT_CHUNK_SIZE)
    #         self._connection.cwd(pwd)
    #     except ftplib.all_errors:
    #         raise FTPStorageException('Error writing file %s' % name)