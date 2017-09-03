#!/usr/local/bin/ruby
#
# An example of change key of public-key authentication
#

require("cgi")
require("cgi/session")
require("logger")

load(Dir.getwd + "/config.rb")

log = Logger.new($log_file)
log.level = Logger::INFO

cgi = CGI.new
sess = CGI::Session.new(cgi, {
  "session_secure" => true,
  "tmpdir" => $sess_dir,
  "prefix" => $sess_prefix
  })

cgi.out({
  "status" => "OK",
  "type" => "text/html",
  "charset" => "utf-8"
}) {
  <<-"EOS"
  <html>
  <head>
  <title>Change Key-pair</title>
  <script type="text/javascript" src="jsrsasign-all-min.js"></script>
  </head>
  <body>
  <h1>Change Key-pair of #{esc_tags(sess[USERNAME])}</h1>
  <form method="POST" action="keychg-pka1.cgi" onsubmit="return send_key()" >
    Old Passphrase: <input name="oldpass" type="password" size="20" /><br/>
    New Passphrase: <input name="newpass" type="password" size="20" /><br/>
    New Passphrase (confirm): <input name="vrfy" type="password" size="20" /><br/>
    <input type="submit" />
    <input type="reset" />
    <input name="pubkey" type="hidden" value="" /><br/>
  </form>
  <hr/>
  <p>Save private key: <a id="prvsave" href="#" download="privatekey.txt" onclick="handlePrivate()">click!</a><br />
  Save public key: <a id="pubsave" href="#" download="publickey.txt" onclick="handlePublic()">click!</a></p>
  <p>Load private key: <input type="file" name="prvfile" id="prvfile" /><br />
  Load public key: <input type="file" name="pubfile" id="pubfile" /></p>
  <hr/>
  <p><a href="#{$home_uri}">Return to Home</a>.</p>
  <script type="text/javascript" src="keychg-pka.js"></script>
  </body>
  </html>
  EOS
}

log.info($0) { "respond key change form." }

log.close
