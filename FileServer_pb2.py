# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: FileServer.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x46ileServer.proto\"G\n\x13\x44ownloadFileRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x1d\n\x15request_forward_count\x18\x02 \x01(\x05\"N\n\x14\x44ownloadFileResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x03 \x01(\x0c\":\n\x0fSaveFileRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\x12\x14\n\x0c\x66ile_content\x18\x02 \x01(\x0c\"4\n\x10SaveFileResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2~\n\nFileServer\x12=\n\x0c\x44ownloadFile\x12\x14.DownloadFileRequest\x1a\x15.DownloadFileResponse\"\x00\x12\x31\n\x08SaveFile\x12\x10.SaveFileRequest\x1a\x11.SaveFileResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'FileServer_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DOWNLOADFILEREQUEST']._serialized_start=20
  _globals['_DOWNLOADFILEREQUEST']._serialized_end=91
  _globals['_DOWNLOADFILERESPONSE']._serialized_start=93
  _globals['_DOWNLOADFILERESPONSE']._serialized_end=171
  _globals['_SAVEFILEREQUEST']._serialized_start=173
  _globals['_SAVEFILEREQUEST']._serialized_end=231
  _globals['_SAVEFILERESPONSE']._serialized_start=233
  _globals['_SAVEFILERESPONSE']._serialized_end=285
  _globals['_FILESERVER']._serialized_start=287
  _globals['_FILESERVER']._serialized_end=413
# @@protoc_insertion_point(module_scope)
