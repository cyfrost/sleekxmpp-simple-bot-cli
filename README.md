# SleekXMPP CLI (ephemeral, and not ncurses!)

This repo derives from the very simple [EchoBot](https://github.com/fritzy/SleekXMPP/blob/develop/examples/echo_client.py) from the SleekXMPP examples repository.

The EchoBot script has been subtly modified to make it work in a simple-send-and-get script like. You'd supply all the necessary arguments while running this python script and it'd connect to the XMPP server, authenticate as `user1` with their supplied password, send a message `hello` to `user2`, wait indefinitely for a response, once received, prints the response from `user2` to the console, and then exits the program. See below for Usage and examples!

### Usage:

This very simple project uses [pipenv](https://pipenv.kennethreitz.org/) to handle the only dependency (SleekXMPP).

To get started:

1. Download this repo as a ZIP, extract it somewhere (or just clone it via Git)

2. Open a Terminal prompt

3. Make sure [pipenv is installed](https://pipenv.kennethreitz.org/en/latest/#install-pipenv-today)

4. Run `pipenv install` (this installs all the dependencies needed for the script to work --currently only one ---`sleekxmpp`)

5. Run `pipenv run python sleekxmpp-cli.py --from-jid "user1@blabber.im" --password "somerandompassword" --to-jid "user2@blabber.im" --message "Hello from user1, sent via XMPP CLI script!" --verbose`

The above command will first connect to the XMPP server (`blabber.im` in the example) (YES! SSL/TLS upto v1.2 only is supported), authenticates as the from JID (`user1@blabber.im`) with supplied password, sends the given message to the To-JID (`user2@blabber.im`), then waits for a response indefinitely, prints the response to console once its received, and finally exits the program.

#### CLI arguments

```
Usage:

-f, --from-jid - the Jabber ID from which the message is to be sent.
-p, --password - the password of the From-JID, needed to authenticate as them.
-t, --to-jid   - the destination Jabber ID to which you wish to send a message to (can be a XMPP Bot/Human/whatever).
-m, --message  - the message you want to send as From-JID to To-JID.
-v, --verbose  - enables Verbose logging about inbetweening. If this is disabled, no output except the actual response body will be printed to stdout.

Example: pipenv run python sleekxmpp-cli.py -f "bob@blabber.im" -p "doncorleone" -t "alice@blabber.im" -m "hi from bob!"

This example sends a message from bob to alice and then waits for a response text from alice, once received, prints it to console and exits the program (There are no log messages except the actual response stanza body because --verbose flag isn't supplied).

```

### Screenshot

![Imgur Image](https://i.imgur.com/jH6f9HA.png)

### Use-cases
Top of my head:

1. Send messages to a device running an app/bot which is listening for XMPP messages, interprets them as commands, run them, and sends back the response with the output of the executed command.

(Example: use the script in this repo to send a "ping" message to a bot accepting XMPP commands, then the response would be "pong" in the terminal after this script is finished, now you can parse the result of the command (via stdout stream) and take actions based off of it). 

### Notes

1. Support for TLS v1.3 isn't really working at this point but that's soon to change probably given the wave of its adoption.
2. You could run a thread to send multiple messages and spawn multiple message listeners and actions, this example was deliberately kept simple for demonstration.
3. Jabber (formerly XMPP) is an IM protocol used by people around the world with a solid history of stability, reliability, and federated network of servers. SleekXMPP works with Jabber, and the long-lived GTalk (?), so you'd need to sign-up with one of the free Jabber networks (Blabber.im for example) or even-better self-host an ejabberd/prosody instance on a cheap VPS.
4. one of the drawbacks of the example script mentioned above is that, for every invocation it'd connect, auth, send message, await response, print response, disconnect, exit. If you'd like to avoid such a cycle, refer to #2.
5. This entire example will work perfectly fine on arm64 devices as long as there's a shell environment available (Recommended: Termux). Perhaps, you can even make use of the Tasker-Termux plugin to automate sending/receiving/reacting to XMPP messages from Tasker and its superb comfort of automation).
