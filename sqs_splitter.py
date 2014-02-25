#!/usr/bin/env python

import traceback
from clint.textui import puts, indent, colored
import boto.sqs
from boto.sqs.message import Message
import config


def get_connection():
    puts('Connecting to SQS...')
    try:
        return boto.sqs.connect_to_region(config.REGION)
    except:
        puts(colored.red(
            "Failed to connect. Did you set the AWS environment variables?\n"
            "See README for more info on AWS environment variables."))
        exit(1)


def get_incoming_queue(conn):
    puts('Getting incoming queue: %s' % config.INCOMING_QUEUE)
    incoming = conn.get_queue(config.INCOMING_QUEUE)
    if incoming is None:
        puts(colored.red("No queue found with name: %s in region: %s" % (
            config.INCOMING_QUEUE, config.REGION)))
        exit(1)

    return incoming


def get_outgoing_queues(conn):
    puts('Assembling list of outgoing queues...')
    outgoing = []
    for q in config.OUTGOING_QUEUES:
        try:
            outgoing.append(conn.create_queue(q))
            with indent(4):
                puts('added %s' % q)
        except:
            puts(colored.red("Failed to create queue %s" % q))
            traceback.print_exc()
            exit(1)

    if not outgoing:
        puts(colored.red("There are no outgoing queues."))
        exit(1)

    return outgoing


def process_messages(incoming, outgoing):
    puts('Listening for messages...')
    while True:
        try:
            message = incoming.read(wait_time_seconds=20)
            if message:
                puts('Found message:')
                msg_body = message.get_body()
                if config.VERBOSE:
                    with indent(4):
                        puts(msg_body)
                for q in outgoing:
                    out_msg = Message()
                    out_msg.set_body(msg_body)
                    q.write(out_msg)
                    with indent(4):
                        puts("Added to: %s" % q)
                incoming.delete_message(message)
                with indent(4):
                    puts('Deleted message')
        except:
            traceback.print_exc()
            exit(1)


def main():
    conn = get_connection()
    incoming = get_incoming_queue(conn)
    outgoing = get_outgoing_queues(conn)
    process_messages(incoming, outgoing)


if __name__ == "__main__":
    main()