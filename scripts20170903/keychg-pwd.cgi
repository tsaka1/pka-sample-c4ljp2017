#!/usr/local/bin/ruby
#
# An example of change key of password authentication
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
  <title>Change Password</title>
  </head>
  <body>
  <h1>Change Password of #{esc_tags(sess[USERNAME])}</h1>
  <form method="POST" action="keychg-pwd1.cgi">
    Old Password: <input name="oldpwd" type="password" size="20" /><br/>
    New Password: <input name="newpwd" type="password" size="20" /><br/>
    New Password (confirm): <input name="vrfy" type="password" size="20" /><br/>
    <input type="submit" />
    <input type="reset" />
  </form>
  <hr/>
  <p><a href="#{$home_uri}">Return to Home</a>.</p>
  </body>
  </html>
  EOS
}

log.info($0) { "respond key change form." }

log.close
