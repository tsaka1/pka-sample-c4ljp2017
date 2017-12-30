#!/usr/local/bin/ruby
#
# Sign-out / simply deletes session objects
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
user_name = sess[USERNAME]
if !user_name
  user_name = "NOT_LOGIN"
end
sess.delete
redirect_to(cgi, $sign_in_uri)
log.info($0) { "#{user_name} signed out, redirect to #{$sign_in_uri}" }

log.close
