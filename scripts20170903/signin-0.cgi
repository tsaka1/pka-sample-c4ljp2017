#!/usr/local/bin/ruby
#
# An example of sign-in CGI script
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

user_name = sprintf("%s(%s)", ENV["REMOTE_ADDR"], Time.now.to_s)
sess[USERNAME] = user_name

redirect_to(cgi, $home_uri)
log.info($0) { "#{user_name} signed in, redirect to #{$home_uri}" }

log.close
