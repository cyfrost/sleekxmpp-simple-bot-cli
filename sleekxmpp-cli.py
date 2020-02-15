import sys
import logging
import getpass
from optparse import OptionParser
import sleekxmpp

class EchoBot(sleekxmpp.ClientXMPP):
    to_jid = None
    message_to_send = None
    is_verbose_logging_enabled = None
    should_exit_after_send = None

    def __init__(self, jid, pwd, to_jid, message, should_exit_after_send, is_verbose_logging_enabled):
        sleekxmpp.ClientXMPP.__init__(self, jid, pwd)
        self.to_jid = to_jid
        self.message_to_send = message
        self.is_verbose_logging_enabled = is_verbose_logging_enabled
        self.should_exit_after_send = should_exit_after_send
        self.add_event_handler('session_start', self.start)
        if not self.should_exit_after_send:
            self.add_event_handler('message', self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        msg = str.format("Sending message: \"{}\" to user \"{}\"", self.message_to_send, self.to_jid)
        self.logToStdout(is_verbose_logging_enabled, msg)
        self.send_message(self.to_jid, self.message_to_send)
        if self.should_exit_after_send:
            sys.exit(0)
        self.logToStdout(is_verbose_logging_enabled, "Message sent! awaiting response...")

    def logToStdout(self, is_logging_enabled, msg):
        if is_logging_enabled:
            print(msg)

    def message(self, msg):
        self.logToStdout(is_verbose_logging_enabled, "\n================\nReceived response\n================")
        print(msg['body'])
        self.logToStdout(is_verbose_logging_enabled, "================\n")
        sys.exit(0)

def logToStdout(is_logging_enabled, msg):
    if is_logging_enabled:
        print(msg)

if __name__ == "__main__":
    optp = OptionParser()
    optp.add_option('-f', '--from-jid', dest="from_jid", help="From JID")
    optp.add_option('-p', '--password', dest='password', help="From JID password")
    optp.add_option('-t', '--to-jid', dest="to_jid", help="To JID")
    optp.add_option('-m', '--message', dest="send_message", help="Message to send")
    optp.add_option('-n', '--no-wait', dest="no_await_response", help="Send message and exit immediately; no wait for response", action='store_const', const='no_await_response')
    optp.add_option('-v', '--verbose', dest="verbose", help="Enable verbose logging", action='store_const', const='verbose')

    opts, args = optp.parse_args()

    is_verbose_logging_enabled = opts.verbose is not None
    from_jid = opts.from_jid
    from_jid_pass = opts.password
    to_jid = opts.to_jid
    message_to_send = opts.send_message
    should_exit_after_send = opts.no_await_response is not None

    if from_jid is None or from_jid_pass is None or to_jid is None or message_to_send is None:
        print("\nInsufficient arguments!\n")
        sys.exit(1)

    logToStdout(is_verbose_logging_enabled, "Info: Settings OK. Connecting to XMPP server...")

    xmpp = EchoBot(from_jid, from_jid_pass, to_jid, message_to_send, should_exit_after_send, is_verbose_logging_enabled)
    xmpp.register_plugin('xep_0030')  # service discovery
    xmpp.register_plugin('xep_0004')  # date form
    xmpp.register_plugin('xep_0060')  # pubsub
    xmpp.register_plugin('xep_0199')  # xmpp ping

    if xmpp.connect():
        logToStdout(is_verbose_logging_enabled, "Info: Connected successfully!")
        xmpp.process(block=True)
        logToStdout(is_verbose_logging_enabled, "Finished!")
    else:
        print("Error: failed to connect to XMPP server!")
        sys.exit(1)
