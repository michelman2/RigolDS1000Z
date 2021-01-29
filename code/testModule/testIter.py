import itertools 
import __init__
from TransactionMeans import MessageCarrier

mymess = ["one" , "two" , "three" , "four" , "five"]

my_message2 = ["hello" , "wellow" , "chellow"]

message_carrier = MessageCarrier.IterMessageList(mymess)
message_carrier2 = MessageCarrier.IterMessageList(my_message2)

message_carrier.append(message_carrier2)


for message in message_carrier: 
    print(message)
