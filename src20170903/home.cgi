#!/usr/local/bin/ruby
#
# An example of CGI script with session management
#

require("cgi")
require("cgi/session")
require("logger")

load(Dir.getwd + "/config.rb")

log = Logger.new($log_file)
log.level = Logger::INFO

sess = nil
user_name = nil
new_sess = false

cgi = CGI.new
begin
  sess = CGI::Session.new(cgi, {
    "session_secure" => true,
    "new_session" => false,
    "tmpdir" => $sess_dir,
    "prefix" => $sess_prefix
    })
  user_name = sess[USERNAME]
rescue ArgumentError => e	# if not sign-in
  new_sess = true
end

if new_sess || !user_name
  redirect_to(cgi, $sign_in_uri)
  log.info($0) { "not signed in, redirect to #{$sign_in_uri}" }
else
  cgi.out({
    "status" => "OK",
    "type" => "text/html",
    "charset" => "utf-8"
  }){
    <<-"EOS"
    <html>
    <head>
      <title>Example Home</title>
    </head>
    <body>
    [<a href="#{$home_uri}">Home</a>]
    [<a href="#{$sign_out_uri}">Sign-Out</a>]
    [<a href="#{$key_chg_uri}">Change Password/Key</a>]
    <hr/>
    <p>Your name is &quot;#{esc_tags(user_name)}&quot;</p>
    <p>Fortune message:</p>
    <hr/>
    <pre>#{esc_tags(IO.popen("/usr/games/fortune", "r"){ | i | i.read })}</pre>
    <hr/>
    <p>Now: #{esc_tags(Time.now.to_s)}</p>
    </body>
    </html>
    EOS
  }
  log.info($0) { "done." }
end

log.close
