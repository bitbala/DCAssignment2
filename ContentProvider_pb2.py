# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ContentProvider.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x43ontentProvider.proto\x12\x0f\x63ontentprovider\"<\n\x16\x43riticalSectionRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x11\n\ttimestamp\x18\x02 \x01(\x03\";\n\x17\x43riticalSectionResponse\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x0f\n\x07granted\x18\x02 \x01(\x08\"0\n\x0cReplyRequest\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x0f\n\x07granted\x18\x02 \x01(\x08\"\x0f\n\rReplyResponse2\xd4\x01\n\x16\x43ontentProviderService\x12k\n\x16RequestCriticalSection\x12\'.contentprovider.CriticalSectionRequest\x1a(.contentprovider.CriticalSectionResponse\x12M\n\x0cReceiveReply\x12\x1d.contentprovider.ReplyRequest\x1a\x1e.contentprovider.ReplyResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ContentProvider_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CRITICALSECTIONREQUEST']._serialized_start=42
  _globals['_CRITICALSECTIONREQUEST']._serialized_end=102
  _globals['_CRITICALSECTIONRESPONSE']._serialized_start=104
  _globals['_CRITICALSECTIONRESPONSE']._serialized_end=163
  _globals['_REPLYREQUEST']._serialized_start=165
  _globals['_REPLYREQUEST']._serialized_end=213
  _globals['_REPLYRESPONSE']._serialized_start=215
  _globals['_REPLYRESPONSE']._serialized_end=230
  _globals['_CONTENTPROVIDERSERVICE']._serialized_start=233
  _globals['_CONTENTPROVIDERSERVICE']._serialized_end=445
# @@protoc_insertion_point(module_scope)