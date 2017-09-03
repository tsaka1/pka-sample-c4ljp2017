#!/usr/local/bin/ruby
#
# An example of sign-in by public-key authentication
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
  <title>Public-key Authentication</title>
  </head>
  <body>
  <h1>Public-key Authentication</h1>
  <form method="POST" action="signin-pka1.cgi" >
    Email: <input name="email" type="text" size="40" /><br/>
    <input type="submit" />
    <input type="reset" />
  </form>
  <hr/>
  <p>To register this service, please <a href="#{$sign_up_uri}">Sign-Up</a>.</p>
  <p>If you forgot your password, please follow
  <a href="#{$sign_up_uri}">Sign-Up</a> process to reset your password.</p>
  </body>
  </html>
  EOS
}

log.info($0) { "respond sign-in form." }

log.close
