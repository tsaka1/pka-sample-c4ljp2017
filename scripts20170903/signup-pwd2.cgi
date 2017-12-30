#!/usr/local/bin/ruby
#
# An example of sign-up for password authentication
#

require("cgi")
require("cgi/session")
require("logger")
require("sqlite3")
require("securerandom")
require("digest/sha1")

load(Dir.getwd + "/config.rb")

log = Logger.new($log_file)
log.level = Logger::INFO

cgi = CGI.new
sess = CGI::Session.new(cgi, {
  "session_secure" => true,
  "tmpdir" => $sess_dir,
  "prefix" => $sess_prefix
  })

u_name = cgi["email"]
u_pin = cgi["pin"]
salt = nil
pass = nil
stat = nil
db = SQLite3::Database.new($db_name)
begin
  begin
    db.transaction{
      db.execute("update pwd set status = 'locked' where status = 'reset' \
	  and tstamp < datetime('now', '-24 hours');")
      db.execute("select salt, passwd from pwd where email = ? \
	  and status = 'reset';", u_name){ |r|
	salt = r[0]
	pass = r[1]
      }
    }
  rescue SQLite3::BusyException
    sleep(0.1)
    retry
  end
  if !salt || !pass
    redirect_to(cgi, $sign_in_uri)
    log.info($0) { "signup/reset not started, redirect to #{$sign_in_uri}" }
  elsif Digest::SHA1.hexdigest(salt + u_pin) != pass
    redirect_to(cgi, $sign_up_uri)
    log.info($0) { "PIN invalid, redirect to #{$sign_up_uri}" }
  else
    cgi.out({
      "status" => "OK",
      "type" => "text/html",
      "charset" => "utf-8"
    }) {
      <<-"EOS"
      <html>
      <head>
      <title>Reset Password</title>
      </head>
      <body>
      <h1>Reset Password of #{esc_tags(u_name)}</h1>
      <form method="POST" action="signup-pwd3.cgi">
	New Password: <input name="newpwd" type="password" size="20" /><br/>
	New Password (confirm): <input name="vrfy" type="password" size="20" /><br/>
	<input name="pin" type="hidden" value="#{u_pin}" />
	<input name="email" type="hidden" value="#{u_name}" />
	<input type="submit" />
	<input type="reset" />
      </form>
      <hr/>
      <p><a href="#{$home_uri}">Return to Home</a>.</p>
      </body>
      </html>
      EOS
    }
  end
  log.info($0) { "respond password reset form." }
ensure
  db.close
end

log.close

