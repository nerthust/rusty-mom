# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\x12\x08messages\"\x12\n\x10HeartbeatRequest\"\x15\n\x13HeartbeatOkResponse\")\n\x13SubscriptionRequest\x12\x12\n\nchannel_id\x18\x01 \x01(\t\"5\n\x07Message\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\x12\r\n\x05topic\x18\x03 \x01(\t\";\n\x04Push\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\x0c\x12\r\n\x05topic\x18\x02 \x01(\t\x12\x13\n\x0bqueue_label\x18\x03 \x01(\t\"\x10\n\x0ePushOkResponse\")\n\x12\x43reateQueueRequest\x12\x13\n\x0bqueue_label\x18\x01 \x01(\t\"\x17\n\x15\x43reateQueueOkResponse\"*\n\x13RebuildQueueRequest\x12\x13\n\x0bqueue_label\x18\x01 \x01(\t\"\x18\n\x16RebuildQueueOkResponse\")\n\x12\x44\x65leteQueueRequest\x12\x13\n\x0bqueue_label\x18\x01 \x01(\t\"\x17\n\x15\x44\x65leteQueueOkResponse\":\n\x14\x43reateChannelRequest\x12\x13\n\x0bqueue_label\x18\x01 \x01(\t\x12\r\n\x05topic\x18\x02 \x01(\t\"+\n\x15\x43reateChannelResponse\x12\x12\n\nchannel_id\x18\x01 \x01(\t\"\x13\n\x11ListQueuesRequest\"$\n\x12ListQueuesResponse\x12\x0e\n\x06queues\x18\x01 \x03(\t\"\x15\n\x13ListChannelsRequest\"(\n\x14ListChannelsResponse\x12\x10\n\x08\x63hannels\x18\x01 \x03(\t\"*\n\x14\x44\x65leteChannelRequest\x12\x12\n\nchannel_id\x18\x01 \x01(\t\"\x19\n\x17\x44\x65leteChannelOkResponse2\x9c\x06\n\rMessageStream\x12J\n\x12SubscribeToChannel\x12\x1d.messages.SubscriptionRequest\x1a\x11.messages.Message\"\x00\x30\x01\x12\x39\n\x0bPushToQueue\x12\x0e.messages.Push\x1a\x18.messages.PushOkResponse\"\x00\x12N\n\x0b\x43reateQueue\x12\x1c.messages.CreateQueueRequest\x1a\x1f.messages.CreateQueueOkResponse\"\x00\x12N\n\x0b\x44\x65leteQueue\x12\x1c.messages.DeleteQueueRequest\x1a\x1f.messages.DeleteQueueOkResponse\"\x00\x12Q\n\x0cRebuildQueue\x12\x1d.messages.RebuildQueueRequest\x1a .messages.RebuildQueueOkResponse\"\x00\x12R\n\rCreateChannel\x12\x1e.messages.CreateChannelRequest\x1a\x1f.messages.CreateChannelResponse\"\x00\x12I\n\nListQueues\x12\x1b.messages.ListQueuesRequest\x1a\x1c.messages.ListQueuesResponse\"\x00\x12O\n\x0cListChannels\x12\x1d.messages.ListChannelsRequest\x1a\x1e.messages.ListChannelsResponse\"\x00\x12T\n\rDeleteChannel\x12\x1e.messages.DeleteChannelRequest\x1a!.messages.DeleteChannelOkResponse\"\x00\x12K\n\x0cGetHeartbeat\x12\x1a.messages.HeartbeatRequest\x1a\x1d.messages.HeartbeatOkResponse\"\x00\x42\x06\xa2\x02\x03MSGb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\242\002\003MSG'
  _HEARTBEATREQUEST._serialized_start=28
  _HEARTBEATREQUEST._serialized_end=46
  _HEARTBEATOKRESPONSE._serialized_start=48
  _HEARTBEATOKRESPONSE._serialized_end=69
  _SUBSCRIPTIONREQUEST._serialized_start=71
  _SUBSCRIPTIONREQUEST._serialized_end=112
  _MESSAGE._serialized_start=114
  _MESSAGE._serialized_end=167
  _PUSH._serialized_start=169
  _PUSH._serialized_end=228
  _PUSHOKRESPONSE._serialized_start=230
  _PUSHOKRESPONSE._serialized_end=246
  _CREATEQUEUEREQUEST._serialized_start=248
  _CREATEQUEUEREQUEST._serialized_end=289
  _CREATEQUEUEOKRESPONSE._serialized_start=291
  _CREATEQUEUEOKRESPONSE._serialized_end=314
  _REBUILDQUEUEREQUEST._serialized_start=316
  _REBUILDQUEUEREQUEST._serialized_end=358
  _REBUILDQUEUEOKRESPONSE._serialized_start=360
  _REBUILDQUEUEOKRESPONSE._serialized_end=384
  _DELETEQUEUEREQUEST._serialized_start=386
  _DELETEQUEUEREQUEST._serialized_end=427
  _DELETEQUEUEOKRESPONSE._serialized_start=429
  _DELETEQUEUEOKRESPONSE._serialized_end=452
  _CREATECHANNELREQUEST._serialized_start=454
  _CREATECHANNELREQUEST._serialized_end=512
  _CREATECHANNELRESPONSE._serialized_start=514
  _CREATECHANNELRESPONSE._serialized_end=557
  _LISTQUEUESREQUEST._serialized_start=559
  _LISTQUEUESREQUEST._serialized_end=578
  _LISTQUEUESRESPONSE._serialized_start=580
  _LISTQUEUESRESPONSE._serialized_end=616
  _LISTCHANNELSREQUEST._serialized_start=618
  _LISTCHANNELSREQUEST._serialized_end=639
  _LISTCHANNELSRESPONSE._serialized_start=641
  _LISTCHANNELSRESPONSE._serialized_end=681
  _DELETECHANNELREQUEST._serialized_start=683
  _DELETECHANNELREQUEST._serialized_end=725
  _DELETECHANNELOKRESPONSE._serialized_start=727
  _DELETECHANNELOKRESPONSE._serialized_end=752
  _MESSAGESTREAM._serialized_start=755
  _MESSAGESTREAM._serialized_end=1551
# @@protoc_insertion_point(module_scope)
