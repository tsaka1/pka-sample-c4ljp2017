#!/usr/local/bin/ruby
#
# An example of sign-up for public-key authentication
#

require("cgi")
require("cgi/session")
require("logger")
require("sqlite3")

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
  <title>Sign-Up / Password reset form</title>
  </head>
  <body>
  <h1>Sign-Up / Key-pair reset form</h1>
  <form method="POST" action="signup-pka1.cgi">
    Email: <input name="email" type="text" size="40" /><br/>
    Keyword: <input name="kwd" type="password" size="20" /><br/>
    <input type="submit" />
    <input type="reset" />
  </form>
  <hr/>
  <p>Note: Please type-in family name of the developer as keyword.</p>
  <p>Back to <a href="#{$sign_in_uri}">Sign in Page</a>.</p>
  </body>
  </html>
  EOS
}

log.info($0) { "respond sign-up form." }

log.close
